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
  reporter: process.env.CI
    ? [
        ["html", { open: "never" }],
        ["json", { outputFile: "playwright-report/results.json" }],
        ["list"],
      ]
    : [["html", { open: "never" }], ["list"]],

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

  // Use platform-specific snapshot directories via SNAPSHOT_DIR env var
  // CI (ubuntu) uses default, tox on macOS sets SNAPSHOT_DIR=macos
  // Include project name to separate desktop/mobile snapshots
  snapshotPathTemplate: process.env.SNAPSHOT_DIR
    ? `{testDir}/{testFileDir}/${process.env.SNAPSHOT_DIR}/{projectName}/{arg}{ext}`
    : "{testDir}/{testFileDir}/__snapshots__/{projectName}/{arg}{ext}",

  // Web server to serve the built lecture site
  // Path varies: CI uses _build/html, tox uses lectures/_build/html
  webServer: {
    command: `python -m http.server 8000 --directory ${process.env.SITE_PATH || "lecture-python-programming.myst/lectures/_build/html"}`,
    url: "http://localhost:8000",
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },
});
