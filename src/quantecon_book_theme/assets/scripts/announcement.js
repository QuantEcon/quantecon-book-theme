/**
 * Announcement Banner Module
 *
 * Renders a dismissible announcement bar at the top of the page. The bar is
 * server-rendered hidden and revealed here only for rows that survive two
 * checks, so the reader never sees a flash of a notice they already dismissed
 * or one that has expired:
 *
 *   - Dismissed: each row carries a content hash (`data-announcement-id`). The
 *     set of dismissed ids is stored in localStorage, so an edited message —
 *     which produces a new hash — re-appears even for readers who dismissed the
 *     old one. Dismissal persists across visits until the message changes.
 *   - Expired: an optional `data-announcement-expires` (YYYY-MM-DD) hides the
 *     row once the visitor's clock is past the end of that day, so a notice
 *     disappears on the date even if the site has not been rebuilt.
 *
 * The bar may hold more than one row; the logic is intentionally n-aware so
 * per-page announcements can be added additively later without changes here.
 */

const STORAGE_KEY = "qe-dismissed-announcements";
const MAX_REMEMBERED = 20;

function readDismissed() {
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    const parsed = raw ? JSON.parse(raw) : [];
    return Array.isArray(parsed) ? parsed : [];
  } catch (e) {
    // localStorage unavailable (e.g. private mode) or corrupt value.
    return [];
  }
}

function rememberDismissed(id) {
  try {
    const dismissed = readDismissed().filter((value) => value !== id);
    dismissed.push(id);
    // Cap the list so it can't grow unbounded over the site's lifetime.
    const trimmed = dismissed.slice(-MAX_REMEMBERED);
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(trimmed));
  } catch (e) {
    // Persisting is best-effort; dismissal still works for this page view.
  }
}

function isExpired(expires) {
  if (!expires) return false;
  // Parse YYYY-MM-DD into explicit local-time components (unambiguous across
  // engines, and not subject to the "date-only string is UTC" parsing rule).
  // Expire at the very end of that calendar day in the visitor's timezone.
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(expires.trim());
  if (!m) return false; // fail open on bad/unsupported format
  const endOfDay = new Date(+m[1], +m[2] - 1, +m[3], 23, 59, 59, 999);
  if (Number.isNaN(endOfDay.getTime())) return false;
  return new Date() > endOfDay;
}

export function initAnnouncement() {
  const bar = document.querySelector(".qe-announcement-bar");
  if (!bar) return;

  const dismissed = readDismissed();

  bar.querySelectorAll(".qe-announcement").forEach((row) => {
    const id = row.getAttribute("data-announcement-id");
    const expires = row.getAttribute("data-announcement-expires");

    // Drop rows the reader has dismissed or that have expired.
    if (dismissed.includes(id) || isExpired(expires)) {
      row.remove();
      return;
    }

    const closeButton = row.querySelector(".qe-announcement__close");
    if (closeButton) {
      closeButton.addEventListener("click", function () {
        rememberDismissed(id);
        row.remove();
        if (!bar.querySelector(".qe-announcement")) {
          bar.setAttribute("hidden", "");
        }
      });
    }
  });

  // Reveal the bar only if at least one row survived.
  if (bar.querySelector(".qe-announcement")) {
    bar.removeAttribute("hidden");
  } else {
    bar.remove();
  }
}
