// PhenoTips Website — Main JS
// Handles: nav scroll, mobile menu, tabs, ROI calculator

document.addEventListener('DOMContentLoaded', () => {
  initNav();
  initTabs();
  initROI();
  initReveal();
  if (window.lucide) lucide.createIcons();
});

// ============================================================
// SCROLL REVEAL — fade-in-up for elements with .reveal
// ============================================================

function initReveal() {
  const targets = document.querySelectorAll('.reveal');
  if (!targets.length) return;

  if (!('IntersectionObserver' in window)) {
    targets.forEach(el => el.classList.add('in'));
    return;
  }

  const obs = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in');
        obs.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  targets.forEach(el => obs.observe(el));
}

// ============================================================
// NAV — frosted glass on scroll + mobile menu
// ============================================================

function initNav() {
  const nav = document.querySelector('.nav');
  if (!nav) return;

  const observer = new IntersectionObserver(
    ([entry]) => nav.classList.toggle('scrolled', !entry.isIntersecting),
    { rootMargin: '-1px 0px 0px 0px', threshold: 0 }
  );

  const sentinel = document.createElement('div');
  sentinel.style.cssText = 'position:absolute;top:0;left:0;height:1px;width:1px;pointer-events:none;';
  document.body.prepend(sentinel);
  observer.observe(sentinel);

  const hamburger = document.querySelector('.nav__hamburger');
  const mobileMenu = document.querySelector('.nav__mobile-menu');
  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', () => {
      const open = mobileMenu.classList.toggle('open');
      hamburger.setAttribute('aria-expanded', String(open));
      document.body.style.overflow = open ? 'hidden' : '';
    });

    mobileMenu.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        mobileMenu.classList.remove('open');
        document.body.style.overflow = '';
      });
    });
  }

  // Mark active link
  const path = window.location.pathname.replace(/\/$/, '');
  document.querySelectorAll('.nav__link').forEach(link => {
    const href = link.getAttribute('href')?.replace(/\/$/, '') ?? '';
    if (href && path.endsWith(href)) link.classList.add('active');
  });
}

// ============================================================
// TABS — platform feature tabs
// ============================================================

function initTabs() {
  document.querySelectorAll('.feature-tabs').forEach(tabs => {
    const buttons = tabs.querySelectorAll('.tab-btn');
    const panels = tabs.querySelectorAll('.tab-panel');

    buttons.forEach((btn, i) => {
      btn.addEventListener('click', () => {
        buttons.forEach(b => b.classList.remove('active'));
        panels.forEach(p => p.classList.remove('active'));
        btn.classList.add('active');
        panels[i]?.classList.add('active');
      });
    });

    // Activate first tab
    buttons[0]?.classList.add('active');
    panels[0]?.classList.add('active');
  });
}

// ============================================================
// ROI CALCULATOR
// ============================================================

function initROI() {
  const calc = document.getElementById('roi-calculator');
  if (!calc) return;

  const inputs = {
    patients:   document.getElementById('roi-patients'),
    timeNew:    document.getElementById('roi-time-new'),
    riskCount:  document.getElementById('roi-risk-count'),
    timeRisk:   document.getElementById('roi-time-risk'),
    rareCases:  document.getElementById('roi-rare-cases'),
    testCost:   document.getElementById('roi-test-cost'),
  };

  const displays = {
    patients:   document.getElementById('val-patients'),
    timeNew:    document.getElementById('val-time-new'),
    riskCount:  document.getElementById('val-risk-count'),
    timeRisk:   document.getElementById('val-time-risk'),
    rareCases:  document.getElementById('val-rare-cases'),
    testCost:   document.getElementById('val-test-cost'),
  };

  const outputs = {
    hoursYear:      document.getElementById('out-hours-year'),
    addedPatients:  document.getElementById('out-added-patients'),
    staffSavings:   document.getElementById('out-staff-savings'),
    waste:          document.getElementById('out-waste'),
    odyssey:        document.getElementById('out-odyssey'),
    rareCasesEcho:  document.getElementById('out-rare-cases'),
    total:          document.getElementById('out-total'),
  };

  // --- Model constants (grounded in published PhenoTips outcomes + clinical literature)
  const EFFICIENCY_GAIN      = 0.50;   // 50% reduction in encounter + risk assessment time
  const STAFF_HOURLY_RATE    = 85;     // $ loaded rate for genetic counselor
  const DUPLICATE_TEST_RATE  = 0.15;   // 15% reduction in duplicate / wasted tests
  const ODYSSEY_VALUE        = 8000;   // $ downstream savings per rare disease case accelerated

  function fmt(n) { return Number(n).toLocaleString(); }
  function money(n) { return '$' + Math.round(n).toLocaleString(); }

  function updateDisplay(inputEl, displayEl) {
    if (!inputEl || !displayEl) return;
    displayEl.textContent = Number(inputEl.value).toLocaleString();
  }

  function calculate() {
    if (!inputs.patients) return;

    const patients  = +inputs.patients.value  || 0;
    const timeNew   = +inputs.timeNew.value   || 0;
    const riskCount = +inputs.riskCount.value || 0;
    const timeRisk  = +inputs.timeRisk.value  || 0;
    const rareCases = +inputs.rareCases.value || 0;
    const testCost  = +inputs.testCost.value  || 0;

    // ---- Stream 1: Reclaimed clinical capacity ----
    const hoursNewMonth  = (patients  * EFFICIENCY_GAIN * timeNew)  / 60;
    const hoursRiskMonth = (riskCount * EFFICIENCY_GAIN * timeRisk) / 60;
    const hoursPerYear   = Math.round((hoursNewMonth + hoursRiskMonth) * 12);
    const staffSavings   = hoursPerYear * STAFF_HOURLY_RATE;
    // Additional patient visits the reclaimed hours can support
    const addedPatients  = timeNew > 0 ? Math.floor((hoursPerYear * 60) / timeNew) : 0;

    // ---- Stream 2: Reduced diagnostic waste ----
    // Approximates total tests ordered per year from risk assessments + rare cases + a share of new patients
    const testsPerYear   = (riskCount * 12) + rareCases + (patients * 12 * 0.3);
    const wasteSavings   = Math.round(testsPerYear * DUPLICATE_TEST_RATE * testCost);

    // ---- Stream 3: Shortened diagnostic odyssey ----
    const odyssaySavings = rareCases * ODYSSEY_VALUE;

    // ---- Total ----
    const totalValue = staffSavings + wasteSavings + odyssaySavings;

    if (outputs.hoursYear)     outputs.hoursYear.textContent     = fmt(hoursPerYear);
    if (outputs.addedPatients) outputs.addedPatients.textContent = fmt(addedPatients);
    if (outputs.staffSavings)  outputs.staffSavings.textContent  = money(staffSavings);
    if (outputs.waste)         outputs.waste.textContent         = money(wasteSavings);
    if (outputs.odyssey)       outputs.odyssey.textContent       = money(odyssaySavings);
    if (outputs.rareCasesEcho) outputs.rareCasesEcho.textContent = fmt(rareCases);
    if (outputs.total)         outputs.total.textContent         = money(totalValue);
  }

  Object.entries(inputs).forEach(([key, el]) => {
    if (!el) return;
    el.addEventListener('input', () => {
      updateDisplay(el, displays[key]);
      calculate();
    });
    updateDisplay(el, displays[key]);
  });

  calculate();
}

// ============================================================
// SMOOTH SCROLL for anchor links
// ============================================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', e => {
    const target = document.querySelector(anchor.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});
