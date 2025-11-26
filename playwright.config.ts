import { defineConfig, devices } from "@playwright/test";

/**
 * Playwright configuration for visual regression testing.
 *
 * Tests are run against a locally served build of lecture-python-programming.myst
 * to verify theme styling hasn't regressed.
 */
export default defineConfig({
  testDir: "./tests/visual",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [["html", { open: "never" }], ["list"]],

  // Shared settings for all projects
  use: {
    // Base URL for the locally served lecture site
    baseURL: process.env.BASE_URL || "http://localhost:8000",
    trace: "on-first-retry",
  },

  // Configure projects for different viewports
  projects: [
    {
      name: "desktop-chrome",
      use: {
        ...devices["Desktop Chrome"],
        viewport: { width: 1280, height: 720 },
      },
    },
    {
      name: "mobile-chrome",
      use: {
        ...devices["Pixel 5"],
      },
    },
  ],

  // Snapshot configuration
  expect: {
    toHaveScreenshot: {
      // Allow small pixel differences (anti-aliasing, font rendering)
      maxDiffPixelRatio: 0.01,
      // Threshold for individual pixel color difference
      threshold: 0.2,
    },
  },

  // Web server to serve the built lecture site
  webServer: {
    command: "python -m http.server 8000 --directory lecture-python-programming.myst/_build/html",
    url: "http://localhost:8000",
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },
});
