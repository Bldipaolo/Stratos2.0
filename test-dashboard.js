const fs = require('fs');
const path = require('path');
const root = __dirname;
function assert(cond, msg){ if(!cond){ throw new Error(msg); } }
const html = fs.readFileSync(path.join(root,'index.html'),'utf8');
const css = fs.readFileSync(path.join(root,'styles.css'),'utf8');
const js = fs.readFileSync(path.join(root,'app.js'),'utf8');
const leads = JSON.parse(fs.readFileSync(path.join(root,'data','leads.json'),'utf8'));
const autos = JSON.parse(fs.readFileSync(path.join(root,'data','automations.json'),'utf8'));
['Boca Lead War Room','Hyper-Specific Demo Sites','One-Click Outreach Packs','Audit → Demo → Pitch','MedSpa Domination Pack','Revenue Forecast Simulator','Morning Briefing','Proof Vault','Public Portfolio Page','Client Close Room'].forEach(label=> assert(js.includes(label), `missing module ${label}`));
assert(html.includes('styles.css') && html.includes('app.js'), 'index does not load assets');
assert(css.includes('@media(max-width:980px)'), 'missing responsive CSS');
assert(leads.length >= 10, 'expected at least 10 real leads');
assert(leads.every(l=>l.business && l.industry && l.phone && l.score && l.weaknesses && l.offer), 'lead missing required fields');
assert(autos.length === 8, 'automation catalog should have 8 items');
console.log('All Stratos dashboard checks passed:', { leads: leads.length, automations: autos.length });
