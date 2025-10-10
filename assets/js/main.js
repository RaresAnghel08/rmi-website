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
      if(push) history.pushState({path:path},'', '#'+encodeURIComponent(path));
    }).catch(err=>{
      rendered.innerHTML = '<p class="error">Page not found: '+err.message+'</p>';
    });
  }

  function buildNav(manifest){
    navList.innerHTML = '';
    manifest.forEach(item=>{
      const li = document.createElement('li');
      const a = document.createElement('a');
      // progressive links: keep href as hash for fallback but intercept clicks to load into center
      const encoded = encodeURIComponent(item.path || '');
      a.href = '#'+encoded;
      a.dataset.path = item.path;
      a.textContent = item.title || item.path.replace(/^content\//,'');
      a.addEventListener('click', function(ev){
        ev.preventDefault();
        const p = this.dataset.path;
        // load into center
        loadPage(p, true);
        // update active class
        navList.querySelectorAll('a').forEach(x=>x.classList.remove('active'));
        this.classList.add('active');
      });
      li.appendChild(a);
      navList.appendChild(li);
    });
  }

  // fetch manifest
  fetch('content_index.json').then(r=>r.json()).then(manifest=>{
    buildNav(manifest);

    // load initial page from hash or first manifest entry
    const hash = decodeURIComponent(location.hash.slice(1));
    const initial = manifest.find(m=>m.path===hash) || manifest[0];
    if(initial) loadPage(initial.path, false);
    // mark active nav item if present
    const activeNode = navList.querySelector('a[data-path="'+(initial && initial.path || '')+'"]');
    if(activeNode){ navList.querySelectorAll('a').forEach(x=>x.classList.remove('active')); activeNode.classList.add('active'); }
  }).catch(err=>{
    contentEl.innerHTML = '<p class="error">Failed to load manifest: '+err.message+'</p>';
  });

  // handle back/forward
  window.addEventListener('popstate', function(e){
    const p = (e.state && e.state.path) || decodeURIComponent(location.hash.slice(1));
    if(p) {
      loadPage(p, false);
      // update active link if present
      const node = navList.querySelector('a[data-path="'+p+'"]');
      if(node){ navList.querySelectorAll('a').forEach(x=>x.classList.remove('active')); node.classList.add('active'); }
    }
  });
  // no raw preview toggle in this build
})();

