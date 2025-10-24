// Client-side static HTML page loader (menu-driven)
(function(){
  const navList = document.getElementById('nav-list');
  const rendered = document.getElementById('rendered');

  function fetchAndRender(path){
    if(!path){ rendered.innerHTML = '<p class="error">No page specified</p>'; return; }
    rendered.innerHTML = '<p>Loading...</p>';
    fetch(path).then(r=>{
      if(!r.ok) throw new Error('Not found: '+path+' ('+r.status+')');
      return r.text();
    }).then(text=>{
      try{
        const doc = new DOMParser().parseFromString(text, 'text/html');
        const main = doc.querySelector('main.content') || doc.body;
        
        // Inject stylesheet links from the fetched page into the document head (avoid duplicates)
        const links = doc.querySelectorAll('link[rel="stylesheet"]');
        links.forEach(link => {
          const href = link.getAttribute('href');
          if (!href) return;
          const exists = Array.from(document.head.querySelectorAll('link[rel="stylesheet"]')).some(l => l.getAttribute('href') === href);
          if (!exists) {
            const newLink = document.createElement('link');
            newLink.rel = 'stylesheet';
            newLink.href = href;
            document.head.appendChild(newLink);
          }
        });

        // Extract inline <style> blocks from the loaded page so component styles apply (they'll be inserted into the rendered container)
        const styles = doc.querySelectorAll('style');
        let styleHTML = '';
        styles.forEach(style => { styleHTML += style.outerHTML; });

        // Put inline page styles followed by the page content into the rendered container
        rendered.innerHTML = styleHTML + main.innerHTML;

        // Inject a small override stylesheet to keep the results table clean (no theme header/bg/striping),
        // but DO NOT override medal name colors; place this AFTER the page styles so it takes precedence.
        const overrideId = 'rmi-results-override';
        let overrideEl = document.getElementById(overrideId);
        const overrideCSS = `
/* Clean results table overrides - keep medal name colors intact */
.results-table{width:100%;border-collapse:collapse;background:transparent!important;border-radius:0!important;box-shadow:none!important}

/* Header: clean design, no cell borders, subtle readable text */
.results-table thead th{
  background:transparent!important;
  border:none!important;
  border-bottom:none!important;
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

/* Dark mode: unify row dividing lines and make header text light for contrast */
.theme-dark .results-table th,
.theme-dark .results-table td {
  border-bottom: 1px solid rgba(255,255,255,0.06) !important;
}
.theme-dark .results-table thead th {
  color: rgba(255,255,255,0.92) !important;
}

/* Re-assert medal name colors so they're not overridden by theme rules */
.name-gold{color:#bb9413!important}
.name-silver{color:#807f81!important}
.name-bronze{color:#804A00!important}
`;
        if (!overrideEl) {
          overrideEl = document.createElement('style');
          overrideEl.id = overrideId;
        }
        // append to body so it appears after any inline page <style> and wins on equal specificity
        overrideEl.textContent = overrideCSS;
        // remove existing and re-append to ensure ordering
        if (overrideEl.parentNode) overrideEl.parentNode.removeChild(overrideEl);
        document.body.appendChild(overrideEl);
      }catch(e){ rendered.innerHTML = text; }
    }).catch(err=>{
      rendered.innerHTML = '<p class="error">Error loading page: '+err.message+'</p>';
    });
  }

  function buildNav(menu){
    navList.innerHTML = '';

    // menu is expected to be an array of category objects with {name, items: [{title,path|url}]}
    menu.sort((a,b)=> (a.weight||0) - (b.weight||0));
    menu.forEach(cat=>{
      const h = document.createElement('h4');
      h.textContent = cat.name;
      navList.appendChild(h);

      const ul = document.createElement('ul');
      ul.style.listStyle = 'none';
      ul.style.padding = '0 0 0 .5rem';

      (cat.items||[]).forEach(item=>{
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.textContent = item.title;
        if(item.url){
          a.href = item.url; a.target = '_blank'; a.rel = 'noopener';
          a.addEventListener('click', ()=>{
            // if mobile nav open, close it
            const nav = document.getElementById('site-nav');
            if(nav.classList.contains('open')) toggleNav(false);
          });
        } else if(item.path){
          a.dataset.path = item.path;
          a.addEventListener('click', function(ev){
            ev.preventDefault();
            // load page but do not change the browser URL
            fetchAndRender(this.dataset.path);
            navList.querySelectorAll('a').forEach(x=>x.classList.remove('active'));
            this.classList.add('active');
            // close mobile nav after selection
            const nav = document.getElementById('site-nav');
            if(nav.classList.contains('open')) toggleNav(false);
          });
        } else {
          a.classList.add('inactive');
        }
        li.appendChild(a);
        ul.appendChild(li);
      });
      navList.appendChild(ul);
    });
  }

  // Mobile nav toggle (create if missing so standalone pages also get it)
  let toggleBtn = document.getElementById('nav-toggle');
  if(!toggleBtn){
    toggleBtn = document.createElement('button');
    toggleBtn.id = 'nav-toggle';
    toggleBtn.className = 'nav-toggle';
    toggleBtn.setAttribute('aria-controls','site-nav');
    toggleBtn.setAttribute('aria-expanded','false');
    toggleBtn.type = 'button';
    toggleBtn.textContent = '☰';
    // insert near the top of the body for consistent positioning
    document.body.appendChild(toggleBtn);
  }
  function toggleNav(force){
    const nav = document.getElementById('site-nav');
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

  // Theme toggle: creates a small button to switch light/dark mode and persists choice
  function createThemeToggle(){
    const btn = document.createElement('button');
    btn.className = 'theme-toggle';
    btn.type = 'button';
    btn.title = 'Toggle theme';
    btn.innerHTML = '<span class="icon">🌙</span>';
    btn.addEventListener('click', ()=>{
      const isDark = document.body.classList.toggle('theme-dark');
      localStorage.setItem('site-theme-dark', isDark ? '1' : '0');
      btn.innerHTML = isDark ? '<span class="icon">☀️</span>' : '<span class="icon">🌙</span>';
    });
    document.body.appendChild(btn);
    // initialize from preference
    const pref = localStorage.getItem('site-theme-dark');
    if(pref === '1'){
      document.body.classList.add('theme-dark');
      btn.innerHTML = '<span class="icon">☀️</span>';
    }
  }
  createThemeToggle();

  // Load menu.json and initialize
  fetch('menu.json').then(r=>r.json()).then(menu=>{
    buildNav(menu);
    // load first available page (first item with a path)
    for(const cat of menu){
      if(cat.items){
        const first = cat.items.find(it=>it.path);
        if(first){
          fetchAndRender(first.path);
          // mark active link
          const node = navList.querySelector('a[data-path="'+first.path+'"]');
          if(node) node.classList.add('active');
          break;
        }
      }
    }
  }).catch(err=>{
    rendered.innerHTML = '<p class="error">Failed to load menu.json: '+err.message+'</p>';
  });

})();
