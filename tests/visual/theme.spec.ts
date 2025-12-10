import { test, expect } from "@playwright/test";

/**
 * Visual regression tests for quantecon-book-theme.
 *
 * These tests capture screenshots of key page types from the lecture site
 * and compare them against baseline snapshots to detect styling regressions.
 *
 * Note: Full-page screenshots are only tested for pages without matplotlib plots,
 * since plot rendering varies between CI runs. For pages with plots, we test
 * only the theme elements (header, sidebar) which are stable.
 */

// Pages to test - these represent different content types in lectures
// Pages with matplotlib figures should only test header/sidebar (stable theme elements)
const testPages = [
  { name: "homepage", path: "/index.html", hasPlots: false },
  { name: "intro", path: "/intro.html", hasPlots: false },
  { name: "getting-started", path: "/getting_started.html", hasPlots: true },
  { name: "python-by-example", path: "/python_by_example.html", hasPlots: true },
  { name: "numpy", path: "/numpy.html", hasPlots: true },
  { name: "matplotlib", path: "/matplotlib.html", hasPlots: true },
];

test.describe("Visual Regression Tests", () => {
  for (const page of testPages) {
    // Full page screenshots only for pages without dynamic content (matplotlib plots)
    // Pages with plots vary between CI runs, so we only test theme elements
    if (!page.hasPlots) {
      test(`${page.name} - full page screenshot`, async ({
        page: browserPage,
      }) => {
        await browserPage.goto(page.path);
        // Wait for fonts and images to load
        await browserPage.waitForLoadState("networkidle");
        // Wait a bit more for any CSS animations to complete
        await browserPage.waitForTimeout(500);

        await expect(browserPage).toHaveScreenshot(`${page.name}.png`, {
          fullPage: true,
        });
      });
    }

    test(`${page.name} - header region`, async ({ page: browserPage }) => {
      await browserPage.goto(page.path);
      await browserPage.waitForLoadState("networkidle");

      const header = browserPage.locator(".qe-page__header");
      if (await header.isVisible()) {
        await expect(header).toHaveScreenshot(`${page.name}-header.png`);
      }
    });

    test(`${page.name} - sidebar region`, async ({ page: browserPage }) => {
      await browserPage.goto(page.path);
      await browserPage.waitForLoadState("networkidle");

      const sidebar = browserPage.locator(".qe-sidebar");
      if (await sidebar.isVisible()) {
        await expect(sidebar).toHaveScreenshot(`${page.name}-sidebar.png`);
      }
    });
  }
});

test.describe("Theme Features", () => {
  test("dark mode toggle", async ({ page }) => {
    await page.goto("/index.html");
    await page.waitForLoadState("networkidle");

    // Click contrast/dark mode button
    const contrastBtn = page.locator(".btn__contrast");
    if (await contrastBtn.isVisible()) {
      await contrastBtn.click();
      await page.waitForTimeout(300); // Wait for transition

      await expect(page).toHaveScreenshot("dark-mode.png", {
        fullPage: true,
      });
    }
  });

  test("code block styling", async ({ page }) => {
    await page.goto("/python_by_example.html");
    await page.waitForLoadState("networkidle");

    const codeBlock = page.locator(".highlight").first();
    if (await codeBlock.isVisible()) {
      await expect(codeBlock).toHaveScreenshot("code-block.png");
    }
  });

  test("f-string interpolation styling", async ({ page, browserName }, testInfo) => {
    // Skip on mobile - viewport too narrow to meaningfully test f-string styling
    test.skip(testInfo.project.name === "mobile-chrome", "F-string test only relevant on desktop");

    // Test that f-string placeholders render without italics
    // Uses names.html which contains: print(f'the identity of local x is {id(x)}')
    await page.goto("/names.html");
    await page.waitForLoadState("networkidle");

    // Find a code block containing .si (String.Interpol) tokens
    const fstringBlock = page.locator(".highlight:has(.si)").first();
    if (await fstringBlock.isVisible()) {
      await expect(fstringBlock).toHaveScreenshot("fstring-interpolation.png");
    }
  });

  test("math equation rendering", async ({ page }) => {
    await page.goto("/numpy.html");
    await page.waitForLoadState("networkidle");
    // Wait for MathJax to render
    await page.waitForTimeout(1000);

    const mathBlock = page.locator(".MathJax").first();
    if (await mathBlock.isVisible()) {
      // MathJax rendering can vary slightly between runs due to font loading
      // and rendering differences, so use a more lenient threshold
      await expect(mathBlock).toHaveScreenshot("math-equation.png", {
        maxDiffPixelRatio: 0.2,
      });
    }
  });

  test("toolbar visibility", async ({ page }) => {
    await page.goto("/index.html");
    await page.waitForLoadState("networkidle");

    const toolbar = page.locator(".qe-toolbar");
    await expect(toolbar).toHaveScreenshot("toolbar.png");
  });
});
