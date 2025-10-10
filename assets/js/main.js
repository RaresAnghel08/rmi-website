// Client-side markdown page loader
(function(){
  const navList = document.getElementById('nav-list');
  const contentEl = document.getElementById('content');

  function mdToHtml(md){
    // Very small markdown -> HTML converter for headings, paragraphs and links, lists, code blocks
    // This is intentionally minimal. For richer rendering, swap in a library like marked.js.
    const esc = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
    let html = md
      .replace(/(^|\n)###### (.*)/g, '$1<h6>$2</h6>')
      .replace(/(^|\n)##### (.*)/g, '$1<h5>$2</h5>')
      .replace(/(^|\n)#### (.*)/g, '$1<h4>$2</h4>')
      .replace(/(^|\n)### (.*)/g, '$1<h3>$2</h3>')
      .replace(/(^|\n)## (.*)/g, '$1<h2>$2</h2>')
      .replace(/(^|\n)# (.*)/g, '$1<h1>$2</h1>');

    // code blocks ```
    html = html.replace(/```([\s\S]*?)```/g, function(m,code){
      return '<pre><code>'+esc(code)+'</code></pre>';
    });

    // inline code `...`
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

    // unordered lists
    html = html.replace(/(^|\n)\s*[-\*+] (.+)(?=\n|$)/g, function(m, p1, item){
      return p1 + '<li>' + item + '</li>';
    });
    // wrap consecutive lis into ul
    html = html.replace(/(<li>[\s\S]*?<\/li>)(?:(\n)?<li>)/g, function(m){return m});
    html = html.replace(/((?:<li>[\s\S]*?<\/li>\s*)+)/g, function(m){
      if (m.indexOf('<li>')!==-1) return '<ul>'+m+'</ul>';
      return m;
    });

    // links [text](url)
    html = html.replace(/\[([^\]]+)\]\(([^\)]+)\)/g, '<a href="$2">$1</a>');

    // paragraphs: split by double newlines
    html = html.split(/\n\s*\n/).map(function(blk){
      if (/^<h|^<ul|^<pre|^<p|^<blockquote/.test(blk.trim())) return blk;
      return '<p>'+blk.replace(/\n/g,' ')+'</p>';
    }).join('\n');

    return html;
  }

  const rendered = document.getElementById('rendered');

  function loadPage(path, push){
    rendered.innerHTML = '<p>Loading...</p>';
    // clear any previous content

    // Load pre-generated HTML from pages/ and fail if missing
    const htmlPath = path.replace(/^content\//, 'pages/').replace(/\.md$/,'') + '.html';
    fetch(htmlPath).then(r=>{
      if(!r.ok) throw new Error('HTML not found: '+htmlPath+' ('+r.status+')');
      return r.text();
    }).then(htmlText=>{
      try{
        const doc = new DOMParser().parseFromString(htmlText, 'text/html');
        const main = doc.querySelector('main.content') || doc.body;
        rendered.innerHTML = main.innerHTML;
      }catch(e){
        rendered.innerHTML = htmlText;
      }
  if(push) history.pushState({path:path}, '');
    }).catch(err=>{
      rendered.innerHTML = '<p class="error">Page not found: '+err.message+'</p>';
    });
  }

  function buildGroupedNav(menu, pages){
    // menu: array of entries with identifiers and external links
    // pages: array of {path,title}
    navList.innerHTML = '';

    // build category map from menu identifiers
    const categories = {};
    menu.forEach(item=>{
      if(item.identifier){
        categories[item.identifier] = {meta: item, children: []};
      }
    });

    // place pages into categories by path
    pages.forEach(p=>{
      let placed = false;
      if(p.path.startsWith('content/organisation/')){ categories['organisation'] && categories['organisation'].children.push(p); placed = true; }
      else if(p.path.startsWith('content/contest/')){ categories['contest'] && categories['contest'].children.push(p); placed = true; }
      else { categories['root'] && categories['root'].children.push(p); }
    });

    // add external links from menu (those with url)
    menu.forEach(item=>{
      if(item.url && item.parent){
        const parent = categories[item.parent];
        if(parent){ parent.children.push({path: null, title: item.name, url: item.url}); }
      }
    });

    // sort categories by weight
    const ordered = Object.values(categories).sort((a,b)=> (a.meta.weight||0)-(b.meta.weight||0));

    ordered.forEach(cat=>{
      const header = document.createElement('h4');
      header.textContent = cat.meta.name;
      navList.appendChild(header);
      const ul = document.createElement('ul');
      ul.style.listStyle='none'; ul.style.padding='0 0 0 .5rem';
      (cat.children || []).forEach(child=>{
        const li = document.createElement('li');
        const a = document.createElement('a');
        if(child.url){
          a.href = child.url; a.target='_blank'; a.rel='noopener'; a.textContent = child.title;
          } else {
          // a.href = 'javascript:void(0)';
          a.dataset.path = child.path;
          a.textContent = child.title || (child.path||'');
          a.addEventListener('click', function(ev){ ev.preventDefault(); loadPage(this.dataset.path, true); navList.querySelectorAll('a').forEach(x=>x.classList.remove('active')); this.classList.add('active'); });
        }
        li.appendChild(a); ul.appendChild(li);
      });
      navList.appendChild(ul);
    });
  }

  // fetch both menu and content manifests
  Promise.all([fetch('menu.json').then(r=>r.json()), fetch('content_index.json').then(r=>r.json())])
    .then(([menu, manifest])=>{
      buildGroupedNav(menu, manifest);

      // load initial page from hash or first manifest entry
  const initial = (history.state && history.state.path && manifest.find(m=>m.path===history.state.path)) || manifest[0];
      if(initial) loadPage(initial.path, false);
      // mark active nav item if present
      const activeNode = navList.querySelector('a[data-path="'+(initial && initial.path || '')+'"]');
      if(activeNode){ navList.querySelectorAll('a').forEach(x=>x.classList.remove('active')); activeNode.classList.add('active'); }
    }).catch(err=>{
      contentEl.innerHTML = '<p class="error">Failed to load manifest(s): '+err.message+'</p>';
    });

  // handle back/forward
  window.addEventListener('popstate', function(e){
    const p = (e.state && e.state.path);
    if(p) {
      loadPage(p, false);
      // update active link if present
      const node = navList.querySelector('a[data-path="'+p+'"]');
      if(node){ navList.querySelectorAll('a').forEach(x=>x.classList.remove('active')); node.classList.add('active'); }
    }
  });
  // no raw preview toggle in this build
})();

