#!/usr/bin/env python3
"""Build Stratos premium GPT Image 2 OAuth content series with exact local overlays.

Quality pass rules:
- Original Stratos premium palette: black/ink, deep greens, cream/white, muted sage, gold.
- No visible day numbers on generated posts/stories/carousels/reels.
- Text boxes are measured, clamped, and trimmed to avoid overlap/cutoff.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import json, re, textwrap, zipfile, math
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

# Original Stratos premium palette.
BLACK=(3,6,5)        # near-black
INK=(10,16,13)       # black-green ink
GREEN=(20,88,56)     # #145838
GREEN2=(36,126,79)   # #247E4F
GREEN3=(85,174,116)  # #55AE74
WHITE=(248,250,246)  # warm white
CREAM=(238,240,232)  # cream
MUTED=(184,198,188)  # muted sage
GOLD=(211,199,160)   # restrained gold
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
BOLD='/System/Library/Fonts/Supplemental/Arial Bold.ttf'


def font(size,b=False):
    return ImageFont.truetype(BOLD if b else FONT,size)


def slug(s):
    return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')[:62]


def wrap_text(s, chars):
    return '\n'.join(textwrap.wrap(s, chars, break_long_words=False))


def text_box(draw, text, fnt, spacing=8):
    if not text:
        return (0,0,0,0)
    return draw.multiline_textbbox((0,0), text, font=fnt, spacing=spacing)


def text_size(draw, text, fnt, spacing=8):
    b=text_box(draw,text,fnt,spacing)
    return b[2]-b[0], b[3]-b[1]


def trim_to_fit(draw, wrapped, fnt, max_w, max_h, spacing):
    """Trim wrapped lines with an ellipsis until the text fits the box."""
    lines=wrapped.split('\n') if wrapped else []
    while lines and text_size(draw, '\n'.join(lines), fnt, spacing)[1] > max_h:
        lines.pop()
    if not lines:
        return ''
    out='\n'.join(lines)
    if out != wrapped:
        last=lines[-1].rstrip()
        while last and text_size(draw, '\n'.join(lines[:-1]+[last+'…']), fnt, spacing)[0] > max_w:
            last=last[:-1].rstrip()
        lines[-1]=(last+'…') if last else '…'
        out='\n'.join(lines)
    return out

def fit_wrapped(draw, text, max_w, max_h, start_size, min_size, bold=True, max_chars=28, spacing_ratio=.13):
    """Return (wrapped, size, spacing) that fits measured width/height, trimming as a last resort."""
    max_h=max(24, max_h)
    for size in range(start_size, min_size-1, -2):
        avg=max(8, size*.50)
        chars=max(9, min(max_chars, int(max_w/avg)))
        wrapped=wrap_text(text, chars)
        spacing=max(4, int(size*spacing_ratio))
        fnt=font(size,bold)
        w,h=text_size(draw, wrapped, fnt, spacing)
        if w <= max_w and h <= max_h:
            return wrapped, size, spacing
    size=min_size
    chars=max(8, int(max_w/(size*.55)))
    spacing=max(4,int(size*spacing_ratio))
    fnt=font(size,bold)
    wrapped=trim_to_fit(draw, wrap_text(text, chars), fnt, max_w, max_h, spacing)
    return wrapped, size, spacing


def draw_text(draw, xy, text, size, fill=WHITE, bold=False, anchor=None, spacing=8, align='left'):
    draw.multiline_text(xy, text, font=font(size,bold), fill=fill, anchor=anchor, spacing=spacing, align=align)


def rr(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def logo(draw, x, y, scale=1.0, dark=True):
    mark=int(58*scale)
    rr(draw, (x,y,x+mark,y+mark), int(16*scale), fill=GREEN2, outline=GREEN3, width=max(2,int(2*scale)))
    draw_text(draw, (x+mark/2,y+mark/2-1), 'S', int(32*scale), WHITE, True, 'mm')
    fill=WHITE if dark else INK
    draw_text(draw, (x+mark+16,y+1), 'STRATOS AI', int(26*scale), fill, True)
    draw_text(draw, (x+mark+18,y+34), 'WEBSITES • AUTOMATION • REVENUE', int(10*scale), GREEN3 if dark else GREEN, True)


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


def grade(im, darken=120, blur=0.20):
    """Restore the original Stratos art treatment: natural source render + dark premium veil."""
    im=ImageEnhance.Color(im).enhance(.82)
    im=ImageEnhance.Contrast(im).enhance(1.08)
    if blur:
        im=im.filter(ImageFilter.GaussianBlur(blur))
    overlay=Image.new('RGBA', im.size, (0,0,0,darken))
    return Image.alpha_composite(im.convert('RGBA'), overlay)

def diagonal_field(draw, w, h, seed=0):
    for i in range(8):
        y=110 + ((seed*53+i*155) % (h-220))
        x0=-120 + i*35
        x1=w+140
        col=GREEN3 if i%2==0 else GOLD
        draw.line((x0,y,x1,y-180), fill=(*col, 42), width=3)
    for i in range(6):
        x=80 + ((seed*97+i*167) % (w-160))
        y=120 + ((seed*41+i*211) % (h-240))
        rr(draw,(x,y,x+88,y+8),4,fill=(*GREEN3,62))


def panel(draw, box, variant=0, alpha=224):
    fill = (*BLACK, alpha) if variant % 2 == 0 else (*INK, alpha)
    outline = (*GREEN3, 115) if variant % 2 == 0 else (*GOLD, 105)
    rr(draw, box, 40, fill=fill, outline=outline, width=2)


def pill(draw, box, label, size=22):
    rr(draw, box, 999, fill=(*GREEN,238), outline=(*GREEN3,230), width=2)
    draw_text(draw, ((box[0]+box[2])/2,(box[1]+box[3])/2), label, size, WHITE, True, 'mm')


def card_copy(draw, rect, eyebrow, headline, body, mode=0, cta=None, logo_scale=1.0):
    """Draw a measured card. All vertical positions are derived from text bounds."""
    x1,y1,x2,y2=rect
    pad=42
    panel(draw, rect, mode, alpha=230)
    logo(draw, x1+pad, y1+pad, logo_scale)
    cursor=y1+pad+112
    draw_text(draw, (x1+pad, cursor), eyebrow.upper(), 20, WHITE, True)
    cursor += 54
    max_w=x2-x1-pad*2
    cta_h=86 if cta else 0
    cta_gap=30 if cta else 0
    remaining_bottom=y2-pad-cta_h-cta_gap
    available=max(120, remaining_bottom-cursor)
    headline_h=max(120, int(available*.48))
    wrapped, size, spacing = fit_wrapped(draw, headline, max_w, headline_h, 66, 40, True, 24)
    draw_text(draw, (x1+pad, cursor), wrapped, size, WHITE, True, spacing=spacing)
    _, hh=text_size(draw, wrapped, font(size,True), spacing)
    cursor += hh + 34
    body_h=max(42, remaining_bottom-cursor)
    wrapped_body, body_size, body_spacing = fit_wrapped(draw, body, max_w, body_h, 34, 23, False, 37, .24)
    draw_text(draw, (x1+pad, cursor), wrapped_body, body_size, WHITE, False, spacing=body_spacing)
    if cta:
        pill(draw, (x1+pad, y2-pad-70, x2-pad, y2-pad), cta, 22)


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

for folder in [FEED, STORIES, CAROUSELS, VIDEOS]:
    for p in folder.glob('*'):
        if p.is_file(): p.unlink()

feed=[]
for idx,(headline,body,pillar,src_idx) in enumerate(items,1):
    src=SOURCE/source_files[src_idx][0]
    im=grade(cover_image(src,(1080,1080)), darken=126 if idx%5 else 95, blur=.15)
    d=ImageDraw.Draw(im,'RGBA')
    diagonal_field(d,1080,1080,idx)
    mode=(idx-1)%6
    # No DAY label; the eyebrow only names the strategic pillar.
    if mode==0:
        card_copy(d,(70,532,1010,1000),pillar,headline,body,mode,cta='DM STRATOS FOR A CLEAN AUDIT')
    elif mode==1:
        card_copy(d,(58,58,716,996),pillar,headline,body,mode,cta=None)
        pill(d,(742,884,1010,948),'REVENUE FLOW',21)
    elif mode==2:
        card_copy(d,(364,58,1022,996),pillar,headline,body,mode,cta=None)
        pill(d,(70,884,338,948),'SYSTEM FIX',21)
    elif mode==3:
        card_copy(d,(82,78,998,610),pillar,headline,body,mode,cta=None,logo_scale=.92)
        pill(d,(118,884,720,952),'CAPTURE → ROUTE → FOLLOW UP',21)
    elif mode==4:
        card_copy(d,(90,90,990,990),pillar,headline,body,mode,cta='BOOK THE REVENUE FLOW AUDIT')
    else:
        panel(d,(64,64,1016,1016),mode,alpha=210)
        logo(d,104,104,1.0)
        draw_text(d,(104,232),pillar.upper(),20,WHITE,True)
        wrapped,size,spacing=fit_wrapped(d,headline,830,300,78,48,True,25)
        draw_text(d,(104,352),wrapped,size,WHITE,True,spacing=spacing)
        bwrap,bsize,bspacing=fit_wrapped(d,body,800,170,36,27,False,39,.26)
        draw_text(d,(108,706),bwrap,bsize,WHITE,False,spacing=bspacing)
        for n,label in enumerate(['Capture','Route','Book']):
            x=112+n*260; y=892
            rr(d,(x,y,x+190,y+62),26,fill=(*GREEN,238),outline=(*GREEN3,220),width=2)
            draw_text(d,(x+95,y+31),label,22,WHITE,True,'mm')
            if n<2: d.line((x+204,y+31,x+246,y+31),fill=(*GREEN3,220),width=4)
    out=FEED/f'post_{idx:02d}_{slug(headline)}.png'
    im.convert('RGB').save(out,quality=95)
    feed.append(out)

# Stories/reel covers: 12 high-impact verticals with measured lower panels.
story_indices=[0,1,2,3,4,5,6,10,14,20,26,29]
stories=[]
for n,idx0 in enumerate(story_indices,1):
    headline,body,pillar,src_idx=items[idx0]
    src=SOURCE/source_files[src_idx][0]
    crop='top' if 'medspa' in str(src).lower() else 'center'
    im=grade(cover_image(src,(1080,1920),crop), darken=132, blur=.12)
    d=ImageDraw.Draw(im,'RGBA')
    diagonal_field(d,1080,1920,n+40)
    panel(d,(56,66,1024,392),n,alpha=218)
    logo(d,92,106,1.15)
    draw_text(d,(92,282),f'{pillar.upper()} / PREMIUM SYSTEMS',22,WHITE,True)
    panel(d,(56,1040,1024,1718),n+1,alpha=236)
    max_w=856
    wrapped,size,spacing=fit_wrapped(d,headline,max_w,270,86,60,True,18)
    draw_text(d,(104,1118),wrapped,size,WHITE,True,spacing=spacing)
    _,hh=text_size(d,wrapped,font(size,True),spacing)
    bwrap,bsize,bspacing=fit_wrapped(d,body,max_w,145,43,33,False,31,.24)
    draw_text(d,(108,1118+hh+34),bwrap,bsize,WHITE,False,spacing=bspacing)
    pill(d,(104,1604,976,1686),'BOOK THE REVENUE FLOW AUDIT',30)
    out=STORIES/f'story_{n:02d}_{slug(headline)}.png'
    im.convert('RGB').save(out,quality=95)
    stories.append(out)

carousel_sets=[
('The Revenue Leak Audit',['Where intent enters','Where response slows','Where ownership disappears','Where follow-up dies','Where Stratos installs the path'],2),
('The Modern Front Office',['Website captures','Automation routes','Team gets context','Prospect gets next step','Owner sees outcome'],0),
('Premium Intake Playbook',['Fast first impression','One serious CTA','Instant qualification','Booked calls','Measured follow-up'],3),
('Enterprise Handoff Fix',['Fewer tabs','Cleaner ownership','Less waiting','More booked calls','One operating system'],1),
]
carousel=[]
for deck,(deck_title,slides,src_idx) in enumerate(carousel_sets,1):
    src=SOURCE/source_files[src_idx][0]
    for sidx,slide in enumerate(slides,1):
        im=grade(cover_image(src,(1080,1080)), darken=150 if sidx>1 else 116, blur=.22)
        d=ImageDraw.Draw(im,'RGBA')
        diagonal_field(d,1080,1080,deck*10+sidx)
        panel(d,(70,70,1010,1010),deck+sidx,alpha=225)
        logo(d,104,108,1.0)
        # Deck label only; no day numbering and no visible slide numbering.
        draw_text(d,(104,230),deck_title.upper(),23,WHITE,True)
        if sidx==1:
            wrapped,size,spacing=fit_wrapped(d,deck_title,830,280,90,60,True,16)
            draw_text(d,(104,352),wrapped,size,WHITE,True,spacing=spacing)
            draw_text(d,(108,728),'Swipe for the Stratos operating logic.',38,WHITE,False)
        else:
            wrapped,size,spacing=fit_wrapped(d,slide,810,245,94,62,True,15)
            draw_text(d,(104,358),wrapped,size,WHITE,True,spacing=spacing)
            body_line=f'This is where Stratos turns scattered intent into a cleaner revenue path.'
            bwrap,bsize,bspacing=fit_wrapped(d,body_line,800,160,38,29,False,34,.24)
            draw_text(d,(108,690),bwrap,bsize,WHITE,False,spacing=bspacing)
        pill(d,(104,876,700,948),'STRATOS SYSTEMS',27)
        out=CAROUSELS/f'deck_{deck:02d}_slide_{sidx:02d}_{slug(slide)}.png'
        im.convert('RGB').save(out,quality=95)
        carousel.append(out)

video_specs=[
('website-is-your-operator',items[0],0),
('handoff-leak',items[1],1),
('disconnected-tools',items[2],2),
('medspa-after-hours',items[3],3),
('booked-calls',items[4],4),
('clean-workflow',items[5],5),
]
for vid,(name,(headline,body,pillar,src_idx),src_idx) in enumerate(video_specs,1):
    src=SOURCE/source_files[src_idx][0]
    base=grade(cover_image(src,(1080,1920),'center'), darken=134, blur=.12)
    d=ImageDraw.Draw(base,'RGBA')
    diagonal_field(d,1080,1920,vid+80)
    panel(d,(56,80,1024,820),vid,alpha=224)
    logo(d,92,124,1.12)
    wrapped,size,spacing=fit_wrapped(d,headline,850,260,78,55,True,18)
    draw_text(d,(92,314),wrapped,size,WHITE,True,spacing=spacing)
    _,hh=text_size(d,wrapped,font(size,True),spacing)
    bwrap,bsize,bspacing=fit_wrapped(d,body,850,170,38,29,False,32,.26)
    draw_text(d,(96,314+hh+36),bwrap,bsize,WHITE,False,spacing=bspacing)
    pill(d,(72,1648,1008,1728),'STRATOS AI / REVENUE FLOW AUDIT',27)
    frames=[]
    for f in range(105):
        frame=base.copy()
        od=ImageDraw.Draw(frame,'RGBA')
        offset=f*5
        od.line((90+offset%840,1518,420+offset%840,1518),fill=(*GREEN3,170),width=7)
        od.ellipse((72+(offset*2)%920,1486,94+(offset*2)%920,1508),fill=(*GREEN,210))
        frames.append(np.array(frame.convert('RGB')))
    imageio.mimsave(VIDEOS/f'reel_{vid:02d}_{name}.mp4',frames,fps=25,quality=8,macro_block_size=1)

# Preview contact sheet — clean/client-facing, no filenames or visible numbering.
thumbs=[Image.open(p).resize((216,216)) for p in feed[:20]]
sheet=Image.new('RGB',(1080,864),BLACK)
for i,im in enumerate(thumbs):
    x=(i%5)*216; y=(i//5)*216
    sheet.paste(im,(x,y))
sheet.save(PACK/'PREVIEW_CONTACT_SHEET.jpg',quality=92)

captions=[]
for idx,(headline,body,pillar,src_idx) in enumerate(items,1):
    captions.append(f"## Post {idx:02d} — {headline}\n\n{body}\n\nCTA: DM Stratos for a clean revenue-flow audit.\nBest use: Instagram feed / LinkedIn / sales follow-up.\nSource art: GPT Image 2 OAuth — {source_files[src_idx][1]}\n")
(PACK/'CAPTIONS.md').write_text('# Stratos GPT Image 2 Premium Content Series — Captions\n\n'+'\n'.join(captions))
(PACK/'CONTENT_CALENDAR.md').write_text('# Premium Stratos Content Calendar\n\n'+'\n'.join([f"- Post {i:02d}: {h} — {pillar}" for i,(h,b,pillar,src_idx) in enumerate(items,1)]))
(PACK/'README.md').write_text(f'''# Stratos GPT Image 2 Premium Content Series\n\nBuilt from **6 GPT Image 2 OAuth source renders** with exact local Stratos typography overlays.\n\n## Brand palette\n\n- Base: near-black `#030605` / ink `#0A100D`\n- Accent: deep green `#145838`, green `#247E4F`, signal green `#55AE74`\n- Text: warm white `#F8FAF6`, cream `#EEF0E8`, muted sage `#B8C6BC`, restrained gold `#D3C7A0`\n\n## Quality pass\n\n- Removed visible day numbers from posts.\n- Rebuilt posts, stories, carousels, and motion covers with measured text boxes to prevent overlap.\n- Kept all final typography deterministic/local for exact Stratos spelling and mobile readability.\n\n## Contents\n\n- 30 premium feed posts: `assets/feed/`\n- 12 story/reel covers: `assets/stories/`\n- 4 carousel mini-decks / 20 slides: `assets/carousels/`\n- 6 simple motion reel covers: `videos/`\n- Captions/calendar/manifest/preview contact sheet\n\n## Production note\n\nThe generated source images intentionally contain no final Stratos logo/headline text. Final branding, headlines, CTAs, and offer language are composited locally for exact spelling, readability, and consistent Stratos quality.\n''')
manifest={
    'name':'Stratos GPT Image 2 Premium Content Series',
    'source_model':'gpt-image-2-medium via Hermes image_generate/openai-codex OAuth',
    'generated_source_renders':len(source_files),
    'feed_posts':len(feed),
    'stories':len(stories),
    'carousel_slides':len(carousel),
    'videos':len(list(VIDEOS.glob('*.mp4'))),
    'final_type':'local deterministic overlays for exact Stratos typography',
    'palette':{'base':['#030605','#0A100D'],'accent':['#145838','#247E4F','#55AE74'],'text':['#F8FAF6','#EEF0E8','#B8C6BC'],'highlight':'#D3C7A0'},
    'quality_pass':['removed visible day numbers','measured text boxes to avoid overlap','rebuilt all posts stories carousels and motion covers'],
    'source_files':[{'file':f,'concept':c} for f,c in source_files]
}
(PACK/'manifest.json').write_text(json.dumps(manifest,indent=2))
zip_path=ROOT/'marketing-assets'/'stratos-gpt2-premium-content-series.zip'
if zip_path.exists(): zip_path.unlink()
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for p in PACK.rglob('*'):
        if p.is_file(): z.write(p,p.relative_to(PACK.parent))
print(json.dumps({**manifest,'zip':str(zip_path),'zip_mb':round(zip_path.stat().st_size/1024/1024,2)},indent=2))
