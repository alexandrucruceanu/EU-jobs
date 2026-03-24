/**
 * shared.js - Common logic for EU Job Market Visualizer
 * Includes cookie consent and randomized footer quotes.
 */

let currentQuoteIndex = -1;

function initCookiePopup() {
  if (localStorage.getItem("cookie_consent") === "true") return;

  const banner = document.createElement("div");
  banner.id = "cookie-banner";
  banner.innerHTML = `
    <div class="cookie-content">
      <p>We use cookies to ensure you get the best experience on our website. No personal data is sold to robots (yet).</p>
      <button id="accept-cookies">Accept</button>
    </div>
  `;
  document.body.appendChild(banner);

  document.getElementById("accept-cookies").addEventListener("click", () => {
    localStorage.setItem("cookie_consent", "true");
    banner.classList.add("hidden");
    setTimeout(() => banner.remove(), 400);
  });
}

function updateFunnyFooter() {
  const footerQuoteEl = document.getElementById("footer-quote");
  if (!footerQuoteEl) return;
  
  // Pick index once per session/page-load if not set
  if (currentQuoteIndex === -1) {
    currentQuoteIndex = Math.floor(Math.random() * 15) + 1;
  }
  
  const key = "quote_" + currentQuoteIndex;
  // Use translation if available, otherwise fallback to a generic placeholder or wait
  if (window.__i18n && window.__i18n[key]) {
    footerQuoteEl.textContent = `"${window.__i18n[key]}"`;
  }
}

// Expose to global scope for i18n hooks
window.updateFunnyFooter = updateFunnyFooter;

// Initialize when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  initCookiePopup();
  updateFunnyFooter();
});
