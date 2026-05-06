#!/usr/bin/env python3
"""Build Stratos premium GPT Image 2 OAuth content series with exact local overlays."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import json, re, textwrap, zipfile, shutil, math
import numpy as np
import imageio.v2 as imageio

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / 'marketing-assets' / 'stratos-gpt2-premium-content-series'
SOURCE = PACK / 'source'
ASSETS = PACK / 'assets'
FEED = ASSETS / 'feed'
STORIES = ASSETS / 'stories'
CAROUSELS = ASSETS / 'carousels'
VIDEOS = PACK / 'videos'
for d in [FEED, STORIES, CAROUSELS, VIDEOS]:
    d.mkdir(parents=True, exist_ok=True)

BLACK=(3,6,5); INK=(10,16,13); GREEN=(20,88,56); GREEN2=(36,126,79); GREEN3=(85,174,116)
WHITE=(248,250,246); CREAM=(238,240,232); MUTED=(184,198,188); GOLD=(211,199,160)
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
BOLD='/System/Library/Fonts/Supplemental/Arial Bold.ttf'

def font(size,b=False):
    return ImageFont.truetype(BOLD if b else FONT,size)

def slug(s):
    return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')[:62]

def wrap(s,w):
    return '\n'.join(textwrap.wrap(s,w,break_long_words=False))

def txt(d,xy,s,size,fill=WHITE,b=False,anchor=None,spacing=8,align='left'):
    d.multiline_text(xy,s,font=font(size,b),fill=fill,anchor=anchor,spacing=spacing,align=align)

def rr(d,box,r,fill,outline=None,width=1):
    d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=width)

def logo(d,x,y,scale=1.0,dark=True):
    mark=int(56*scale)
    rr(d,(x,y,x+mark,y+mark),16,fill=GREEN2,outline=GREEN3,width=max(1,int(2*scale)))
    txt(d,(x+mark/2,y+mark/2-1),'S',int(32*scale),WHITE,True,'mm')
    fill=WHITE if dark else INK
    txt(d,(x+mark+16,y+1),'STRATOS AI',int(26*scale),fill,True)
    txt(d,(x+mark+18,y+34),'WEBSITES • AUTOMATION • REVENUE',int(10*scale),GREEN3 if dark else GREEN,True)

def cover_image(src, size, crop='center'):
    im=Image.open(src).convert('RGB')
    sw,sh=im.size; tw,th=size
    scale=max(tw/sw, th/sh)
    im=im.resize((int(sw*scale),int(sh*scale)), Image.LANCZOS)
    nw,nh=im.size
    if crop=='top': y=0
    elif crop=='bottom': y=nh-th
    else: y=(nh-th)//2
    x=(nw-tw)//2
    return im.crop((x,y,x+tw,y+th)).convert('RGBA')

def grade(im, darken=120, blur=0.25):
    im=ImageEnhance.Color(im).enhance(.82)
    im=ImageEnhance.Contrast(im).enhance(1.08)
    if blur: im=im.filter(ImageFilter.GaussianBlur(blur))
    overlay=Image.new('RGBA', im.size, (0,0,0,darken))
    return Image.alpha_composite(im.convert('RGBA'), overlay)

def panel(d, box, alpha=190, light=False):
    fill=(248,250,246,226) if light else (0,0,0,alpha)
    rr(d,box,38,fill=fill,outline=(85,174,116,72),width=2)

def accent_flow(d,w,h,seed=1):
    # deterministic premium line motif; no fake generated type
    for i in range(3):
        y=int(h*(0.70+0.055*i))
        x0=80+i*18; x1=w-90-i*26
        d.line((x0,y,x1,y-50+i*38), fill=(85,174,116,110), width=4)
        d.ellipse((x0-8,y-8,x0+8,y+8), fill=(85,174,116,190))
        d.ellipse((x1-7,y-57+i*38,x1+7,y-43+i*38), fill=(85,174,116,150))

source_files=[
    ('front-office-command-room.png','Front Office Command Room'),
    ('large-firm-handoffs.png','Large Firm Handoff Map'),
    ('disconnected-tools-revenue-leak.png','Disconnected Systems'),
    ('medspa-after-hours-concierge.png','Medspa Concierge'),
    ('executive-response-dashboard.png','Outcome Dashboard'),
    ('chaos-to-clean-workflow.png','Chaos To Clean Workflow'),
]
for f,_ in source_files:
    if not (SOURCE/f).exists():
        raise SystemExit(f'Missing GPT Image 2 source art: {SOURCE/f}')

items=[
('Your website should act like your best operator.','A premium site captures demand, routes intent, and protects follow-up when the team is busy.','SYSTEMS',0),
('Large firms lose money in tiny handoffs.','Forms, missed calls, inboxes, and calendars should not behave like separate businesses.','ENTERPRISE FRICTION',1),
('Disconnected tools leak revenue.','Ads, website, CRM, calendar, and follow-up need one clean operating path.','INTEGRATION',2),
('Consult intent should not wait until morning.','Medspa leads need instant next steps, not a callback window that depends on office hours.','MEDSPA',3),
('Less dashboard. More booked calls.','The point is not more software. The point is making revenue movement obvious.','OUTCOMES',4),
('Turn chaos into one clean workflow.','Stratos makes the business easier to choose, easier to run, and easier to measure.','WORKFLOW',5),
('Speed is a brand asset.','The fastest serious business often feels like the most professional one.','FOLLOW-UP',0),
('Your CRM is not the strategy.','A database does not create revenue unless the workflow around it is alive.','CRM',4),
('A premium firm needs premium intake.','Before the first consultation, the experience should already feel organized and high-trust.','INTAKE',1),
('Missed calls should trigger movement.','Text-back, qualification, booking, and owner alerts should start instantly.','LOCAL SERVICES',0),
('Stop buying traffic for a broken system.','More visitors only help when the business captures intent and creates one clear next step.','CONVERSION',2),
('AI should disappear into the workflow.','No gimmicks. Just cleaner routing, faster answers, booked calls, and fewer manual touches.','AUTOMATION',5),
('Every lead deserves a next step.','Attention, trust, contact, follow-up, and revenue should connect without manual chasing.','LEAD OPS',0),
('Make the business easier to buy from.','Simple message. Fast response. Clear offer. One obvious path to action.','CLARITY',5),
('The best automations feel human.','They protect service from silence, delay, and dropped handoffs.','HUMAN AI',3),
('Modernize before the market notices.','By the time competitors copy the website, your systems should already be compounding.','ADVANTAGE',4),
('If the team is busy, the system should still sell.','Nights, weekends, and follow-up windows are where revenue disappears.','OPERATIONS',0),
('Your site should qualify, not just impress.','Beautiful design opens trust. Smart flows turn that trust into conversations.','WEBSITES',2),
('One clean path beats ten scattered buttons.','Complex firms need simple choices for prospects, not an obstacle course.','UX',5),
('Follow-up is where premium brands separate.','The second touch often matters more than the first click.','SALES',1),
('Outdated intake makes big firms look small.','When a serious prospect has to chase the business, the brand loses leverage.','LARGE FIRMS',1),
('Your best employee should not be the only system.','If everything depends on memory, tabs, and manual reminders, the business is leaking.','PROCESS',5),
('Make the invisible measurable.','Response time, source, next step, owner, and outcome should be obvious.','METRICS',4),
('Your online presence should feel expensive.','Not loud. Not complicated. Clear, fast, polished, and built to convert.','BRAND',0),
('Integrate before adding more tools.','Most businesses do not need another app. They need the current stack to finally talk.','STACK',2),
('The agency is not selling websites.','Stratos sells the modern front office: design, automation, and revenue flow.','STRATOS',0),
('Turn interest into scheduled action.','A serious website makes the next step obvious and helps the team follow through.','BOOKING',3),
('Local businesses deserve enterprise systems.','Medspas, dental offices, service brands, and firms can operate with bigger-team speed.','LOCAL',4),
('The buyer journey should not depend on office hours.','Good systems keep moving when the staff is with clients, in meetings, or offline.','24/7',3),
('Build the system customers feel.','From first impression to follow-up, Stratos makes the business sharper and more trustworthy.','CLOSE',5),
]

# Clear generated outputs only.
for folder in [FEED, STORIES, CAROUSELS, VIDEOS]:
    for p in folder.glob('*'):
        if p.is_file(): p.unlink()

feed=[]
for day,(headline,body,pillar,src_idx) in enumerate(items,1):
    src=SOURCE/source_files[src_idx][0]
    im=grade(cover_image(src,(1080,1080)), darken=142 if day%5 else 105, blur=.18)
    d=ImageDraw.Draw(im,'RGBA')
    # Five editorial layouts keep the campaign premium instead of template-heavy.
    mode=day%5
    if mode==0:
        box=(64,590,1016,1016); text_x=104; title_y=690; body_y=842; maxw=22; title_size=58
        d.rectangle((0,570,1080,1080),fill=(0,0,0,128)); panel(d,box,alpha=150)
        logo(d,86,74,1.0,True); txt(d,(104,638),f'DAY {day:02d} / {pillar}',18,GREEN3,True)
    elif mode==1:
        box=(54,54,728,1018); text_x=90; title_y=292; body_y=594; maxw=17; title_size=64 if len(headline)<46 else 57
        panel(d,box,alpha=178); logo(d,text_x,88,1.0,True); txt(d,(text_x,210),f'DAY {day:02d} / {pillar}',18,GREEN3,True)
    elif mode==2:
        box=(344,58,1024,1018); text_x=386; title_y=292; body_y=594; maxw=17; title_size=64 if len(headline)<46 else 57
        panel(d,box,alpha=176); logo(d,text_x,88,1.0,True); txt(d,(text_x,210),f'DAY {day:02d} / {pillar}',18,GREEN3,True)
    elif mode==3:
        box=(84,86,996,498); text_x=124; title_y=206; body_y=742; maxw=23; title_size=60
        panel(d,box,alpha=156); logo(d,124,112,0.92,True); txt(d,(124,184),f'DAY {day:02d} / {pillar}',17,GREEN3,True)
        d.rectangle((0,688,1080,1080),fill=(0,0,0,132))
    else:
        box=(90,92,990,990); text_x=134; title_y=304; body_y=612; maxw=18; title_size=62 if len(headline)<46 else 55
        rr(d,box,46,fill=(248,250,246,224),outline=(85,174,116,84),width=2)
        logo(d,text_x,128,1.0,False); txt(d,(text_x,246),f'DAY {day:02d} / {pillar}',18,GREEN,True)
    dark_text = (mode==4)
    fg=INK if dark_text else WHITE; sub=(74,92,78) if dark_text else MUTED; accent=GREEN if dark_text else GREEN3
    txt(d,(text_x,title_y),wrap(headline,maxw),title_size,fg,True,spacing=3)
    txt(d,(text_x+2,body_y),wrap(body,34 if mode in [0,3] else 30),32,sub,False,spacing=11)
    # Varied mechanism/proof treatment; CTA appears selectively to avoid repetitive ad-template rhythm.
    mech_y=910 if mode in [0,3] else 802
    if day%3==0:
        rr(d,(text_x,mech_y,text_x+560,mech_y+88),24,fill=(20,88,56,232),outline=GREEN3,width=2)
        txt(d,(text_x+28,mech_y+25),'SYSTEM FIX',18,WHITE,True)
        txt(d,(text_x+28,mech_y+52),'Capture → Route → Follow up',24,WHITE,True)
    elif day%3==1:
        for i,pt in enumerate(['Capture','Route','Book']):
            x=text_x+i*158; y=mech_y
            d.ellipse((x,y,x+50,y+50),fill=GREEN)
            txt(d,(x+25,y+25),str(i+1),22,WHITE,True,'mm')
            txt(d,(x,y+66),pt,19,fg,True)
            if i<2: d.line((x+58,y+25,x+136,y+25),fill=accent,width=4)
    else:
        txt(d,(text_x,mech_y),'Revenue leak → owned workflow',28,fg,True)
        d.line((text_x,mech_y+52,text_x+530,mech_y+52),fill=accent,width=5)
    if day%4 in [1,2]:
        rr(d,(text_x,944,text_x+574,1000),28,fill=GREEN if not dark_text else INK,outline=GREEN3,width=2)
        txt(d,(text_x+287,972),'DM STRATOS FOR A CLEAN AUDIT',18,WHITE,True,'mm')
    elif mode not in [0,3]:
        txt(d,(text_x,958),'STRATOS AI / MODERN FRONT OFFICE',21,accent,True)
    out=FEED/f'day_{day:02d}_{slug(headline)}.png'
    im.convert('RGB').save(out,quality=95)
    feed.append(out)

# Stories/reel covers: 12 high-impact verticals.
story_indices=[0,1,2,3,4,5,6,10,14,20,26,29]
stories=[]
for n,idx in enumerate(story_indices,1):
    headline,body,pillar,src_idx=items[idx]
    src=SOURCE/source_files[src_idx][0]
    crop='center'
    if 'medspa' in str(src).lower(): crop='top'
    im=grade(cover_image(src,(1080,1920),crop), darken=148, blur=.18)
    d=ImageDraw.Draw(im,'RGBA')
    d.rectangle((0,0,1080,430),fill=(0,0,0,92))
    d.rectangle((0,1320,1080,1920),fill=(0,0,0,132))
    logo(d,72,92,1.18,True)
    txt(d,(72,292),f'{pillar} / PREMIUM SYSTEMS',22,GREEN3,True)
    txt(d,(72,1318),wrap(headline,16),78 if len(headline)<44 else 68,WHITE,True,spacing=4)
    txt(d,(78,1580),wrap(body,29),38,MUTED,False,spacing=12)
    rr(d,(72,1774,1008,1856),41,fill=GREEN,outline=GREEN3,width=2)
    txt(d,(540,1816),'BOOK THE STRATOS REVENUE FLOW AUDIT',27,WHITE,True,'mm')
    out=STORIES/f'story_{n:02d}_{slug(headline)}.png'
    im.convert('RGB').save(out,quality=95)
    stories.append(out)

# Carousels: 4 premium mini-decks x 5 slides.
carousel_sets=[
('The Revenue Leak Audit',['Where intent enters','Where response slows','Where ownership disappears','Where follow-up dies','Where Stratos installs the path'],2),
('The Modern Front Office',['Website captures','Automation routes','Team gets context','Prospect gets next step','Owner sees outcome'],0),
('Premium Intake Playbook',['Fast first impression','One serious CTA','Instant qualification','Booked action','Measured follow-up'],3),
('Enterprise Handoff Fix',['Fewer tabs','Cleaner ownership','Less waiting','More booked action','One operating system'],1),
]
carousel=[]
for deck,(deck_title,slides,src_idx) in enumerate(carousel_sets,1):
    src=SOURCE/source_files[src_idx][0]
    for sidx,slide in enumerate(slides,1):
        im=grade(cover_image(src,(1080,1080)), darken=172 if sidx>1 else 130, blur=.28)
        d=ImageDraw.Draw(im,'RGBA')
        panel(d,(70,70,1010,1010),alpha=168)
        logo(d,104,108,1.0,True)
        txt(d,(104,230),f'0{sidx} / {deck_title.upper()}',20,GREEN3,True)
        if sidx==1:
            txt(d,(104,344),wrap(deck_title,14),86,WHITE,True,spacing=4)
            txt(d,(108,720),'Swipe for the exact Stratos operating logic.',34,MUTED,False)
        else:
            txt(d,(104,346),wrap(slide,13),92,WHITE,True,spacing=3)
            txt(d,(108,690),wrap('Premium brands do not leave this step to memory, manual tabs, or office-hour luck.',34),32,MUTED,False,spacing=10)
        accent_flow(d,1080,1080,deck+sidx)
        rr(d,(104,920,650,980),30,fill=GREEN,outline=GREEN3,width=2)
        txt(d,(377,950),'STRATOS SYSTEMS',22,WHITE,True,'mm')
        out=CAROUSELS/f'week_{deck:02d}_slide_{sidx:02d}_{slug(slide)}.png'
        im.convert('RGB').save(out,quality=95)
        carousel.append(out)

# Simple premium motion covers from GPT source/key-art.
video_specs=[
('website-is-your-operator',items[0],0),
('handoff-leak',items[1],1),
('disconnected-tools',items[2],2),
('medspa-after-hours',items[3],3),
('booked-action',items[4],4),
('clean-workflow',items[5],5),
]
for vid,(name,(headline,body,pillar,src_idx),src_idx) in enumerate(video_specs,1):
    src=SOURCE/source_files[src_idx][0]
    base=grade(cover_image(src,(1080,1920),'center'), darken=150, blur=.16)
    d=ImageDraw.Draw(base,'RGBA')
    logo(d,72,105,1.15,True)
    txt(d,(72,340),wrap(headline,15),78,WHITE,True,spacing=4)
    txt(d,(78,650),wrap(body,28),39,MUTED,False,spacing=12)
    rr(d,(72,1648,1008,1728),40,fill=GREEN,outline=GREEN3,width=2)
    txt(d,(540,1688),'STRATOS AI / REVENUE FLOW AUDIT',27,WHITE,True,'mm')
    frames=[]
    for f in range(105):
        frame=base.copy()
        od=ImageDraw.Draw(frame,'RGBA')
        offset=f*5
        od.line((90+offset%840,1518,420+offset%840,1518),fill=(85,174,116,160),width=7)
        od.ellipse((72+(offset*2)%920,1486,94+(offset*2)%920,1508),fill=(85,174,116,190))
        frames.append(np.array(frame.convert('RGB')))
    imageio.mimsave(VIDEOS/f'reel_{vid:02d}_{name}.mp4',frames,fps=25,quality=8,macro_block_size=1)

# Preview contact sheet
thumbs=[Image.open(p).resize((216,216)) for p in feed[:20]]
sheet=Image.new('RGB',(1080,1160),BLACK)
sd=ImageDraw.Draw(sheet)
for i,im in enumerate(thumbs):
    x=(i%5)*216; y=(i//5)*270
    sheet.paste(im,(x,y))
    sd.text((x+8,y+222),Path(feed[i]).name[:25],fill=(220,240,230),font=font(11))
sheet.save(PACK/'PREVIEW_CONTACT_SHEET.jpg',quality=92)

captions=[]
for day,(headline,body,pillar,src_idx) in enumerate(items,1):
    captions.append(f"## Day {day:02d} — {headline}\n\n{body}\n\nCTA: DM Stratos for a clean revenue-flow audit.\nBest use: Instagram feed / LinkedIn / sales follow-up.\nSource art: GPT Image 2 OAuth — {source_files[src_idx][1]}\n")
(PACK/'CAPTIONS.md').write_text('# Stratos GPT Image 2 Premium Content Series — Captions\n\n'+'\n'.join(captions))
(PACK/'CONTENT_CALENDAR.md').write_text('# 30-Day Premium Stratos Content Calendar\n\n'+'\n'.join([f"- Day {i:02d}: {h} — {pillar}" for i,(h,b,pillar,src_idx) in enumerate(items,1)]))
(PACK/'README.md').write_text(f'''# Stratos GPT Image 2 Premium Content Series\n\nBuilt from **6 GPT Image 2 OAuth source renders** with exact local Stratos typography overlays.\n\n## Contents\n\n- 30 premium feed posts: `assets/feed/`\n- 12 story/reel covers: `assets/stories/`\n- 4 carousel mini-decks / 20 slides: `assets/carousels/`\n- 6 simple motion reel covers: `videos/`\n- Captions/calendar/manifest/preview contact sheet\n\n## Production note\n\nThe generated source images intentionally contain no final Stratos logo/headline text. Final branding, headlines, CTAs, and offer language are composited locally for exact spelling, readability, and consistent Stratos quality.\n''')
manifest={
    'name':'Stratos GPT Image 2 Premium Content Series',
    'source_model':'gpt-image-2-medium via Hermes image_generate/openai-codex OAuth',
    'generated_source_renders':len(source_files),
    'feed_posts':len(feed),
    'stories':len(stories),
    'carousel_slides':len(carousel),
    'videos':len(list(VIDEOS.glob('*.mp4'))),
    'final_type':'local deterministic overlays for exact Stratos typography',
    'source_files':[{'file':f,'concept':c} for f,c in source_files]
}
(PACK/'manifest.json').write_text(json.dumps(manifest,indent=2))
zip_path=ROOT/'marketing-assets'/'stratos-gpt2-premium-content-series.zip'
if zip_path.exists(): zip_path.unlink()
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for p in PACK.rglob('*'):
        if p.is_file(): z.write(p,p.relative_to(PACK.parent))
print(json.dumps({**manifest,'zip':str(zip_path),'zip_mb':round(zip_path.stat().st_size/1024/1024,2)},indent=2))
