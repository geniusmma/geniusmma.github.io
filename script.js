'use strict';
(() => {
  const menu = document.querySelector('.menu-button');
  const nav = document.querySelector('.main-nav');
  function closeMenu() { if (!menu || !nav) return; menu.setAttribute('aria-expanded','false'); menu.textContent='Menu'; nav.classList.remove('is-open'); }
  menu?.addEventListener('click', () => { const open=menu.getAttribute('aria-expanded')!=='true'; menu.setAttribute('aria-expanded',String(open)); menu.textContent=open?'Close':'Menu'; nav.classList.toggle('is-open',open); });
  nav?.querySelectorAll('a').forEach(link=>link.addEventListener('click',closeMenu));
  document.addEventListener('keydown',event=>{if(event.key==='Escape'&&menu?.getAttribute('aria-expanded')==='true'){closeMenu();menu.focus();}});
  document.querySelector('[data-print]')?.addEventListener('click',()=>window.print());
  const search=document.querySelector('#project-search');
  if(!search)return;
  const select=document.querySelector('#project-category');
  const cards=[...document.querySelectorAll('[data-project]')];
  const count=document.querySelector('#result-count');
  const empty=document.querySelector('#empty-state');
  const pagination=document.querySelector('.pagination');
  const previous=document.querySelector('#previous-page');
  const next=document.querySelector('#next-page');
  const pageLabel=document.querySelector('#page-number');
  const categories=[...select.options].map(option=>option.value);
  const pageSize=6;
  let currentPage=1;
  function readUrl(){const p=new URLSearchParams(location.search);search.value=p.get('q')||'';select.value=categories.includes(p.get('category'))?p.get('category'):'All work';currentPage=Math.max(1,Number.parseInt(p.get('page'),10)||1);}
  function render(sync=true){
    const words=search.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    const matching=cards.filter(card=>(select.value==='All work'||card.dataset.category===select.value)&&words.every(word=>card.dataset.search.includes(word)));
    const totalPages=Math.max(1,Math.ceil(matching.length/pageSize));
    currentPage=Math.min(currentPage,totalPages);
    cards.forEach(card=>card.hidden=true);
    const start=(currentPage-1)*pageSize;
    matching.slice(start,start+pageSize).forEach(card=>card.hidden=false);
    count.textContent=matching.length?`${start+1} to ${Math.min(start+pageSize,matching.length)} of ${matching.length} projects`:'0 projects';
    empty.hidden=matching.length>0;pagination.hidden=totalPages<=1;
    previous.disabled=currentPage===1;next.disabled=currentPage===totalPages;pageLabel.textContent=`Page ${currentPage} of ${totalPages}`;
    if(sync){const p=new URLSearchParams();if(search.value.trim())p.set('q',search.value.trim());if(select.value!=='All work')p.set('category',select.value);if(currentPage>1)p.set('page',currentPage);try{history.replaceState(null,'',location.pathname+(p.size?'?'+p:'')+location.hash);}catch(_){}}
  }
  search.addEventListener('input',()=>{currentPage=1;render();});
  select.addEventListener('change',()=>{currentPage=1;render();});
  document.querySelectorAll('[data-reset]').forEach(button=>button.addEventListener('click',()=>{search.value='';select.value='All work';currentPage=1;render();search.focus();}));
  function turnPage(delta){currentPage+=delta;render();search.scrollIntoView({block:'start',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});search.focus({preventScroll:true});}
  previous.addEventListener('click',()=>turnPage(-1));next.addEventListener('click',()=>turnPage(1));
  window.addEventListener('popstate',()=>{readUrl();render(false);});
  readUrl();render(false);
})();
