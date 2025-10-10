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
        rendered.innerHTML = main.innerHTML;
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
          a.href = 'javascript:void(0)';
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

  // Mobile nav toggle
  const toggleBtn = document.getElementById('nav-toggle');
  function toggleNav(force){
    const nav = document.getElementById('site-nav');
    const expanded = typeof force === 'boolean' ? force : !nav.classList.contains('open');
    if(expanded){
      nav.classList.add('open');
      toggleBtn.setAttribute('aria-expanded','true');
    } else {
      nav.classList.remove('open');
      toggleBtn.setAttribute('aria-expanded','false');
    }
  }
  if(toggleBtn){
    toggleBtn.addEventListener('click', ()=> toggleNav());
  }

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
