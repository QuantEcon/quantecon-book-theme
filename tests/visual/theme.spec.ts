import { test, expect, Page } from "@playwright/test";

/**
 * Visual regression tests for quantecon-book-theme.
 *
 * Snapshots are captured against the quantecon-book-theme-fixtures site,
 * which contains a curated set of synthetic pages (one per theme surface)
 * plus real-world lecture captures that previously exposed theme bugs.
 *
 * Since fixtures don't execute notebooks, every page renders deterministic
 * output — there is no need to skip full-page screenshots for "pages with
 * plots" as the previous lecture-python-programming setup required.
 */

// Wait for the page to fully settle, including MathJax typesetting when the
// page contains math (pages without MathJax pass the typeset gate
// immediately; the font and height-stability waits below apply to every
// page).
//
// After MathJax's startup promise resolves, font loading and late reflow
// can still shift the total page height for a short window. Full-page
// screenshots fail outright on any dimension mismatch (before pixel
// tolerances apply), so a fixed post-typeset delay isn't enough: math-heavy
// pages were observed settling ~60px apart between runs on mobile-chrome.
// Instead of sleeping, wait for web fonts and then require the document
// height to hold steady across consecutive polls.
//
// NB: waitForFunction's second positional parameter is `arg` (forwarded to
// the page function) — `timeout`/`polling` options must go third.
async function waitForReady(page: Page) {
  await page.waitForLoadState("networkidle");
  await page.waitForFunction(
    () => {
      const mj = (window as any).MathJax;
      if (!mj || !mj.startup || !mj.startup.promise) return true;
      return mj.startup.promise.then(() => true);
    },
    undefined,
    { timeout: 15000 }
  );
  await page.waitForFunction(
    () => document.fonts.ready.then(() => true),
    undefined,
    { timeout: 15000 }
  );
  // Stable means three consecutive 250ms polls (750ms) without the
  // document height changing.
  await page.waitForFunction(
    () => {
      const w = window as any;
      const height = Math.max(
        document.body.scrollHeight,
        document.documentElement.scrollHeight
      );
      if (w.__qeLastHeight === height) {
        w.__qeStablePolls = (w.__qeStablePolls ?? 0) + 1;
      } else {
        w.__qeLastHeight = height;
        w.__qeStablePolls = 0;
      }
      return w.__qeStablePolls >= 3;
    },
    undefined,
    { timeout: 15000, polling: 250 }
  );
}

// hasMath: true loosens the snapshot tolerance for that page. MathJax font
// metrics shift slightly across environments (Ubuntu CI vs macOS local),
// so pages with rendered math need a wider tolerance than the strict default.
// Pages without math keep the default `maxDiffPixelRatio: 0.01` from
// playwright.config.ts so sub-pixel regressions still get caught.
//
// fullPage: false skips the full-page screenshot test entirely. Use for
// real-world fixtures where the rendered page height isn't stable enough
// for pixel comparison (MathJax + dynamic content can shift total height
// by hundreds of pixels between runs, which fails Playwright's
// dimension-matched comparison regardless of tolerance). Header + sidebar
// region tests still run and provide theme-regression coverage; the full
// page is reviewable via the Netlify preview.
const fixturePages = [
  { name: "intro",            path: "/intro.html",                                       hasMath: false, fullPage: true  },
  { name: "typography",       path: "/synthetic/typography.html",                        hasMath: false, fullPage: true  },
  { name: "definition-lists", path: "/synthetic/definition-lists.html",                  hasMath: true,  fullPage: true  },
  { name: "code-blocks",      path: "/synthetic/code-blocks.html",                       hasMath: false, fullPage: true  },
  { name: "math",             path: "/synthetic/math.html",                              hasMath: true,  fullPage: true  },
  { name: "admonitions",      path: "/synthetic/admonitions.html",                       hasMath: true,  fullPage: true  },
  { name: "exercises",        path: "/synthetic/exercises.html",                         hasMath: true,  fullPage: true  },
  { name: "proofs",           path: "/synthetic/proofs.html",                            hasMath: true,  fullPage: true  },
  { name: "tables",           path: "/synthetic/tables.html",                            hasMath: true,  fullPage: true  },
  { name: "figures",          path: "/synthetic/figures.html",                           hasMath: false, fullPage: true  },
  { name: "toc-deep-nesting", path: "/synthetic/toc-deep-nesting.html",                  hasMath: false, fullPage: true  },
  { name: "long-page",        path: "/synthetic/long-page.html",                         hasMath: true,  fullPage: true  },
  { name: "cross-references", path: "/synthetic/cross-references.html",                  hasMath: true,  fullPage: true  },
  { name: "prob-matrix",      path: "/real-world/from-lecture-python/prob_matrix.html",  hasMath: true,  fullPage: false },
];

test.describe("Visual Regression Tests", () => {
  for (const page of fixturePages) {
    test(`${page.name} - full page screenshot`, async ({ page: browserPage }, testInfo) => {
      test.skip(!page.fullPage, "full-page screenshot disabled for this fixture (height instability)");
      await browserPage.goto(page.path);
      await waitForReady(browserPage);

      await expect(browserPage).toHaveScreenshot(`${page.name}.png`, {
        fullPage: true,
        // Default 5000ms isn't enough for long fixtures like long-page
        // (which has math + many sections). 30s covers stitching the
        // tallest stable pages and is harmless for short ones (they finish
        // in well under a second).
        timeout: 30000,
        // Apply the looser tolerance only for pages with rendered math.
        // Non-math pages keep the strict default from playwright.config.ts.
        ...(page.hasMath ? { maxDiffPixelRatio: 0.05 } : {}),
      });
    });

    test(`${page.name} - header region`, async ({ page: browserPage }) => {
      await browserPage.goto(page.path);
      await waitForReady(browserPage);

      const header = browserPage.locator(".qe-page__header");
      if (await header.isVisible()) {
        await expect(header).toHaveScreenshot(`${page.name}-header.png`);
      }
    });

    test(`${page.name} - sidebar region`, async ({ page: browserPage }) => {
      await browserPage.goto(page.path);
      await waitForReady(browserPage);

      const sidebar = browserPage.locator(".qe-sidebar");
      if (await sidebar.isVisible()) {
        await expect(sidebar).toHaveScreenshot(`${page.name}-sidebar.png`);
      }
    });
  }
});

test.describe("Theme Features", () => {
  test("dark mode toggle", async ({ page }) => {
    await page.goto("/synthetic/typography.html");
    await waitForReady(page);

    const contrastBtn = page.locator(".btn__contrast");
    if (await contrastBtn.isVisible()) {
      await contrastBtn.click();
      await page.waitForTimeout(300);

      await expect(page).toHaveScreenshot("dark-mode.png", {
        fullPage: true,
      });
    }
  });

  test("code block styling", async ({ page }) => {
    await page.goto("/synthetic/code-blocks.html");
    await waitForReady(page);

    const codeBlock = page.locator(".highlight").first();
    if (await codeBlock.isVisible()) {
      await expect(codeBlock).toHaveScreenshot("code-block.png");
    }
  });

  test("f-string interpolation styling", async ({ page }, testInfo) => {
    // Skip on mobile — viewport too narrow to meaningfully test f-string styling.
    test.skip(testInfo.project.name === "mobile-chrome", "F-string test only relevant on desktop");

    // synthetic/code-blocks.html contains a section dedicated to f-strings
    // with named .si (String.Interpol) tokens.
    await page.goto("/synthetic/code-blocks.html");
    await waitForReady(page);

    const fstringBlock = page.locator(".highlight:has(.si)").first();
    if (await fstringBlock.isVisible()) {
      await expect(fstringBlock).toHaveScreenshot("fstring-interpolation.png");
    }
  });

  test("math equation rendering", async ({ page }) => {
    await page.goto("/synthetic/math.html");
    await waitForReady(page);
    // Extra settle time beyond waitForReady for MathJax font metrics.
    await page.waitForTimeout(1000);

    const mathParagraph = page.locator("p:has(.MathJax)").first();
    if (await mathParagraph.isVisible()) {
      // MathJax font rendering varies across environments (Ubuntu CI vs
      // macOS, different font stacks, hinting differences). Ratio-based
      // tolerance scales with element size.
      await expect(mathParagraph).toHaveScreenshot("math-equation.png", {
        maxDiffPixelRatio: 0.15,
      });
    }
  });

  test("toolbar visibility", async ({ page }) => {
    await page.goto("/intro.html");
    await waitForReady(page);

    const toolbar = page.locator(".qe-toolbar");
    await expect(toolbar).toHaveScreenshot("toolbar.png", {
      maxDiffPixelRatio: 0.03,
    });
  });
});

test.describe("Typography Styling", () => {
  test("bold text styling", async ({ page }) => {
    await page.goto("/synthetic/typography.html");
    await waitForReady(page);

    const paragraph = page.locator(".qe-page__content p:has(strong)").first();
    await expect(paragraph).toHaveScreenshot("bold-text.png");
  });

  test("italic text styling", async ({ page }) => {
    await page.goto("/synthetic/typography.html");
    await waitForReady(page);

    const paragraph = page.locator(".qe-page__content p:has(em)").first();
    await expect(paragraph).toHaveScreenshot("italic-text.png");
  });

  test("bold text in dark mode", async ({ page }) => {
    await page.goto("/synthetic/typography.html");
    await waitForReady(page);

    const contrastBtn = page.locator(".btn__contrast");
    await contrastBtn.click();
    await page.waitForTimeout(300);

    const paragraph = page.locator(".qe-page__content p:has(strong)").first();
    await expect(paragraph).toHaveScreenshot("bold-text-dark.png");
  });

  test("italic text in dark mode", async ({ page }) => {
    await page.goto("/synthetic/typography.html");
    await waitForReady(page);

    const contrastBtn = page.locator(".btn__contrast");
    await contrastBtn.click();
    await page.waitForTimeout(300);

    const paragraph = page.locator(".qe-page__content p:has(em)").first();
    await expect(paragraph).toHaveScreenshot("italic-text-dark.png");
  });
});

test.describe("Definition Lists", () => {
  // The fixtures repo's synthetic/definition-lists.html exists specifically
  // because lecture-python-programming had no <dl> content to test against.
  test("definition list rendering", async ({ page }) => {
    await page.goto("/synthetic/definition-lists.html");
    await waitForReady(page);

    const dl = page.locator("dl").first();
    if (await dl.isVisible()) {
      await expect(dl).toHaveScreenshot("definition-list.png");
    }
  });

  test("glossary rendering", async ({ page }) => {
    await page.goto("/synthetic/definition-lists.html");
    await waitForReady(page);

    const glossary = page.locator(".glossary").first();
    if (await glossary.isVisible()) {
      await expect(glossary).toHaveScreenshot("glossary.png");
    }
  });
});
