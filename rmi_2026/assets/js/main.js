// Site behaviour: mobile nav, results-table style overrides, scroll animations.
// Pages are static HTML (one file per route, see scripts/build_site.py); nothing is fetched here.
(function(){
  // Mobile nav toggle
  const toggleBtn = document.getElementById('nav-toggle');
  function toggleNav(force){
    const nav = document.getElementById('site-nav');
    if(!nav || !toggleBtn) return;
    const expanded = typeof force === 'boolean' ? force : !nav.classList.contains('open');
    const body = document.body;
    const existingOverlay = document.getElementById('nav-overlay');
    if(expanded){
      nav.classList.add('open');
      toggleBtn.setAttribute('aria-expanded','true');
      body.classList.add('nav-open');
      if(!existingOverlay){
        const overlay = document.createElement('div');
        overlay.id = 'nav-overlay';
        overlay.className = 'nav-overlay';
        overlay.addEventListener('click', ()=> toggleNav(false));
        document.body.appendChild(overlay);
        // allow CSS transitions
        requestAnimationFrame(()=> overlay.classList.add('visible'));
      } else {
        existingOverlay.classList.add('visible');
      }
    } else {
      nav.classList.remove('open');
      toggleBtn.setAttribute('aria-expanded','false');
      body.classList.remove('nav-open');
      if(existingOverlay){
        existingOverlay.classList.remove('visible');
        setTimeout(()=>{
          if(existingOverlay.parentNode) existingOverlay.parentNode.removeChild(existingOverlay);
        }, 250);
      }
    }
  }
  if(toggleBtn){
    toggleBtn.addEventListener('click', ()=> toggleNav());
  }

  // Keep the results table clean (no theme header/bg/striping) but DO NOT override medal name colors.
  // Appended to <body> so it comes after the page's own inline <style> and wins on equal specificity.
  function applyResultsOverrides(){
    if(!document.querySelector('.results-table')) return;
    const overrideCSS = `
/* Clean results table overrides - keep medal name colors intact */
.results-table{width:100%;border-collapse:collapse;background:transparent!important;border-radius:0!important;box-shadow:none!important}

/* Header: clean design, no cell borders, subtle readable text */
.results-table thead th{
  background:transparent!important;
  /* keep header visually clean but keep a single bottom rule */
  border:none!important;
  border-bottom: 1px solid rgba(0,0,0,0.12) !important;
  padding:.6rem .5rem!important;
  color:rgba(0,0,0,0.85)!important;
  font-weight:600!important;
}

/* First data row: remove top borders so the table reads as a single clean block */
.results-table tbody tr:first-child td{
  border-top:none!important;
}

/* Cell padding and default dividing lines (light mode) */
.results-table th,.results-table td{padding:.5rem .65rem;text-align:left;background:transparent!important}
.results-table tbody tr:hover{background:transparent!important}
.results-table tbody tr:last-child td{border-bottom:none!important}

/* Re-assert medal name colors so they're not overridden by theme rules */
.name-gold{color:#bb9413!important; font-weight:600!important}
.name-silver{
  color: #6f6f72 !important;
  font-weight:700 !important;
  background: rgba(128,127,129,0.08) !important;
  padding: 0 .22rem !important;
  border-radius: 0.28rem !important;
  text-shadow: 0 1px 0 rgba(255,255,255,0.03) !important;
}
.name-bronze{color:#804A00!important; font-weight:600!important}
`;
    const el = document.createElement('style');
    el.id = 'rmi-results-override';
    el.textContent = overrideCSS;
    document.body.appendChild(el);
  }

  // Scroll fade-in animation for team cards
  function initScrollAnimation() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('fade-in-visible');
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    document.querySelectorAll('.team-card').forEach(card => {
      card.classList.add('fade-in');
      observer.observe(card);
    });
  }

  function init(){
    applyResultsOverrides();
    initScrollAnimation();
  }
  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
