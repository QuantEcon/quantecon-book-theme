/**
 * QuantEcon Book Theme - Main JavaScript Entry Point
 *
 * This is the main entry point for all theme JavaScript.
 * Individual features are organized into separate modules for maintainability.
 */

// Import styles
import "../styles/index.scss";

// Import feature modules
import { initThemeSettings, initFontSize } from "./theme-settings.js";
import { initSidebar } from "./sidebar.js";
import { initSearch } from "./search.js";
import { initFullscreen, initBackToTop } from "./navigation.js";
import { initCollapsibleCode, initTableContainers } from "./code-blocks.js";
import { initPopups, initLauncherSettings } from "./popups.js";
import { initPageHeader, initChangelog } from "./page-header.js";
import { initStderrWarnings } from "./stderr-warnings.js";

document.addEventListener("DOMContentLoaded", function () {
  // Load feather icon set
  feather.replace();

  // Initialize theme settings (contrast/dark mode, font size)
  initThemeSettings();
  initFontSize();

  // Initialize navigation components
  initSidebar();
  initSearch();
  initFullscreen();
  initBackToTop();

  // Initialize content features
  initCollapsibleCode();
  initTableContainers();

  // Initialize popups and modals
  initPopups();
  initLauncherSettings();

  // Initialize page header features
  initPageHeader();
  initChangelog();

  // Initialize stderr warnings
  initStderrWarnings();
});
