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
// page contains math. Pages without MathJax resolve immediately.
async function waitForReady(page: Page) {
  await page.waitForLoadState("networkidle");
  await page.waitForFunction(
    () => {
      const mj = (window as any).MathJax;
      if (!mj || !mj.startup || !mj.startup.promise) return true;
      return mj.startup.promise.then(() => true);
    },
    { timeout: 15000 }
  );
  await page.waitForTimeout(500);
}

// hasMath: true loosens the snapshot tolerance for that page. MathJax font
// metrics shift slightly across environments (Ubuntu CI vs macOS local),
// so pages with rendered math need a wider tolerance than the strict default.
// Pages without math keep the default `maxDiffPixelRatio: 0.01` from
// playwright.config.ts so sub-pixel regressions still get caught.
const fixturePages = [
  { name: "intro",            path: "/intro.html",                                       hasMath: false },
  { name: "typography",       path: "/synthetic/typography.html",                        hasMath: false },
  { name: "definition-lists", path: "/synthetic/definition-lists.html",                  hasMath: true  },
  { name: "code-blocks",      path: "/synthetic/code-blocks.html",                       hasMath: false },
  { name: "math",             path: "/synthetic/math.html",                              hasMath: true  },
  { name: "admonitions",      path: "/synthetic/admonitions.html",                       hasMath: true  },
  { name: "exercises",        path: "/synthetic/exercises.html",                         hasMath: true  },
  { name: "proofs",           path: "/synthetic/proofs.html",                            hasMath: true  },
  { name: "tables",           path: "/synthetic/tables.html",                            hasMath: true  },
  { name: "figures",          path: "/synthetic/figures.html",                           hasMath: false },
  { name: "toc-deep-nesting", path: "/synthetic/toc-deep-nesting.html",                  hasMath: false },
  { name: "long-page",        path: "/synthetic/long-page.html",                         hasMath: true  },
  { name: "cross-references", path: "/synthetic/cross-references.html",                  hasMath: true  },
  { name: "prob-matrix",      path: "/real-world/from-lecture-python/prob_matrix.html",  hasMath: true  },
];

test.describe("Visual Regression Tests", () => {
  for (const page of fixturePages) {
    test(`${page.name} - full page screenshot`, async ({ page: browserPage }) => {
      await browserPage.goto(page.path);
      await waitForReady(browserPage);

      await expect(browserPage).toHaveScreenshot(`${page.name}.png`, {
        fullPage: true,
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
