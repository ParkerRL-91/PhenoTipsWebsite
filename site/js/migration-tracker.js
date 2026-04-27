/* PhenoTips migration tracker
   ----------------------------
   Loaded on every page during the WordPress → static cutover window.
   Detects pages that ARRIVED via a legacy URL (i.e., were 301-redirected
   from /our-story/, /blog/*, etc.) and logs the chain to the console.

   Optionally sends a beacon to a logging endpoint if MIGRATION_BEACON_URL
   is configured. Wire that to a real endpoint (Netlify Function / HubSpot
   custom event / Logflare) to capture which legacy URLs are still being
   hit in the wild.

   Remove or disable this script once 404 rate stabilizes (typically
   60-90 days after cutover). */

(function () {
  try {
    var ref = document.referrer;
    var here = window.location.pathname;
    var canonical = document.querySelector('link[rel="canonical"]');
    var canonicalHref = canonical ? canonical.getAttribute('href') : null;

    // Heuristic: if user came from an external phenotips.com URL,
    // they were likely 301-redirected. Log it.
    var fromLegacy = ref && /phenotips\.com/i.test(ref) && ref.indexOf(here) === -1;

    if (fromLegacy) {
      var info = {
        type: "migration-301-arrival",
        landed_on: here + window.location.search,
        canonical: canonicalHref,
        likely_from: ref,
        time: new Date().toISOString(),
      };
      console.info("[PhenoTips migration]", info);

      // Send a beacon if MIGRATION_BEACON_URL is set on window
      if (window.MIGRATION_BEACON_URL) {
        try {
          var blob = new Blob([JSON.stringify(info)], { type: "application/json" });
          navigator.sendBeacon(window.MIGRATION_BEACON_URL, blob);
        } catch (_) {}
      }
    }
  } catch (_) {}
})();
