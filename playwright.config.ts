import { defineConfig, devices } from "@playwright/test";

/**
 * Playwright configuration for visual regression testing.
 *
 * Tests are run against a locally served build of the
 * quantecon-book-theme-fixtures site to verify theme styling hasn't
 * regressed. The fixtures repo is checked out as a sibling directory
 * (`fixtures/`) by CI; local users can clone it manually or use
 * `tox -e visual`, which clones it automatically.
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
      // Playwright's default 5000ms isn't enough to capture full-page
      // screenshots of long real-world fixtures (e.g. prob_matrix is ~1900
      // source lines). Bump generously — short captures finish in well
      // under a second, so this is just a ceiling for the long-page case.
      timeout: 30000,
    },
  },

  // Use platform-specific snapshot directories via SNAPSHOT_DIR env var
  // CI (ubuntu) uses default, tox on macOS sets SNAPSHOT_DIR=macos
  // Include project name to separate desktop/mobile snapshots
  snapshotPathTemplate: process.env.SNAPSHOT_DIR
    ? `{testDir}/{testFileDir}/${process.env.SNAPSHOT_DIR}/{projectName}/{arg}{ext}`
    : "{testDir}/{testFileDir}/__snapshots__/{projectName}/{arg}{ext}",

  // Web server to serve the built fixtures site.
  // CI sets SITE_PATH=fixtures/_build/html; local default matches the tox
  // clone path.
  webServer: {
    command: `python -m http.server 8000 --directory ${process.env.SITE_PATH || "fixtures/_build/html"}`,
    url: "http://localhost:8000",
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },
});
