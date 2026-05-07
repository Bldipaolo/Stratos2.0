const MODULES = [
  ['strategy','00','Strategy OS'],
  ['intelligence','01','Command Intelligence'],
  ['today','02','Today Action Board'],
  ['war','03','Sales War Room v2'],
  ['crm','03A','Persistent CRM Board'],
  ['offers','04','Offer Ladder'],
  ['outreach','05','Outreach Vault'],
  ['medspa','06','MedSpa Campaign'],
  ['audit','07','Client Audit Generator'],
  ['closeTemplates','08','Close Room Templates'],
  ['demos','09','Demo Gallery'],
  ['verticals','09A','Vertical Demo Sites'],
  ['repurpose','10','Content Repurposing'],
  ['cases','11','Case Study Templates'],
  ['pitch','12','One-Click Pitch Packs'],
  ['workflow','13','Audit → Demo → Pitch'],
  ['revenue','14','Revenue Forecast Simulator'],
  ['pricing','14A','Pricing / Scope Calculator'],
  ['briefing','15','Morning Briefing'],
  ['proof','16','Proof Vault'],
  ['portfolio','17','Public Portfolio Page'],
  ['close','18','Client Close Room'],
  ['launch','18A','School-Safe Launch Page'],
  ['n8n','19','n8n Automation Library'],
  ['ops','20','Ops Logistics'],
  ['ruflo','21','Ruflo Orchestration'],
  ['swarmArena','21X','Swarm Arena'],
  ['usage','∞','Usage Saver']
];
const state={leads:[], automations:[], growth:null, premium:null, ops:null, demoSystem:null, ruflo:null, rufloArena:null, crm:{}, active:'strategy', selected:null};
const $=s=>document.querySelector(s);
const fmt=n=>new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0}).format(n||0);
const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
function toast(msg){const t=$('#toast');t.textContent=msg;t.classList.add('show-toast');setTimeout(()=>t.classList.remove('show-toast'),2400)}
async function init(){
  state.leads=await fetch('./data/leads.json').then(r=>r.json());
  state.automations=await fetch('./data/automations.json').then(r=>r.json());
  state.growth=await fetch('./data/stratos_growth_system.json').then(r=>r.json());
  state.premium=await fetch('./data/stratos_premium_ops.json').then(r=>r.json());
  state.ops=await fetch('./data/stratos_ops_library.json').then(r=>r.json());
  state.demoSystem=await fetch('./data/stratos_demo_site_system.json').then(r=>r.json());
  state.ruflo=await fetch('./data/stratos_ruflo_system.json').then(r=>r.json());
  state.rufloArena=await fetch('./data/stratos_ruflo_arena.json').then(r=>r.json());
  state.crm=loadCrm();
  state.selected=state.leads.slice().sort((a,b)=>b.score-a.score)[0];
  renderNav(); route(location.hash.replace('#','')||'strategy');
  window.addEventListener('hashchange',()=>route(location.hash.replace('#','')||'strategy'));
  $('#briefBtn').onclick=()=>{location.hash='briefing'; toast('Morning briefing generated from current lead board.')};
  $('#exportBtn').onclick=exportSnapshot;
}
function navCluster(id){
  if(['strategy','intelligence','today','war','crm'].includes(id)) return 'Command';
  if(['offers','outreach','medspa','audit','closeTemplates','pitch','workflow'].includes(id)) return 'Sales';
  if(['demos','verticals','repurpose','cases','proof','portfolio','close','launch'].includes(id)) return 'Proof';
  if(['revenue','pricing','briefing','n8n','ops','ruflo','swarmArena','usage'].includes(id)) return 'Ops';
  return 'System';
}
function renderNav(){
 const groups={}; MODULES.forEach(m=>{const g=navCluster(m[0]); (groups[g]=groups[g]||[]).push(m)});
 $('#nav').innerHTML=Object.entries(groups).map(([group,mods])=>`<div class="nav-cluster"><div class="nav-label">${group}</div>${mods.map(([id,num,name])=>`<button class="nav-btn" data-id="${id}"><span>${name}</span><small>${num}</small></button>`).join('')}</div>`).join('');
 document.querySelectorAll('.nav-btn').forEach(b=>b.onclick=()=>{location.hash=b.dataset.id});
}
function route(id){state.active=id; document.querySelectorAll('.nav-btn').forEach(b=>b.classList.toggle('active',b.dataset.id===id)); const mod=MODULES.find(m=>m[0]===id)||MODULES[0]; $('#pageTitle').textContent=mod[2]; ({strategy,intelligence,today,war,crm,offers,outreach,medspa,audit,closeTemplates,demos,verticals,repurpose,cases,pitch,workflow,revenue,pricing,briefing,proof,portfolio,close,launch,n8n,ops,ruflo,swarmArena,usage}[mod[0]]||strategy)();}
function metrics(){const leads=state.leads, hot=leads.filter(l=>l.score>=88).length, pipe=leads.reduce((a,l)=>a+l.estBookings*l.avgValue,0); return `<div class="grid cols-4"><div class="card metric"><span>Total Leads</span><b>${leads.length}</b></div><div class="card metric"><span>Hot Leads 88+</span><b>${hot}</b></div><div class="card metric"><span>Projected Upside</span><b>${fmt(pipe)}</b></div><div class="card metric"><span>Execution Mode</span><b>Local-first</b></div></div>`}
function leadOptions(){return state.leads.map(l=>`<option value="${l.id}">${esc(l.business)} · ${esc(l.industry)} · ${l.score}</option>`).join('')}
function selectLead(id){state.selected=state.leads.find(l=>l.id===id)||state.leads[0]}
function copy(cmd){navigator.clipboard&&navigator.clipboard.writeText(cmd); toast('Copied command')}
function strategy(){
 const top=state.leads.slice().sort((a,b)=>b.score-a.score).slice(0,4);
 const total=state.leads.reduce((a,l)=>a+upside(l),0);
 const hot=state.leads.filter(l=>l.score>=88).length;
 const verticals=industryStats().slice(0,4);
 const ops=[
  ['Command','Decide what matters today','Strategy OS, Intelligence, Today board, War Room'],
  ['Sell','Create targeted demand','Offers, outreach, audits, pitch packs, close templates'],
  ['Prove','Show premium output','Demo sites, proof vault, portfolio, close rooms'],
  ['Operate','Ship without chaos','Pricing, briefings, n8n, Ops, Ruflo, Usage Saver']
 ];
 const commands=[['Full system rebuild','python3 scripts/run_all.py'],['Launch Ruflo arena','python3 scripts/ruflo_arena.py mission --mode ambush --objective "48-hour Boca medspa revenue ambush" --run-ruflo'],['Morning Ruflo rhythm','python3 scripts/ruflo_daily.py morning'],['Generate briefing','python3 scripts/generate_morning_briefing.py'],['Validate dashboard','python3 scripts/validate_dashboard.py']];
 $('#app').innerHTML=`<section class="revive-home">
  <div class="revive-hero">
    <div class="hero-orbit"><i></i><i></i><i></i><b>STRATOS</b></div>
    <div class="hero-copy"><p class="eyebrow">Revitalized command center</p><h2>Premium agency cockpit for pipeline, proof, automation, and Ruflo-powered execution.</h2><p>The hub is now organized around four lanes: command the day, sell the offer, prove the work, and operate the machine. Less clutter. More signal. Same local-first, deploy-safe Stratos backbone.</p><div class="hero-actions"><button onclick="location.hash='war'">Enter War Room</button><button onclick="location.hash='swarmArena'">Launch Swarm Arena</button><a href="./ruflo/Swarm-Arena.html">Standalone arena</a></div></div>
    <aside class="hero-control"><span>Live system</span><b>${fmt(total)}</b><small>Projected monthly opportunity from ${state.leads.length} current Boca-area targets.</small><div class="mini-ledger"><div><em>${hot}</em><span>Hot leads 88+</span></div><div><em>${state.automations.length}</em><span>Automation plays</span></div><div><em>${state.demoSystem.verticals.length}</em><span>Vertical demos</span></div></div></aside>
  </div>
  <div class="command-ribbon">${[['Today','today','Daily board'],['Pipeline','war','Priority leads'],['Ruflo','ruflo','Coordination'],['Arena','swarmArena','War game'],['Usage','usage','Quota defense']].map(x=>`<button onclick="location.hash='${x[1]}'"><span>${x[0]}</span><b>${x[2]}</b></button>`).join('')}</div>
  <div class="ops-quadrants">${ops.map((o,i)=>`<article class="quadrant q${i+1}"><span>${String(i+1).padStart(2,'0')}</span><h2>${o[0]}</h2><p>${o[1]}</p><small>${o[2]}</small></article>`).join('')}</div>
  <div class="mission-layout"><section class="card priority-stack"><div class="section-kicker">Next best moves</div><h2>Money board</h2>${top.map((l,i)=>`<article class="priority-row"><span>#${i+1}</span><div><b>${esc(l.business)}</b><p>${esc(l.industry)} · ${fmt(upside(l))}/mo upside · ${esc(l.angle)}</p></div><button onclick="selectLead('${l.id}'); location.hash='pitch'">Pitch</button></article>`).join('')}</section><section class="card vertical-stack-card"><div class="section-kicker">Market lanes</div><h2>Where to attack</h2>${verticals.map(v=>`<div class="vertical-meter"><div><b>${esc(v.name)}</b><span>${v.count} leads · avg score ${v.avg}</span></div><strong>${fmt(v.upside)}</strong></div>`).join('')}</section></div>
  <div class="card command-deck"><div><p class="eyebrow">Copy-ready operator deck</p><h2>Run the machine</h2><p class="muted">Fast paths for rebuilds, Ruflo coordination, validation, and daily planning.</p></div>${commands.map(([label,cmd])=>`<div class="cmd-row"><div><b>${label}</b><code>${esc(cmd)}</code></div><button onclick="copy('${cmd.replace(/\\/g,'\\\\').replace(/'/g,"\\'")}')">Copy</button></div>`).join('')}</div>
 </section>`;
}

function intelligence(){
 const p=state.premium, top=state.leads.slice().sort((a,b)=>(b.score-a.score)||(upside(b)-upside(a))).slice(0,4);
 const lanes=p.operatingSystem;
 const packets=p.dealPackets;
 const studio=p.higgsfieldStudio;
 const totalPipe=state.leads.reduce((a,l)=>a+upside(l),0);
 const medPipe=state.leads.filter(l=>l.industry==='Medspa').reduce((a,l)=>a+upside(l),0);
 $('#app').innerHTML=`<section class="intel-shell">
  <div class="intel-hero">
    <div><p class="eyebrow">Premier rebuild layer</p><h2>The revenue command room for Stratos.</h2><p>${esc(p.positioning.coreThesis)}</p><div class="intel-actions"><button onclick="location.hash='war'">Work pipeline</button><button onclick="location.hash='outreach'">Send outreach</button><a href="./STRATOS_PREMIUM_REBUILD_BLUEPRINT.md">Blueprint</a><a href="./HIGGSFIELD_CREATIVE_STUDIO.md">Higgsfield studio</a></div></div>
    <aside class="intel-verdict"><span>Current verdict</span><b>Strong bones. Premium visuals now exist.</b><small>${esc(p.repoAuditFindings[1])}</small><div class="verdict-list"><div><strong>Next sale</strong><em>Medspa concierge</em></div><div><strong>Creative</strong><em>GPT Image 2 OAuth shipped</em></div><div><strong>Ship mode</strong><em>Static / Vercel-safe</em></div></div></aside>
  </div>
  <div class="intel-scoreboard">
    <div class="intel-score primary"><span>Total pipeline</span><b>${fmt(totalPipe)}</b><small>Opportunity math from current lead board</small></div>
    <div class="intel-score"><span>Medspa wedge</span><b>${fmt(medPipe)}</b><small>Primary market attack lane</small></div>
    <div class="intel-score"><span>GPT Image 2 OAuth</span><b>${p.higgsfieldStudio.oauthAssetPack?.successfulRenders||9} renders</b><small>${studio.contentSeries?.feedPosts||30} posts: original green/black/cream palette, no day labels, measured overlays</small></div>
    <div class="intel-score"><span>Proof discipline</span><b>${p.proofLedger.statuses.length} stages</b><small>Demo → result guardrails embedded</small></div>
  </div>
  <div class="quality-wall">${p.positioning.qualityBar.map((q,i)=>`<div><span>Q${i+1}</span><p>${esc(q)}</p></div>`).join('')}</div>
  <div class="section-title"><h2>Operating lanes</h2><p>Every module now rolls up into one of these command lanes.</p></div>
  <div class="lane-grid">${lanes.map(l=>`<article class="lane-card"><p class="eyebrow">${esc(l.lane)}</p><h2>${esc(l.goal)}</h2><ul>${l.dailyMoves.slice(0,3).map(m=>`<li>${esc(m)}</li>`).join('')}</ul><div class="lane-metric"><b>Measure</b><span>${esc(l.ownerMetric)}</span></div><details class="failure-mode"><summary>Failure mode</summary><span>${esc(l.failureMode)}</span></details></article>`).join('')}</div>
  <div class="split premium-split"><div class="card deal-command"><h2>Deal packet router</h2><p class="muted">Use these as the prospect-specific sales spine before writing anything custom.</p>${packets.map(d=>`<details class="deal-packet"><summary><span>${esc(d.vertical)}</span><b>${esc(d.flagshipOffer)}</b><em>${esc(d.recommendedPackage)}</em></summary><p>${esc(d.firstTouch)}</p><div class="trigger-list">${d.triggerSignals.map(s=>`<span>${esc(s)}</span>`).join('')}</div><div class="sales-line">${esc(d.closeRoomPromise)}</div></details>`).join('')}</div><div class="card"><h2>Today’s boardroom targets</h2>${top.map((l,i)=>`<div class="boardroom-target"><span>${String(i+1).padStart(2,'0')}</span><div><b>${esc(l.business)}</b><p>${esc(l.industry)} · ${fmt(upside(l))}/mo upside · ${esc(l.angle)}</p></div><button onclick="selectLead('${l.id}'); location.hash='audit'">Audit</button></div>`).join('')}</div></div>
  <div class="split premium-split"><div class="card proof-rules"><h2>Proof ledger rules</h2>${p.proofLedger.rules.map(r=>`<div class="proof-rule">${esc(r)}</div>`).join('')}<h3>Capture checklist</h3><div class="trigger-list">${p.proofLedger.captureChecklist.map(x=>`<span>${esc(x)}</span>`).join('')}</div></div><div class="card higgs-panel"><h2>Creative Studio</h2><p class="muted">${esc(studio.currentStatus)}</p>${studio.modelPlan.map(m=>`<div class="model-plan"><b>${esc(m.asset)}</b><span>${esc(m.model)} · ${esc(m.format)}</span><small>${esc(m.post)}</small></div>`).join('')}<div class="asset-pack-callout"><b>${esc(studio.oauthAssetPack?.status||'ready')}</b><span>${esc(studio.oauthAssetPack?.usageLimitNote||'GPT Image 2 OAuth pack is ready.')}</span><a class="inline-link" href="${esc(studio.oauthAssetPack?.gallery||'./marketing-assets/gpt-image-2-oauth/index.html')}">Open OAuth asset gallery</a>${studio.contentSeries?`<a class="inline-link" href="${esc(studio.contentSeries.gallery)}">Open premium content series</a>`:''}</div><button onclick="location.hash='repurpose'">Use content engine</button></div></div>
  <div class="section-title"><h2>GPT Image 2 OAuth assets</h2><p>Premium source imagery generated without an OpenAI API key, with exact Stratos overlays handled locally.</p></div>
  <div class="oauth-asset-grid">${(studio.oauthAssetPack?.assets||[]).map(a=>`<a class="oauth-asset-card" href="${esc(a.path)}"><img src="${esc(a.path)}" alt="${esc(a.name)}"><span>${esc(a.name)}</span><small>${esc(a.use)}</small></a>`).join('')}</div>
 </section>`;
}

function upside(l){return (l.estBookings||0)*(l.avgValue||0)}
function industryStats(){
 const map={}; state.leads.forEach(l=>{map[l.industry]=map[l.industry]||{count:0,upside:0,score:0}; map[l.industry].count++; map[l.industry].upside+=upside(l); map[l.industry].score+=l.score;});
 return Object.entries(map).map(([name,v])=>({name,...v,avg:Math.round(v.score/v.count)})).sort((a,b)=>b.upside-a.upside);
}
function warMetricCards(leads=state.leads){
 const sorted=leads.slice().sort((a,b)=>b.score-a.score), top=sorted[0]||{}, hot=leads.filter(l=>l.score>=88), pipe=leads.reduce((a,l)=>a+upside(l),0), avg=Math.round(leads.reduce((a,l)=>a+l.score,0)/(leads.length||1));
 const medspa=leads.filter(l=>l.industry==='Medspa').reduce((a,l)=>a+upside(l),0);
 return `<div class="war-metrics">
  <div class="war-metric primary"><span>Pipeline upside</span><strong data-count="${pipe}">${fmt(pipe)}</strong><small>Monthly opportunity from current board</small></div>
  <div class="war-metric"><span>Priority lead</span><strong>${esc(top.business||'None')}</strong><small>${top.score||0} score · ${fmt(upside(top))}/mo</small></div>
  <div class="war-metric"><span>Hot targets</span><strong>${hot.length}/${leads.length}</strong><small>Score 88+ ready for first touch</small></div>
  <div class="war-metric"><span>Average score</span><strong>${avg}</strong><small>Board quality signal</small></div>
  <div class="war-metric"><span>Medspa upside</span><strong>${fmt(medspa)}</strong><small>Primary vertical focus</small></div>
 </div>`;
}
function scoreTone(score){return score>=90?'elite':score>=88?'hot':'warm'}
function intentLabel(l){return l.score>=90?'Send today':l.industry==='Medspa'?'Medspa lane':'Nurture'}
function war(){
 const industries=industryStats();
 $('#app').innerHTML=`<section class="war-room">
  <div class="war-hero reveal-card">
    <div><p class="eyebrow">Clean attack view</p><h2>Less clutter. More signal.</h2><p>Prioritize the highest-upside Boca businesses, see why they matter, and jump straight into pitch kits or private close rooms.</p></div>
    <div class="war-hero-panel"><span>Next best action</span><b>${esc(state.leads.slice().sort((a,b)=>b.score-a.score)[0]?.business||'Top lead')}</b><small>Open pitch kit → send concise first touch → attach close room.</small><button onclick="selectLead('${state.leads.slice().sort((a,b)=>b.score-a.score)[0]?.id||''}'); location.hash='pitch'">Build pitch</button></div>
  </div>
  ${warMetricCards()}
  <div class="war-layout">
    <aside class="war-control reveal-card">
      <div class="control-head"><span>Filters</span><button id="resetWar">Reset</button></div>
      <label>Industry</label><select id="industry"><option>All industries</option>${industries.map(i=>`<option>${esc(i.name)}</option>`).join('')}</select>
      <label>Search</label><input id="search" placeholder="Business, offer, weakness...">
      <label>Minimum score</label><input id="minScore" type="range" min="80" max="95" value="86"><div class="range-readout"><span>Show score ≥</span><b id="scoreReadout">86</b></div>
      <div class="vertical-stack"><h3>Vertical signal</h3>${industries.map(i=>`<button class="industry-chip" data-industry="${esc(i.name)}"><span>${esc(i.name)}</span><b>${fmt(i.upside)}</b><small>${i.count} leads · avg ${i.avg}</small></button>`).join('')}</div>
    </aside>
    <section class="war-board">
      <div class="board-top"><div><h2>Priority board</h2><p id="resultCount">${state.leads.length} leads</p></div><div class="sort-pill">Sorted by score + upside</div></div>
      <div id="leadCards" class="lead-cards"></div>
    </section>
  </div>
 </section>`;
 const draw=()=>{
  const q=$('#search').value.toLowerCase().trim(), ind=$('#industry').value, min=+$('#minScore').value; $('#scoreReadout').textContent=min;
  const rows=state.leads.filter(l=>(ind==='All industries'||l.industry===ind)&&l.score>=min&&[l.business,l.industry,l.offer,l.angle,...l.weaknesses].join(' ').toLowerCase().includes(q)).sort((a,b)=>(b.score-a.score)||(upside(b)-upside(a)));
  $('#resultCount').textContent=`${rows.length} lead${rows.length===1?'':'s'} visible`;
  $('#leadCards').innerHTML=rows.map((l,i)=>`<article class="lead-card ${scoreTone(l.score)}" style="--delay:${Math.min(i,8)*42}ms">
    <div class="lead-main"><div><span class="rank">#${i+1}</span><h3>${esc(l.business)}</h3><p>${esc(l.industry)} · ${esc(l.address)}</p></div><div class="score-ring" style="--score:${l.score}"><span>${l.score}</span></div></div>
    <div class="lead-kpis"><div><span>Upside</span><b>${fmt(upside(l))}/mo</b></div><div><span>Bookings</span><b>${l.estBookings}</b></div><div><span>Avg value</span><b>${fmt(l.avgValue)}</b></div></div>
    <div class="lead-focus"><span>${esc(intentLabel(l))}</span><p>${esc(l.weaknesses[0])}</p></div>
    <div class="offer-strip"><b>${esc(l.offer)}</b><small>${esc(l.angle)}</small></div>
    <div class="lead-actions"><button onclick="selectLead('${l.id}'); location.hash='pitch'">Pitch kit</button><a class="inline-link" href="./close-rooms/${l.id}.html">Close room</a><a class="inline-link subtle" href=".${l.demo}">Demo</a></div>
  </article>`).join('') || `<div class="empty-board"><b>No leads match this filter.</b><span>Lower the score threshold or reset filters.</span></div>`;
 };
 $('#search').oninput=draw; $('#industry').onchange=draw; $('#minScore').oninput=draw; $('#resetWar').onclick=()=>{$('#industry').value='All industries'; $('#search').value=''; $('#minScore').value=86; draw();};
 document.querySelectorAll('.industry-chip').forEach(b=>b.onclick=()=>{$('#industry').value=b.dataset.industry; draw();});
 draw();
}
function demos(){
 const gallery=state.growth.demoGallery, verticals=state.demoSystem.verticals;
 $('#app').innerHTML=sectionIntro('Proof you can show','Premium vertical demo gallery with generated hero imagery.','Each category now has a standalone demo site, GPT Image 2 OAuth hero asset, workflow framing, and a Command Center path into pricing, proof, and CRM.',`<a class="inline-link" href="./vertical-demos/medspa.html">Open medspa demo</a><a class="inline-link" href="./public-site/index.html">Public Stratos site</a>`)+`<div class="vertical-demo-grid">${verticals.map(v=>`<article class="vertical-demo-card" style="--accent:${esc(v.accent)}"><img src="${esc(v.heroImage)}" alt="${esc(v.vertical)} generated hero"><div><p class="eyebrow">${esc(v.vertical)}</p><h2>${esc(v.headline)}</h2><p>${esc(v.subhead)}</p><div class="demo-actions"><a class="inline-link" href="${esc(v.demoPath)}">Open premium demo</a><button onclick="location.hash='pricing'">Price it</button></div></div></article>`).join('')}</div><div class="section-title"><h2>Original lead-specific demo assets</h2><p>Current generated demos and private close rooms remain available for prospect outreach.</p></div><div class="demo-grid">${state.leads.map(l=>`<div class="card demo-card"><h2>${esc(l.business)}</h2><p class="muted">${esc(l.industry)}: ${esc(l.angle)}</p><p><span class="pill">AI booking</span><span class="pill">Lead capture</span><span class="pill">Before/after audit</span></p><a class="inline-link" href=".${l.demo}">Open demo</a> · <a class="inline-link" href="./close-rooms/${l.id}.html">Close room</a></div>`).join('')}</div>`;
}
function pitchText(l=state.selected){return `SUBJECT: Quick ${l.industry.toLowerCase()} growth idea for ${l.business}\n\nHey ${l.business} team — I was looking at your online booking and lead flow and noticed an opportunity: ${l.weaknesses[0].toLowerCase()}.\n\nI run Stratos AI. We build premium local-business sites with AI booking, missed-call recovery, review automation, and follow-up systems. For ${l.business}, I’d recommend: ${l.offer}.\n\nWhy it fits:\n- ${l.weaknesses.join('\n- ')}\n\nThe angle: ${l.angle}\n\nI can send a quick preview/mockup showing what this would look like with your brand. If it doesn’t feel useful, no worries.\n\n— Bradley\nStratos AI\n\nSMS/DM: Saw a couple ways ${l.business} could capture more ${l.industry.toLowerCase()} leads with AI booking + follow-up. Want me to send the quick preview?\n\nCALL OPENER: I’m local to Boca and built a quick growth-system concept for ${l.business}. The main idea is ${l.angle}\n\nLINKS:\nDemo: .${l.demo}\nClose room: ./close-rooms/${l.id}.html`}
function pitch(){ $('#app').innerHTML=`<div class="split"><div class="card"><h2>Pitch kit generator</h2><p class="muted">Select a lead. The pack generates email, SMS, DM, phone opener, pain points, offer, and demo/proposal CTA.</p><select id="leadSelect">${leadOptions()}</select><div style="height:14px"></div><textarea id="customNote" placeholder="Optional extra context for this lead"></textarea><div style="height:14px"></div><button id="genPitch">Regenerate Pack</button></div><div class="card"><h2>${esc(state.selected.business)}</h2><p class="muted">${esc(state.selected.angle)}</p><div id="pitchOut" class="pitch-output"></div></div></div>`; $('#leadSelect').value=state.selected.id; const gen=()=>{$('#pitchOut').textContent=pitchText(state.selected)+($('#customNote').value?`\n\nCUSTOM NOTE: ${$('#customNote').value}`:'')}; $('#leadSelect').onchange=e=>{selectLead(e.target.value); pitch()}; $('#genPitch').onclick=gen; gen(); }
function workflow(){ $('#app').innerHTML=`<div class="card"><h2>The main money workflow</h2><p class="muted">Every asset supports this one sequence: Scan → Audit → Demo → Pitch → Close → Fulfill → Prove.</p></div><div class="workflow" style="margin-top:16px">${[['Scan','Find real Boca leads'],['Audit','Score site + funnel gaps'],['Demo','Generate specific rebuild'],['Pitch','Send one-click pack'],['Close','Private proposal room'],['Fulfill','Website + AI automations'],['Prove','Proof vault + case study']].map((s,i)=>`<div class="step"><em>Step ${i+1}</em><strong>${s[0]}</strong><p class="muted">${s[1]}</p></div>`).join('')}</div><div class="section-title"><h2>Pipeline</h2></div><div class="pipeline">${['New','Contacted','Responded','Meeting','Closed'].map((stage,i)=>`<div class="stage"><h3>${stage}</h3>${i===0?state.leads.slice(0,4).map(l=>`<div class="mini-card"><b>${esc(l.business)}</b><br><span class="muted">${esc(l.offer)}</span></div>`).join(''):'<p class="muted">Waiting for movement.</p>'}</div>`).join('')}</div>`; }

function crm(){
 const stages=crmStages();
 const counts=stages.map(s=>[s,state.leads.filter(l=>leadStage(l)===s).length]);
 $('#app').innerHTML=sectionIntro('Persistent local CRM','Move leads through contacted, responded, meeting, won, and lost without needing a backend yet.','Statuses persist in localStorage on this browser. This is intentionally transparent: no fake outreach has been sent, and real integrations can replace this state store later.',`<button onclick="state.crm={};saveCrm();crm()">Reset local CRM</button>`)+`<div class="crm-summary">${counts.map(([s,c])=>`<div class="crm-stat ${stageClass(s)}"><span>${esc(s)}</span><b>${c}</b></div>`).join('')}</div><div class="crm-board">${stages.map(stage=>`<section class="crm-stage"><h2>${esc(stage)}</h2>${state.leads.filter(l=>leadStage(l)===stage).map(l=>`<article class="crm-card"><b>${esc(l.business)}</b><p>${esc(l.industry)} · Score ${l.score} · ${fmt(upside(l))}/mo</p><small>${esc(l.angle)}</small><select onchange="setLeadStage('${l.id}',this.value)">${stages.map(s=>`<option ${s===stage?'selected':''}>${esc(s)}</option>`).join('')}</select><div><a class="inline-link" href=".${l.demo}">Demo</a><a class="inline-link" href="./close-rooms/${l.id}.html">Close room</a></div></article>`).join('')||'<p class="muted">No leads in this lane yet.</p>'}</section>`).join('')}</div>`;
}
function verticals(){
 const rows=state.demoSystem.verticals;
 $('#app').innerHTML=sectionIntro('Vertical-specific automation diagrams','Five sellable categories now have demo sites, generated hero assets, and simple workflow maps.','Use these as client-facing visuals before building fully customized demos. Every proof statement remains clearly labeled as demo/projection unless live client data exists.',`<button onclick="location.hash='demos'">Open demo gallery</button>`)+`<div class="diagram-grid">${rows.map(v=>`<article class="diagram-card" style="--accent:${esc(v.accent)}"><div class="diagram-head"><img src="${esc(v.heroImage)}" alt="${esc(v.vertical)}"><div><p class="eyebrow">${esc(v.vertical)}</p><h2>${esc(v.offer)}</h2><p>${esc(v.proof)}</p></div></div><div class="workflow-map">${v.workflow.map((n,i)=>`<div class="workflow-node"><span>${String(i+1).padStart(2,'0')}</span><b>${esc(n)}</b></div>`).join('')}</div><a class="inline-link" href="${esc(v.demoPath)}">Open ${esc(v.vertical)} demo site</a></article>`).join('')}</div>`;
}
function pricing(){
 const defaults=state.demoSystem.pricingDefaults;
 const options=Object.keys(defaults);
 $('#app').innerHTML=sectionIntro('Pricing / scope calculator','Turn website package + automation complexity into setup and monthly pricing instantly.','Use this during a call or close-room prep to keep scope concrete. It gives transparent anchors, not fake ROI guarantees.',`<button onclick="location.hash='close'">Open close room</button>`)+`<div class="pricing-lab"><div class="card"><label>Package</label><select id="pkg">${options.map(o=>`<option>${esc(o)}</option>`).join('')}</select><label>Automation complexity</label><input id="complexity" type="range" min="0" max="4" value="2"><label>Extra landing pages</label><input id="pages" type="number" min="0" value="3"><label>Expected recovered leads / month</label><input id="recLeads" type="number" min="0" value="6"><label>Average customer value</label><input id="avgVal" type="number" min="0" value="850"></div><div class="pricing-output card" id="pricingOut"></div></div>`;
 const calc=()=>{const base=defaults[$('#pkg').value], complexity=+$('#complexity').value, pages=+$('#pages').value, leads=+$('#recLeads').value, val=+$('#avgVal').value; const setup=base.setup+(complexity*1250)+(pages*450), monthly=base.monthly+(complexity*350), recovered=leads*val, breakeven=Math.ceil((monthly||1)/(val||1)); $('#pricingOut').innerHTML=`<p class="eyebrow">Scope anchor</p><h2>${esc($('#pkg').value)}</h2><div class="roi"><span>Recommended setup</span><b>${fmt(setup)}</b></div><div class="roi"><span>Recommended monthly</span><b>${fmt(monthly)}</b></div><div class="roi"><span>Recovery scenario</span><b>${fmt(recovered)}/mo</b></div><p class="muted">Breakeven framing: if this recovers about ${breakeven} customer${breakeven===1?'':'s'} per month, the monthly system is covered. Label this as a scenario until real tracking exists.</p><button onclick="location.hash='proof'">Create proof plan</button>`};
 ['pkg','complexity','pages','recLeads','avgVal'].forEach(id=>$('#'+id).oninput=calc); calc();
}
function launch(){
 const links=state.demoSystem.schoolSafeLinks;
 $('#app').innerHTML=sectionIntro('School-safe launch page','A locked-down-computer friendly control page for Vercel/public use.','This page keeps the useful Stratos links in one lightweight location: dashboard routes, public site, vertical demos, briefing, proof, and deployment marker.',`<a class="inline-link" href="./STRATOS_DEPLOY_READY.txt">Deploy marker</a><a class="inline-link" href="./public-site/index.html">Public website</a>`)+`<div class="launch-grid">${links.map((href,i)=>`<a class="launch-tile" href="${esc(href)}"><span>${String(i+1).padStart(2,'0')}</span><b>${esc(href.replace('./','').replace('#','Command Center → '))}</b><small>Open</small></a>`).join('')}</div><div class="card"><h2>Launch discipline</h2><p class="muted">Use Vercel/public export for school access. Keep private working files local. Run <code>python3 scripts/run_all.py</code> before pushing.</p></div>`;
}
function medspa(){
 const meds=state.leads.filter(l=>l.industry==='Medspa'); const c=state.growth.medspaCampaign;
 $('#app').innerHTML=sectionIntro('Primary wedge campaign','MedSpa Growth OS: the fastest vertical to make Stratos feel premium and specific.','Aesthetic clinics sell high-trust, high-LTV services. The Stratos angle is not generic AI — it is consult capture, premium treatment journeys, proof sequencing, and follow-up.',`<button onclick="location.hash='outreach'">Use medspa scripts</button>`)+`<div class="grid cols-3" style="margin-top:16px"><div class="card"><h2>Positioning</h2><p class="muted">${esc(c.positioning)}</p><h3>Pain signals</h3>${c.painSignals.map(x=>`<div class="mini-card">${esc(x)}</div>`).join('')}</div><div class="card"><h2>Hooks to test</h2>${c.hooks.map(x=>`<div class="mini-card"><b>${esc(x)}</b></div>`).join('')}<div class="sales-line" style="margin-top:12px">${esc(c.demoOffer)}</div></div><div class="card"><h2>Medspa targets</h2>${meds.map(l=>`<div class="mini-card"><b>${esc(l.business)}</b><br><span class="muted">${esc(l.phone)} · Score ${l.score} · ${fmt(upside(l))}/mo upside</span></div>`).join('')}<button onclick="selectLead('${meds[0]?.id||state.leads[0].id}'); location.hash='audit'">Audit first target</button></div></div>`;
}
function revenue(){ $('#app').innerHTML=`<div class="split"><div class="card"><h2>Revenue forecast simulator</h2><p class="muted">Uses each lead’s estimated bookings and average value. Adjust live to make the ROI argument.</p><select id="leadSelect">${leadOptions()}</select><label class="muted">New bookings / month</label><input id="bookings" type="number"><label class="muted">Avg customer value</label><input id="value" type="number"><label class="muted">Stratos monthly fee</label><input id="fee" type="number" value="1500"></div><div class="card" id="roiOut"></div></div>`; $('#leadSelect').value=state.selected.id; const calc=()=>{const rev=+$('#bookings').value*+$('#value').value, fee=+$('#fee').value, roi=fee?(rev/fee).toFixed(1):'0.0'; $('#roiOut').innerHTML=`<h2>${esc(state.selected.business)}</h2><div class="roi"><span>Estimated added monthly revenue</span><b>${fmt(rev)}</b></div><div class="roi"><span>Stratos retainer</span><b>${fmt(fee)}</b></div><div class="roi"><span>ROI multiple</span><b>${roi}x</b></div><p class="muted">Pitch line: if this creates even ${Math.ceil(fee/(+$('#value').value||1))} extra bookings, the system pays for itself.</p>`}; $('#leadSelect').onchange=e=>{selectLead(e.target.value); revenue()}; $('#bookings').value=state.selected.estBookings; $('#value').value=state.selected.avgValue; ['bookings','value','fee'].forEach(id=>$('#'+id).oninput=calc); calc(); }
function briefing(){ const top=state.leads.slice().sort((a,b)=>b.score-a.score).slice(0,5); $('#app').innerHTML=`<div class="card"><p class="eyebrow">Morning Briefing</p><h2>Today’s highest-leverage moves</h2><p class="muted">Generated from the current War Room. No fake responses; this is task guidance until real integrations are connected.</p><a class="inline-link" href="./briefings/latest.md">Open generated briefing file</a></div><div class="grid cols-2" style="margin-top:16px"><div class="card"><h2>Top 5 targets</h2>${top.map((l,i)=>`<div class="proof-item"><div class="proof-dot"></div><div><b>${i+1}. ${esc(l.business)}</b><br><span class="muted">Score ${l.score}. Move: ${esc(l.angle)}</span></div></div>`).join('')}</div><div class="card"><h2>Action queue</h2>${['Generate Glamor Medical close room','Run audits for top 5','Send first pitch kits','Create Vercel preview for public portfolio','Persist leads to production data store'].map(x=>`<div class="mini-card">${x}</div>`).join('')}</div></div>`; }
function proof(){
 const verticals=state.demoSystem.verticals;
 const statuses=['Demo concept','Screenshot needed','Outreach sent','Client result','Case study ready'];
 $('#app').innerHTML=`<div class="grid cols-3"><div class="card metric"><span>Demo builds</span><b>${state.leads.length+verticals.length}</b></div><div class="card metric"><span>AI hero assets</span><b>${verticals.length}</b></div><div class="card metric"><span>Real client claims</span><b>0</b></div></div><div class="section-title"><h2>Proof Vault</h2><p>Screenshot paths, claim status, demo/projection guardrails, proposals, outreach, and case-study material.</p></div><div class="proof-vault-grid"><div class="card"><h2>Claim guardrails</h2>${statuses.map(s=>`<div class="proof-rule">${esc(s)}</div>`).join('')}<p class="muted">Rule: demos and projections can sell the system quality, but do not claim booked revenue until live client data exists.</p></div><div class="card"><h2>Screenshot / asset queue</h2>${verticals.map(v=>`<div class="proof-item"><div class="proof-dot"></div><div><b>${esc(v.vertical)} demo hero</b><br><span class="muted">Path: ${esc(v.heroImage)} · Status: generated source art + local page</span></div></div>`).join('')}</div></div><div class="section-title"><h2>Lead-specific proof ledger</h2></div><div class="card">${state.leads.map(l=>`<div class="proof-item"><div class="proof-dot"></div><div><b>${esc(l.business)} demo + close-room assets</b><br><span class="muted">Status: concept ready · Needs screenshot/audit capture · ${esc(l.demo)}</span></div></div>`).join('')}</div>`;
}
function portfolio(){ $('#app').innerHTML=`<div class="hero-public"><p class="eyebrow">Public Stratos Page</p><h2>Premium AI websites and automation systems for local businesses.</h2><p>Turn missed calls, weak websites, and cold traffic into booked appointments with AI lead capture, follow-up, reviews, and conversion-focused design.</p><a href="./public-site/index.html">Open generated public site</a></div><div class="grid cols-3" style="margin-top:16px">${['Premium website rebuilds','AI booking systems','Review + referral engines'].map(x=>`<div class="card"><h2>${x}</h2><p class="muted">Built for Boca businesses that need measurable lead capture, not generic web design.</p></div>`).join('')}</div>`; }
function close(){ $('#app').innerHTML=`<div class="split"><div class="close-room"><p class="eyebrow">Private Proposal Room</p><h2>${esc(state.selected.business)}</h2><p>${esc(state.selected.angle)}</p><div class="grid cols-2"><div class="roi"><span>Projected upside</span><b>${fmt(state.selected.estBookings*state.selected.avgValue)}/mo</b></div><div class="roi"><span>Recommended offer</span><b>${esc(state.selected.offer)}</b></div></div><h3>What we found</h3>${state.selected.weaknesses.map(w=>`<span class="pill">${esc(w)}</span>`).join('')}<h3>Investment</h3><div class="price">$2,500 setup + $1,500/mo</div><a href="./close-rooms/${state.selected.id}.html">Open generated close room</a> <button onclick="location.hash='pitch'">Generate outreach</button></div><div class="card"><h2>Launch plan</h2>${['48-hour audit and conversion map','7-day custom demo/proposal page','14-day launch of site + AI capture','30-day optimization and reporting'].map((x,i)=>`<div class="proof-item"><div class="proof-dot"></div><div><b>Phase ${i+1}</b><br><span class="muted">${x}</span></div></div>`).join('')}</div></div>`; }

function n8n(){
 const lib=state.ops;
 $('#app').innerHTML=sectionIntro('Automation implementation library','n8n workflows Bradley can sell, scope, import, and QA.','Each playbook turns a common local-business leak into a specific trigger → routing → notification → follow-up system. Templates use placeholders only; real credentials stay inside n8n.',`<a class="inline-link" href="./n8n/README.md">Open n8n README</a><a class="inline-link" href="./operations/templates/automation-scope-sheet.md">Scope sheet</a>`)+`<div class="n8n-grid">${lib.n8nGuides.map(g=>`<article class="card n8n-card"><p class="eyebrow">${esc(g.vertical)}</p><h2>${esc(g.name)}</h2><p class="muted"><b>Trigger:</b> ${esc(g.trigger)}</p><p>${esc(g.outcome)}</p><div class="node-list">${g.nodes.map(n=>`<span>${esc(n)}</span>`).join('')}</div><div class="sales-line">${esc(g.sellLine)}</div><a class="inline-link" href="${esc(g.file)}">Guide</a><a class="inline-link" href="${esc(g.template)}">Workflow JSON</a></article>`).join('')}</div><div class="section-title"><h2>Proactive next builds</h2><p>These are the next logistics/product assets I would add after this pass.</p></div><div class="grid cols-2">${lib.nextBuildIdeas.map((x,i)=>`<div class="card idea-card"><span>Next ${i+1}</span><p>${esc(x)}</p></div>`).join('')}</div>`;
}
function ops(){
 const lib=state.ops;
 $('#app').innerHTML=sectionIntro('Delivery logistics','The Stratos operating backbone for onboarding, fulfillment, QA, proof, and retention.','Use this when a prospect becomes serious so the sale turns into a clean scope and repeatable delivery lane.',`<a class="inline-link" href="./operations/README.md">Open ops README</a><a class="inline-link" href="./operations/CLIENT_ONBOARDING_CHECKLIST.md">Onboarding checklist</a><a class="inline-link" href="./operations/DELIVERY_QA_CHECKLIST.md">QA checklist</a>`)+`<div class="ops-timeline">${lib.logistics.map((l,i)=>`<article class="ops-step-card"><span>${String(i+1).padStart(2,'0')}</span><div><p class="eyebrow">${esc(l.cadence)}</p><h2>${esc(l.lane)}</h2><p>${esc(l.action)}</p><small>Artifact: ${esc(l.artifact)}</small></div></article>`).join('')}</div><div class="section-title"><h2>Reusable templates</h2><p>Fast-start documents for client intake, automation scoping, launch QA, and proof discipline.</p></div><div class="template-grid">${lib.templates.map(t=>`<article class="template-card"><p class="eyebrow">${esc(t.owner)}</p><h2>${esc(t.name)}</h2><p>${esc(t.use)}</p><a class="inline-link" href="${esc(t.file)}">Open template</a></article>`).join('')}</div>`;
}


function ruflo(){
 const r=state.ruflo;
 $('#app').innerHTML=sectionIntro('Ruflo orchestration layer','Ruflo is now wired into Stratos day-to-day execution as the coordination ledger.','Use it to search patterns, start swarms, spawn agent records, and store closeout memory — then Hermes/Codex immediately does the actual build, QA, and shipping work.',`<a class="inline-link" href="./ruflo/README.md">Ruflo README</a><a class="inline-link" href="./ruflo/DAY_TO_DAY_PROCESS.md">Day-to-day process</a>`)+`<section class="ruflo-hero"><div><p class="eyebrow">Cloned source</p><h2>${esc(r.source.summary)}</h2><p>${esc(r.positioning)}</p><div class="source-card"><b>Local clone</b><code>${esc(r.source.localPath)}</code><small>${esc(r.source.notes.join(' '))}</small></div></div><aside><span>Operating rule</span><b>Coordinate, then execute.</b><p>${esc(r.operatingRule)}</p><button onclick="copy('python3 scripts/ruflo_status.py')">Copy status command</button></aside></section><div class="section-title"><h2>Daily Stratos rhythm</h2><p>These routines turn Ruflo into the recurring operating cadence for pipeline, builds, QA, and learning.</p></div><div class="ruflo-rhythm">${r.dailyRhythm.map((d,i)=>`<article class="ruflo-step"><span>${String(i+1).padStart(2,'0')}</span><div><p class="eyebrow">${esc(d.slot)}</p><h2>${esc(d.intent)}</h2><p>${esc(d.stratosAction)}</p><div class="cmd-row"><div><b>Command</b><code>${esc(d.command)}</code></div><button onclick="copy('${d.command.replace(/\\/g,'\\\\').replace(/'/g,"\\'")}')">Copy</button></div></div></article>`).join('')}</div><div class="split premium-split"><div class="card"><h2>Use-case swarms</h2>${r.useCases.map(u=>`<div class="ruflo-case"><b>${esc(u.name)}</b><p>${esc(u.trigger)}</p><div class="node-list">${u.agents.map(a=>`<span>${esc(a)}</span>`).join('')}</div><small>${esc(u.output)}</small></div>`).join('')}</div><div class="card"><h2>Safe command deck</h2><p class="muted">These are copy-ready and keep Ruflo as coordination while Stratos scripts do deterministic production.</p>${r.safeCommands.map(row=>`<div class="cmd-row"><div><b>${esc(row.label)}</b><code>${esc(row.cmd)}</code></div><button onclick="copy('${row.cmd.replace(/\\/g,'\\\\').replace(/'/g,"\\'")}')">Copy</button></div>`).join('')}</div></div>`;
}


function swarmArena(){
 const a=state.rufloArena;
 const modes=a.modes.map(m=>`<button class="arena-mode" data-mode="${m.id}" style="--mode:${m.accent}"><b>${esc(m.name)}</b><span>${esc(m.objective)}</span></button>`).join('');
 $('#app').innerHTML=sectionIntro('Ruflo Swarm Arena','A crazy interactive agency war game: pick a mission, launch a specialized Ruflo swarm, then convert the choreography into real Stratos execution.','The browser animation is deterministic and proof-labeled. The matching CLI can register real Ruflo coordination records with --run-ruflo.',`<a class="inline-link" href="./ruflo/SWARM_ARENA.md">Arena docs</a><button onclick="copy('python3 scripts/ruflo_arena.py mission --mode ambush --objective &quot;48-hour Boca medspa revenue ambush&quot; --run-ruflo')">Copy live Ruflo mission</button>`)+`<section class="arena-stage"><div class="arena-copy"><p class="eyebrow">${esc(a.truthLabel)}</p><h2>${esc(a.tagline)}</h2><textarea id="arenaObjective">${esc(a.defaultObjective)}</textarea><div class="arena-actions"><button id="launchArena">Launch simulated swarm</button><button onclick="copy(document.getElementById('arenaObjective').value)">Copy objective</button></div></div><div class="arena-orb" aria-label="animated swarm orb"><i></i><i></i><i></i><b>RUFLO</b></div></section><div class="arena-modes">${modes}</div><div class="arena-grid"><section class="card arena-agents"><h2>Agent swarm</h2><div id="arenaAgents">${a.agents.map((ag,i)=>`<article class="agent-pod" style="--delay:${i*80}ms"><p class="eyebrow">${esc(ag.type)}</p><h3>${esc(ag.name)}</h3><p>${esc(ag.role)}</p><small>${esc(ag.output)}</small></article>`).join('')}</div></section><section class="card arena-feed"><h2>Live mission feed</h2><div id="arenaFeed"></div></section></div><div class="section-title"><h2>Mission timeline</h2><p>Each phase maps Ruflo coordination to a real Stratos work product.</p></div><div class="arena-phases">${a.phases.map(p=>`<article><span>${esc(p.time)}</span><h3>${esc(p.name)}</h3>${p.actions.map(x=>`<p>${esc(x)}</p>`).join('')}</article>`).join('')}</div><div class="card"><h2>Command deck</h2>${a.commandDeck.map(c=>`<div class="cmd-row"><div><b>Copy-ready</b><code>${esc(c)}</code></div><button onclick="copy('${c.replace(/\\/g,'\\\\').replace(/'/g,"\\'")}')">Copy</button></div>`).join('')}</div>`;
 const feed=$('#arenaFeed'); const objective=$('#arenaObjective'); let active=a.modes[0];
 document.querySelectorAll('.arena-mode').forEach(btn=>btn.onclick=()=>{active=a.modes.find(m=>m.id===btn.dataset.mode)||a.modes[0]; document.documentElement.style.setProperty('--arena-accent', active.accent); document.querySelectorAll('.arena-mode').forEach(b=>b.classList.toggle('active',b===btn)); btn.classList.add('active');});
 document.querySelector('.arena-mode')?.click();
 $('#launchArena').onclick=()=>{ const lines=[`Mission mode: ${active.name}`,`Objective locked: ${objective.value}`, 'Ruflo memory search queued', 'Hierarchical swarm initialized', ...a.agents.map(ag=>`${ag.name}: ${ag.output}`), 'Execution order: Hermes/Codex now builds, validates, commits, and pushes', 'Truth label: simulated in-browser until CLI --run-ruflo is executed']; feed.innerHTML=''; lines.forEach((line,i)=>setTimeout(()=>{feed.innerHTML+=`<p><span>${String(i+1).padStart(2,'0')}</span>${esc(line)}</p>`; feed.scrollTop=feed.scrollHeight;},i*180)); document.querySelectorAll('.agent-pod').forEach((pod,i)=>setTimeout(()=>pod.classList.add('hot'),i*110)); };
}

function usage(){
 const zero=['Generate demo pages from data','Build outreach pitch kits','Generate close rooms','Build public website','Create deploy manifest','Validate dashboard + data'];
 const cheap=['Draft first-pass outreach variants with Ollama','Summarize scraped websites locally','Classify leads by vertical','Rewrite blurbs using qwen3.5:9b'];
 const premium=['Architecture decisions','Complex debugging','Final product/design review','Multi-file refactors'];
 const commands=[['Full rebuild/test','python3 scripts/run_all.py'],['Validate without AI','python3 scripts/validate_dashboard.py'],['Generate all demo pages','python3 scripts/generate_demo_pages.py'],['Build pitch kits','python3 scripts/build_pitch_kits.py'],['Generate close rooms','python3 scripts/generate_close_rooms.py'],['Build public site','python3 scripts/build_public_site.py'],['Check local Ollama','python3 scripts/ollama_health.py'],['Draft with qwen3.5 locally','python3 scripts/ollama_draft.py --lead glamor-medical --mode all'],['Run on free port','python3 scripts/free_port_server.py --start 8790']];
 $('#app').innerHTML=`<div class="usage-hero"><p class="eyebrow">Quota Defense System</p><h2>Make Hermes feel endless by routing work to the cheapest capable lane.</h2><p>Codex stays reserved for architecture, hard debugging, and final review. Everything repeatable becomes scripts or cheap-model drafting.</p></div><div class="grid cols-3" style="margin-top:16px"><div class="card usage-card zero"><span>Tier 0</span><h2>Free Script</h2><p class="muted">No model calls. Use this for deterministic Stratos production work.</p>${zero.map(x=>`<div class="mini-card">${x}</div>`).join('')}</div><div class="card usage-card cheap"><span>Tier 1</span><h2>Cheap Draft</h2><p class="muted">Use local Ollama models for volume writing and classification without Codex quota.</p>${cheap.map(x=>`<div class="mini-card">${x}</div>`).join('')}</div><div class="card usage-card premium"><span>Tier 2</span><h2>Premium Review</h2><p class="muted">Use Codex/GPT-5.5 only when judgment quality matters most.</p>${premium.map(x=>`<div class="mini-card">${x}</div>`).join('')}</div></div><div class="split" style="margin-top:16px"><div class="card"><h2>Zero/local command deck</h2><p class="muted">Copy these into Terminal. Script commands spend no AI quota; Ollama commands run locally on your Mac.</p>${commands.map(([label,cmd])=>`<div class="cmd-row"><div><b>${label}</b><code>${esc(cmd)}</code></div><button onclick="copy('${cmd.replace(/\\/g,'\\\\').replace(/'/g,"\\'")}')">Copy</button></div>`).join('')}</div><div class="card"><h2>Quota routing log</h2><div class="quota-log"><div><b>Lead/demo generation</b><span>Free Script</span></div><div><b>Pitch + close-room generation</b><span>Free Script</span></div><div><b>Outreach copy variants</b><span>Local Ollama</span></div><div><b>Local models</b><span>qwen3.5:9b + qwen2.5-coder:7b</span></div><div><b>Dashboard architecture</b><span>Premium Review only</span></div><div><b>Browser smoke test</b><span>One pass after changes</span></div></div><p class="muted">Default Codex profile remains premium mode. Use <code>hermes -p stratos-local</code> for local drafts.</p></div></div>`;
}

function firstLeadByIndustry(industry){return state.leads.find(l=>l.industry===industry)||state.leads[0]}
function fillTemplate(t,l=state.selected){return esc(String(t||'').replaceAll('{{business}}',l.business).replaceAll('{{industry}}',l.industry).replaceAll('{{weakness}}',l.weaknesses?.[0]||'lead capture can be sharper').replaceAll('{{angle}}',l.angle).replaceAll('{{offer}}',l.offer))}
function sectionIntro(kicker,title,body,action){return `<section class="growth-hero"><div><p class="eyebrow">${esc(kicker)}</p><h2>${esc(title)}</h2><p>${esc(body)}</p></div>${action?`<div class="growth-hero-action">${action}</div>`:''}</section>`}

function crmStages(){return state.demoSystem?.crmStages||['New','Contacted','Responded','Meeting','Won','Lost']}
function loadCrm(){try{return JSON.parse(localStorage.getItem('stratosCrmStatus')||'{}')}catch(e){return {}}}
function saveCrm(){localStorage.setItem('stratosCrmStatus',JSON.stringify(state.crm));}
function leadStage(l){return state.crm[l.id]||'New'}
function setLeadStage(id,stage){state.crm[id]=stage;saveCrm();toast('CRM status saved locally');crm();}
function stageClass(stage){return String(stage).toLowerCase().replace(/\s+/g,'-')}
function today(){
 const moves=state.growth.todayMoves;
 const top=state.leads.slice().sort((a,b)=>b.score-a.score).slice(0,4);
 $('#app').innerHTML=sectionIntro('Built for today','Six concrete moves to create pipeline, proof, and sharper offers before tomorrow.','This is the daily operator board: no fake numbers, no vague strategy, just the actions that move Stratos toward conversations and closed work.',`<button onclick="location.hash='outreach'">Open scripts</button><button onclick="location.hash='offers'">Open offers</button>`)+`<div class="today-layout"><div class="today-list">${moves.map((m,i)=>`<article class="today-card"><div class="today-num">${String(i+1).padStart(2,'0')}</div><div><span class="priority">${esc(m.priority)} · ${esc(m.timebox)}</span><h2>${esc(m.title)}</h2><p>${esc(m.outcome)}</p><ul>${m.actions.map(a=>`<li>${esc(a)}</li>`).join('')}</ul><small>${esc(m.proof)}</small></div></article>`).join('')}</div><aside class="card focus-panel"><h2>Start here</h2>${top.map((l,i)=>`<div class="mini-card"><b>${i+1}. ${esc(l.business)}</b><br><span class="muted">${esc(l.industry)} · ${esc(l.offer)} · ${fmt(upside(l))}/mo upside</span></div>`).join('')}<button onclick="location.hash='pitch'">Generate first touch</button></aside></div>`;
}
function offers(){
 const offers=state.growth.offerLadder;
 $('#app').innerHTML=sectionIntro('Sellable packages','A clean $3k / $5k / $10k offer ladder with a retainer path.','These packages make Stratos easier to explain, easier to price, and easier to upsell without custom proposal chaos.',`<button onclick="location.hash='closeTemplates'">Use in close rooms</button>`)+`<div class="offer-ladder">${offers.map((o,i)=>`<article class="offer-card"><div class="offer-head"><span>0${i+1}</span><strong>${esc(o.price)}</strong></div><h2>${esc(o.name)}</h2><p>${esc(o.promise)}</p><div class="fit"><b>Best for</b><span>${esc(o.bestFor)}</span></div><h3>Deliverables</h3><ul>${o.deliverables.map(d=>`<li>${esc(d)}</li>`).join('')}</ul><div class="sales-line">${esc(o.salesLine)}</div><small>Next step: ${esc(o.upsell)}</small></article>`).join('')}</div>`;
}
function outreach(){
 const g=state.growth.outreachVault, l=state.selected;
 const verticals=['Medspa','Dental','Plumbing','HVAC','Legal','Auto'];
 $('#app').innerHTML=sectionIntro('Ready-to-send copy','Outreach scripts that feel specific without pretending we have fake results.','Select a lead, then copy the channel that fits: DM, email, follow-up, Loom, or phone opener.',`<select id="leadSelect">${leadOptions()}</select>`)+`<div class="script-grid"><div class="card script-card"><h2>DM opener</h2><pre>${fillTemplate(g.dmShort,l)}</pre><button onclick="copy(\`${fillTemplate(g.dmShort,l)}\`)">Copy DM</button></div><div class="card script-card wide"><h2>Email first touch</h2><pre>${fillTemplate(g.emailFirstTouch,l)}</pre><button onclick="copy(\`${fillTemplate(g.emailFirstTouch,l)}\`)">Copy email</button></div><div class="card script-card"><h2>Loom script</h2><pre>${fillTemplate(g.loomScript,l)}</pre><button onclick="copy(\`${fillTemplate(g.loomScript,l)}\`)">Copy Loom</button></div><div class="card script-card"><h2>Phone opener</h2><pre>${fillTemplate(g.phoneOpener,l)}</pre><button onclick="copy(\`${fillTemplate(g.phoneOpener,l)}\`)">Copy phone</button></div><div class="card script-card wide"><h2>Follow-up sequence</h2>${g.followUps.map((f,i)=>`<div class="mini-card followup-row"><div><b>Follow-up ${i+1}</b><br><span>${fillTemplate(f,l)}</span></div><button onclick="copy(\`${fillTemplate(f,l)}\`)">Copy</button></div>`).join('')}</div><div class="card"><h2>Vertical defaults</h2>${verticals.map(v=>{const lead=firstLeadByIndustry(v);return `<button class="industry-chip" onclick="selectLead('${lead.id}'); outreach()"><span>${esc(v)}</span><small>${esc(lead.business)}</small></button>`}).join('')}</div></div>`;
 $('#leadSelect').value=state.selected.id; $('#leadSelect').onchange=e=>{selectLead(e.target.value); outreach()};
}
function audit(){
 const checks=state.growth.auditGenerator.checks, l=state.selected;
 $('#app').innerHTML=sectionIntro('Client Audit Generator','Turn a website scan into a precise, useful sales asset.','Use this before Looms, emails, or close rooms. The goal is to diagnose the front-door leak and recommend the first practical fix.',`<select id="leadSelect">${leadOptions()}</select>`)+`<div class="audit-grid"><div class="audit-checks">${checks.map((c,i)=>`<article class="audit-card"><span>0${i+1}</span><h2>${esc(c.area)}</h2><p><b>Question:</b> ${esc(c.question)}</p><p><b>Fix:</b> ${esc(c.fix)}</p><button onclick="copy('${c.area.replace(/'/g,"\\'")}: ${c.fix.replace(/'/g,"\\'")}')">Copy fix</button></article>`).join('')}</div><aside class="card audit-summary"><h2>${esc(l.business)} quick summary</h2><p>${esc(state.growth.auditGenerator.summaryTemplate.replace('{{business}}',l.business).replace('{{area}}',checks[0].area).replace('{{weakness}}',l.weaknesses[0].toLowerCase()).replace('{{fix}}',checks[0].fix.toLowerCase()))}</p><h3>Lead-specific signals</h3>${l.weaknesses.map(w=>`<span class="pill">${esc(w)}</span>`).join('')}<button onclick="location.hash='pitch'">Turn into pitch</button></aside></div>`;
 $('#leadSelect').value=state.selected.id; $('#leadSelect').onchange=e=>{selectLead(e.target.value); audit()};
}
function closeTemplates(){
 const templates=state.growth.closeRoomTemplates;
 $('#app').innerHTML=sectionIntro('Private proposal rooms','Four close-room structures for the verticals Stratos can sell first.','Each template keeps the proposal simple: diagnose the leak, show the system, anchor investment, and ask for the next step.',`<button onclick="location.hash='close'">Open live close room</button>`)+`<div class="template-grid">${templates.map(t=>`<article class="template-card"><p class="eyebrow">${esc(t.vertical)}</p><h2>${esc(t.headline)}</h2><div class="template-sections">${t.sections.map(s=>`<span>${esc(s)}</span>`).join('')}</div><div class="cta-strip">${esc(t.cta)}</div></article>`).join('')}</div>`;
}
function repurpose(){
 const rows=state.growth.repurposingEngine;
 $('#app').innerHTML=sectionIntro('Content multiplier','Turn one Stratos asset into LinkedIn, X, email hooks, and reel prompts.','This keeps content output high without making every post look like the same AI template.',`<a class="inline-link" href="./marketing-assets/stratos-gpt2-premium-content-series/index.html">Open GPT Image 2 premium series</a><a class="inline-link" href="./marketing-assets/stratos-gpt2-premium-content-series/CONTENT_CALENDAR.md">Open premium calendar</a>`)+`<div class="repurpose-grid">${rows.map((r,i)=>`<article class="card repurpose-card"><span class="priority">Source ${i+1}: ${esc(r.source)}</span><h2>Repurpose stack</h2><div class="channel"><b>LinkedIn</b><p>${esc(r.linkedin)}</p></div><div class="channel"><b>X</b><p>${esc(r.x)}</p></div><div class="channel"><b>Email hook</b><p>${esc(r.emailHook)}</p></div><div class="channel"><b>Reel prompt</b><p>${esc(r.reelPrompt)}</p></div></article>`).join('')}</div>`;
}
function cases(){
 const rows=state.growth.caseStudies;
 $('#app').innerHTML=sectionIntro('Transparent proof builder','Demo case studies that explain value without inventing client results.','Use these in outbound and close rooms as clearly-labeled examples until real client outcomes exist.',`<button onclick="location.hash='proof'">Open Proof Vault</button>`)+`<div class="case-grid">${rows.map(c=>`<article class="case-card"><span>${esc(c.label)}</span><h2>${esc(c.title)}</h2><div class="before-after"><div><b>Before</b><p>${esc(c.before)}</p></div><div><b>After</b><p>${esc(c.after)}</p></div></div><h3>Assets to show</h3>${c.assets.map(a=>`<span class="pill">${esc(a)}</span>`).join('')}<p class="guardrail"><b>Guardrail:</b> ${esc(c.claimGuardrail)}</p></article>`).join('')}</div>`;
}

function exportSnapshot(){ const blob=new Blob([JSON.stringify({exportedAt:new Date().toISOString(),leads:state.leads,automations:state.automations},null,2)],{type:'application/json'}); const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='stratos-command-snapshot.json'; a.click(); toast('Snapshot exported.'); }
init().catch(err=>{document.body.innerHTML='<pre>'+err.stack+'</pre>';});
