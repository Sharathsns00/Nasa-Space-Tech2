// static/app.js
function el(id){ return document.getElementById(id); }
function escapeHtml(s){ if(!s) return ""; return s.replace(/[&<>"']/g, m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m])); }

async function loadExperiments(){
  try{
    const res = await fetch('/api/experiments');
    const list = await res.json();
    const container = el('experiments');
    container.innerHTML = '';
    list.forEach(e=>{
      const d = document.createElement('div');
      d.className = 'exp';
      d.innerHTML = `<strong>${escapeHtml(e.title)}</strong><div class="muted">${escapeHtml(e.organism)} • ${escapeHtml(e.mission)} • ${escapeHtml(e.date)}</div><p>${escapeHtml(e.summary)}</p>`;
      container.appendChild(d);
    });
  }catch(err){ el('experiments').innerHTML = '<p class="error">Error loading experiments.</p>'; console.error(err); }
}

async function loadPapers(filter){
  try{
    const res = await fetch('/api/papers');
    const papers = await res.json();
    const list = el('papers-list');
    list.innerHTML = '';
    const q = (filter||'').toLowerCase();
    const filtered = papers.filter(p => {
      if(!q) return true;
      return p.title.toLowerCase().includes(q) || (p.tags && p.tags.join(' ').toLowerCase().includes(q));
    });
    if(filtered.length === 0) { list.innerHTML = '<p class="muted">No papers found.</p>'; return; }
    filtered.forEach(p=>{
      const div = document.createElement('div');
      div.className = 'paper';
      div.innerHTML = `<a href="${escapeHtml(p.link)}" target="_blank">${escapeHtml(p.title)}</a>
        <div class="tags">${(p.tags||[]).map(t=>`<span class="tag">${escapeHtml(t)}</span>`).join(' ')}</div>`;
      list.appendChild(div);
    });
  }catch(err){ el('papers-list').innerHTML = '<p class="error">Error loading papers.</p>'; console.error(err); }
}

async function loadGraph(){
  try{
    const res = await fetch('/api/graph');
    const payload = await res.json();
    // adapt nodes for vis
    const nodes = new vis.DataSet(payload.nodes.map(n=>{
      if(n.group === 'topic') n.color = {background:'#2b8cff', border:'#145fbd'};
      else n.color = {background:'#2ed1a6', border:'#0e7f55'};
      return n;
    }));
    const edges = new vis.DataSet(payload.edges);
    const container = el('network');
    const data = { nodes, edges };
    const options = {
      nodes: { font:{ color:'#fff' }, shape: 'dot', size:14 },
      edges: { color:'#aaa' },
      interaction: { hover:true },
      physics: { stabilization:false }
    };
    const network = new vis.Network(container, data, options);
    network.on('click', params=>{
      if(params.nodes && params.nodes.length){
        const node = nodes.get(params.nodes[0]);
        if(node && node.link) window.open(node.link, '_blank');
        else {
          // highlight connected nodes temporarily
          const connected = network.getConnectedNodes(node.id);
          nodes.forEach(n => nodes.update({id:n.id, hidden:true}));
          nodes.update({id: node.id, hidden:false});
          connected.forEach(cid => nodes.update({id: cid, hidden:false}));
          setTimeout(()=>{ nodes.forEach(n => nodes.update({id:n.id, hidden:false})); }, 3000);
        }
      }
    });
  }catch(err){ el('network').innerHTML = '<p class="error">Error loading graph.</p>'; console.error(err); }
}

async function askAI(){
  const q = el('user-question').value.trim();
  if(!q) return;
  el('ai-response').innerHTML = `<div class="muted">Thinking...</div>`;
  try{
    const res = await fetch('/api/ask', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ question: q })
    });
    const data = await res.json();
    let html = '';
    if(data.source === 'papers-list' && Array.isArray(data.answer)){
      html += '<strong>Matching papers:</strong><ul>';
      data.answer.forEach(p=> html += `<li><a href="${escapeHtml(p.link)}" target="_blank">${escapeHtml(p.title)}</a> <span class="tag">${(p.tags||[]).join(', ')}</span></li>`);
      html += '</ul>';
    } else if(data.source === 'local-paper' && data.link){
      html += `<strong>Paper found:</strong> <a href="${escapeHtml(data.link)}" target="_blank">${escapeHtml(data.answer)}</a>`;
    } else {
      html += `<div>${escapeHtml(typeof data.answer === 'string' ? data.answer : JSON.stringify(data.answer))}</div>`;
    }
    if(data.error) html += `<div class="error">Note: ${escapeHtml(data.error)}</div>`;
    html += `<div class="muted">Source: ${escapeHtml(data.source||'unknown')}</div>`;
    el('ai-response').innerHTML = html;
  }catch(err){
    el('ai-response').innerHTML = `<div class="error">Server error: ${escapeHtml(err.message||String(err))}</div>`;
  }
}

// wire events
document.addEventListener('DOMContentLoaded', ()=>{
  loadExperiments();
  loadPapers('');
  loadGraph();
  el('filterBtn').addEventListener('click', ()=> loadPapers(el('paper-filter').value));
  el('askBtn').addEventListener('click', askAI);
  el('user-question').addEventListener('keypress', (e)=>{ if(e.key==='Enter') askAI(); });
});
