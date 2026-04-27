/* Netlify Function: log-404
 * --------------------------
 * Receives migration-tracker beacons (legacy URL hits) and logs them.
 *
 * The browser-side migration-tracker.js sends a JSON beacon to this
 * endpoint. Each beacon includes:
 *   { type, landed_on, canonical, likely_from, time }
 *
 * This function:
 *   1. Logs the event to the Netlify function log (visible in dashboard).
 *   2. Optionally forwards to a HubSpot custom event if HUBSPOT_PORTAL_ID
 *      and HUBSPOT_BEACON_TOKEN env vars are set.
 *
 * Set up:
 *   In Netlify dashboard → Site settings → Environment variables, add:
 *     HUBSPOT_PORTAL_ID    = <your portal id>          (optional)
 *     HUBSPOT_BEACON_TOKEN = <a private access token>  (optional)
 *
 * Once deployed, this is reachable at:
 *   https://<your-site>/.netlify/functions/log-404
 *
 * The migration-tracker.js will set window.MIGRATION_BEACON_URL via the
 * inline <script> in main.js, so beacons fire automatically.
 */

exports.handler = async (event) => {
  // CORS preflight
  if (event.httpMethod === "OPTIONS") {
    return {
      statusCode: 200,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Max-Age": "86400",
      },
    };
  }

  if (event.httpMethod !== "POST") {
    return { statusCode: 405, body: "Method not allowed" };
  }

  let payload;
  try {
    payload = JSON.parse(event.body || "{}");
  } catch (e) {
    return { statusCode: 400, body: "Invalid JSON" };
  }

  // Stamp with server-side context
  payload.client_ip = event.headers["x-forwarded-for"] || "(unknown)";
  payload.country   = event.headers["x-country"] || "(unknown)";

  // Always log to the function log
  console.log("[migration-beacon]", JSON.stringify(payload));

  // Optional: forward to HubSpot Custom Events API
  const portalId = process.env.HUBSPOT_PORTAL_ID;
  const token    = process.env.HUBSPOT_BEACON_TOKEN;
  if (portalId && token && payload.landed_on) {
    try {
      await fetch("https://api.hubapi.com/events/v3/send", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          eventName:  "pe" + portalId + "_migration_301_arrival",
          properties: {
            landed_on:   payload.landed_on,
            canonical:   payload.canonical,
            likely_from: payload.likely_from,
          },
        }),
      });
    } catch (e) {
      console.warn("[migration-beacon] HubSpot forward failed:", e.message);
    }
  }

  return {
    statusCode: 204,
    headers: { "Access-Control-Allow-Origin": "*" },
    body: "",
  };
};
