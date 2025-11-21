(function(){
  // LocalPilot inline chat webview script
  const vscode = acquireVsCodeApi();
  let currentAssistantDiv = null;
  let inCode = false;
  let lastAssistantDiv = null;

  function log(){
    try { console.log.apply(console, arguments); } catch(_) {}
  }

  function byId(id){ return document.getElementById(id); }

  function appendUser(text){
    const c = byId('messages');
    const d = document.createElement('div');
    d.className = 'msg user';
    d.textContent = text;
    c.appendChild(d);
    addMsgActions(d, 'user');
    c.scrollTop = c.scrollHeight;
  }

  function beginAssistant(){
    const c = byId('messages');
    currentAssistantDiv = document.createElement('div');
    currentAssistantDiv.className = 'msg assistant';
    c.appendChild(currentAssistantDiv);
    lastAssistantDiv = currentAssistantDiv;
    c.scrollTop = c.scrollHeight;
  }

  function escapeHtml(s){
    return String(s)
      .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  }

  function convertMarkdownMinimal(md){
    // naive streaming codefence handling for ``` blocks
    const parts = String(md).split(/```/g);
    let out = '';
    for(let i=0;i<parts.length;i++){
      const seg = parts[i];
      if(i % 2 === 0){
        // normal text
        if(inCode){
          out += escapeHtml(seg);
        } else {
          out += escapeHtml(seg).replace(/\n/g,'<br/>');
        }
      } else {
        // toggle code block
        if(inCode){
          out += '</code></pre>';
          inCode = false;
        } else {
          out += '<pre><code>';
          inCode = true;
        }
      }
    }
    return out;
  }

  function streamMarkdown(md){
    if(!currentAssistantDiv){ beginAssistant(); }
    currentAssistantDiv.innerHTML += convertMarkdownMinimal(md);
    const c = byId('messages');
    c.scrollTop = c.scrollHeight;
  }

  function endAssistant(){
    if(lastAssistantDiv){
      addCopyButtonsForCode(lastAssistantDiv);
      addMsgActions(lastAssistantDiv, 'assistant');
    }
    currentAssistantDiv = null;
  }

  function send(){
    const t = byId('prompt');
    const v = (t && t.value) || '';
    if(!v.trim()) return;
    const hint = byId('hint'); if(hint){ hint.textContent = 'Sending…'; }
    appendUser(v);
    vscode.postMessage({ type: 'inlineChat', text: v });
    if(t) t.value='';
    log('[LocalPilot Chat] send clicked:', v);
  }

  function transfer(){
    const t = byId('prompt');
    const title = ((t && t.value) || '').trim() || 'Draft plan from Chat';
    vscode.postMessage({ type: 'transfer', title });
    const hint = byId('hint'); if(hint){ hint.textContent = 'Transferring…'; }
    log('[LocalPilot Chat] transfer clicked:', title);
  }

  function clearMsgs(){ const c = byId('messages'); if(c) c.innerHTML=''; }
  function refresh(){ vscode.postMessage({ type: 'refresh' }); }

  function renderRecent(items){
    const r = byId('recent'); if(!r) return;
    if(!items || !items.length){ r.innerHTML = ''; return; }
    r.innerHTML = items.map(t => `<span class="item" data-v="${encodeURIComponent(t)}">${escapeHtml(t)}</span>`).join('');
    for(const el of r.querySelectorAll('.item')){
      el.addEventListener('click', ()=>{
        const v = decodeURIComponent(el.getAttribute('data-v') || '');
        const t = byId('prompt'); if(t){ t.value = v; t.focus(); }
      });
    }
  }

  function updateModelBadge(model){
    const el = byId('model-badge');
    if(el){ el.textContent = 'model: ' + String(model || 'local'); }
  }

  function copyLastAssistant(){
    const blocks = Array.from(document.querySelectorAll('.msg.assistant'));
    if(!blocks.length) return;
    const last = blocks[blocks.length - 1];
    const text = last.textContent || '';
    vscode.postMessage({ type: 'copy', text });
  }

  function addCopyButtonsForCode(container){
    const pres = Array.from(container.querySelectorAll('pre'));
    for(const pre of pres){
      const btn = document.createElement('button');
      btn.textContent = 'Copy code';
      btn.addEventListener('click', ()=>{
        const code = pre.querySelector('code');
        const text = (code && code.innerText) || pre.innerText || '';
        vscode.postMessage({ type: 'copy', text });
      });
      pre.parentNode && pre.parentNode.insertBefore(btn, pre);
    }
  }

  function addMsgActions(div, kind){
    const bar = document.createElement('div');
    bar.className = 'actions';
    if(kind === 'user'){
      const resend = document.createElement('button');
      resend.textContent = 'Resend';
      resend.addEventListener('click', ()=>{
        const text = div.textContent || '';
        vscode.postMessage({ type: 'inlineChat', text });
      });
      const del = document.createElement('button');
      del.textContent = 'Delete';
      del.addEventListener('click', ()=>{ div.remove(); });
      bar.appendChild(resend);
      bar.appendChild(del);
    } else {
      const copy = document.createElement('button');
      copy.textContent = 'Copy';
      copy.addEventListener('click', ()=>{
        const text = div.textContent || '';
        vscode.postMessage({ type: 'copy', text });
      });
      const del = document.createElement('button');
      del.textContent = 'Delete';
      del.addEventListener('click', ()=>{ div.remove(); });
      bar.appendChild(copy);
      bar.appendChild(del);
    }
    div.appendChild(document.createElement('br'));
    div.appendChild(bar);
  }

  window.addEventListener('message', (e)=>{
    const msg = e.data;
    if(msg && msg.type === 'beginAssistant'){ beginAssistant(); }
    if(msg && msg.type === 'stream' && typeof msg.markdown==='string'){ streamMarkdown(msg.markdown); }
    if(msg && msg.type === 'endAssistant'){ endAssistant(); }
    if(msg && msg.type === 'action' && msg.title){
      if(!currentAssistantDiv){ beginAssistant(); }
      const btn = document.createElement('button');
      btn.textContent = msg.title;
      btn.onclick = ()=>{ vscode.postMessage({ type: 'transfer', title: 'Draft plan from Chat' }); };
      currentAssistantDiv.appendChild(document.createElement('br'));
      currentAssistantDiv.appendChild(btn);
    }
    if(msg && msg.type === 'state'){
      const hint = byId('hint');
      if(hint){ hint.textContent = 'Ready (plans: ' + (msg.plans ?? 0) + ')'; }
      renderRecent(msg.recent || []);
      updateModelBadge(msg.model || 'local');
      log('[LocalPilot Chat] state message:', msg);
    }
  });

  function init(){
    refresh();
    const t = byId('prompt');
    if(t && t.focus){ t.focus(); }
    if(t){
      t.addEventListener('keydown', (e)=>{
        if(e.key==='Enter' && !e.shiftKey){ e.preventDefault(); send(); }
      });
    }
    const hint = byId('hint'); if(hint){ hint.textContent = 'Ready'; }
    const btnSend = byId('btn-send');
    const btnStop = byId('btn-stop');
    const btnRegen = byId('btn-regen');
    const btnCopy = byId('btn-copy');
    const btnTransfer = byId('btn-transfer');
    const btnClear = byId('btn-clear');
    if(btnSend){ btnSend.addEventListener('click', ()=> send()); }
    if(btnStop){ btnStop.addEventListener('click', ()=> vscode.postMessage({ type: 'stop' })); }
    if(btnRegen){ btnRegen.addEventListener('click', ()=> vscode.postMessage({ type: 'regen' })); }
    if(btnCopy){ btnCopy.addEventListener('click', ()=> copyLastAssistant()); }
    if(btnTransfer){ btnTransfer.addEventListener('click', ()=> transfer()); }
    if(btnClear){ btnClear.addEventListener('click', ()=> clearMsgs()); }

    const modelBadge = byId('model-badge');
    if(modelBadge){ modelBadge.style.cursor = 'pointer'; modelBadge.title = 'Click to switch model'; modelBadge.addEventListener('click',()=> vscode.postMessage({ type: 'pickModel' })); }
    log('[LocalPilot Chat] init complete');
  }

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
