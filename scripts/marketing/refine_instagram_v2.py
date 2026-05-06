from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import textwrap, random, re, json, imageio.v2 as imageio, numpy as np, zipfile
ROOT=Path('/Users/bradleydipaolo/stratos-ai/instagram-month-pack-v2')
BLACK=(3,6,5); INK=(10,16,13); GREEN=(20,88,56); GREEN2=(36,126,79); GREEN3=(85,174,116); WHITE=(248,250,246); CREAM=(238,240,232); MUTED=(174,190,180)
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'; BOLD='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def font(s,b=False): return ImageFont.truetype(BOLD if b else FONT,s)
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')[:48]
def wrap(s,w): return '\n'.join(textwrap.wrap(s,w,break_long_words=False))
def text(d,xy,s,size,fill=WHITE,b=False,anchor=None,spacing=7,align='left'): d.multiline_text(xy,s,font=font(size,b),fill=fill,anchor=anchor,spacing=spacing,align=align)
def rr(d,box,r,fill,outline=None,width=1): d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=width)
def logo(d,x,y,scale=1,dark=True):
    mark=int(52*scale); rr(d,(x,y,x+mark,y+mark),14,fill=GREEN2,outline=GREEN3,width=2)
    text(d,(x+mark/2,y+mark/2-1),'S',int(30*scale),WHITE,True,'mm')
    fill=WHITE if dark else INK
    text(d,(x+mark+14,y+2),'STRATOS AI',int(25*scale),fill,True)
    text(d,(x+mark+16,y+32),'WEBSITES • AUTOMATION • REVENUE',int(10*scale),GREEN3 if dark else GREEN,True)
def bg(size,dark=True,seed=1,photo=False):
    hero=ROOT/'higgsfield/premium_reception_workflow.png'
    if photo and hero.exists():
        im=Image.open(hero).convert('RGB'); sw,sh=im.size; tw,th=size; sc=max(tw/sw,th/sh); im=im.resize((int(sw*sc),int(sh*sc)),Image.LANCZOS); nw,nh=im.size; im=im.crop(((nw-tw)//2,(nh-th)//2,(nw+tw)//2,(nh+th)//2)); im=ImageEnhance.Color(im).enhance(.35); im=ImageEnhance.Contrast(im).enhance(1.08); im=im.filter(ImageFilter.GaussianBlur(.35)); layer=Image.new('RGBA',size,(0,0,0,135)); return Image.alpha_composite(im.convert('RGBA'),layer)
    im=Image.new('RGBA',size,BLACK if dark else CREAM); d=ImageDraw.Draw(im,'RGBA'); w,h=size; random.seed(seed)
    grid=(255,255,255,8) if dark else (20,60,40,10)
    for x in range(0,w,120): d.line((x,0,x,h),fill=grid,width=1)
    for y in range(0,h,120): d.line((0,y,w,y),fill=grid,width=1)
    # restrained proprietary visual language: fine flow lines, not blobs everywhere
    for i in range(3):
        y=random.randint(690,h-160); d.line((90,y,random.randint(650,w-70),y+random.randint(-70,70)),fill=(85,174,116,70),width=3)
        d.ellipse((78,y-7,92,y+7),fill=(85,174,116,150)); d.ellipse((w-120,y-5,w-110,y+5),fill=(85,174,116,110))
    if seed%4==0:
        d.ellipse((w-300,-130,w+180,350),fill=(20,88,56,38 if dark else 25))
    return im
items=[
('Your website should act like your best operator.','Not a brochure. A clean system for capturing demand, routing next steps, and following up while the team is busy.','SYSTEMS','photo'),
('Large firms lose money in tiny handoffs.','The lead submitted the form. The call was missed. The next step waited. Stratos closes those gaps.','ENTERPRISE FRICTION','dark'),
('Disconnected tools leak revenue.','Ads, website, CRM, calendar, inbox, and sales ops should not behave like separate businesses.','INTEGRATION','diagram'),
('Your website is the new front desk.','If intake feels slow, confusing, or generic, the prospect already has a reason to keep shopping.','POSITIONING','light'),
('Speed is a brand asset.','The fastest serious business often feels like the most professional one.','FOLLOW-UP','photo'),
('AI should disappear into the workflow.','No gimmicks. Just cleaner routing, faster answers, booked calls, and fewer manual touches.','AUTOMATION','dark'),
('A premium firm needs premium intake.','Before the first consultation, the experience should already feel organized, fast, and high-trust.','PROFESSIONAL FIRMS','light'),
('Missed calls should trigger follow-up.','Text-back, qualification, scheduling, review requests, and owner alerts should start instantly.','LOCAL SERVICES','dark'),
('Stop buying traffic for a broken system.','More visitors only help if the business captures intent and creates one clear next step.','CONVERSION','light'),
('Your CRM is not the strategy.','A database does not create revenue unless the workflow around it is alive.','CRM','dark'),
('Every lead deserves a next step.','Stratos connects attention, trust, contact, follow-up, and closed revenue.','LEAD OPS','photo'),
('Make the business easier to buy from.','Simple message. Fast response. Clear offer. One obvious path to action.','CLARITY','light'),
('The best automations feel human.','They do not replace service. They protect it from silence, delay, and dropped handoffs.','HUMAN AI','dark'),
('Modernize before the market notices.','By the time competitors copy the website, your systems should already be compounding.','ADVANTAGE','diagram'),
('If the team is busy, the system should still sell.','Nights, weekends, and follow-up windows are where revenue disappears.','OPERATIONS','light'),
('Your site should qualify, not just impress.','Beautiful design opens trust. Smart flows turn that trust into conversations.','WEBSITES','photo'),
('One clean path beats ten scattered buttons.','Complex firms need simple choices for prospects, not an obstacle course.','UX','dark'),
('Follow-up is where premium brands separate.','The second touch often matters more than the first click.','SALES','dark'),
('Outdated intake makes big firms look small.','When a serious prospect has to chase the business, the brand loses leverage.','LARGE FIRMS','light'),
('Your best employee should not be the only system.','If everything depends on memory, tabs, and manual reminders, the business is leaking.','PROCESS','light'),
('Make the invisible measurable.','Response time, source, next step, owner, and outcome should be obvious.','METRICS','diagram'),
('Your online presence should feel expensive.','Not loud. Not complicated. Clear, fast, polished, and built to convert.','BRAND','dark'),
('Integrate the tools before adding more.','Most businesses do not need another app. They need the current stack to finally talk.','STACK','dark'),
('The agency is not selling websites.','Stratos sells the modern front office: design, automation, and revenue flow.','STRATOS','photo'),
('Turn interest into scheduled action.','A serious website makes the next step obvious and helps the team follow through.','BOOKING','light'),
('Local businesses deserve enterprise systems.','Medspas, dental offices, service brands, and firms can operate with the speed of much bigger teams.','LOCAL','light'),
('The buyer journey should not depend on office hours.','Good systems keep moving when the staff is with clients, in meetings, or offline.','24/7','dark'),
('Revenue leaks rarely announce themselves.','They hide in missed calls, slow replies, unclear offers, and handoffs nobody owns.','AUDIT','diagram'),
('Less dashboard. More outcome.','The point is making the business easier to run and easier to choose.','SIMPLICITY','dark'),
('Build the system customers feel.','From first impression to follow-up, Stratos makes the business sharper and more trustworthy.','CLOSE','photo')]
# clear feed
for p in (ROOT/'assets/feed').glob('*.png'): p.unlink()
feed=[]
for day,(h,b,pillar,style) in enumerate(items,1):
    dark=style not in ['light']; im=bg((1080,1080),dark,day,style=='photo'); d=ImageDraw.Draw(im,'RGBA')
    fg=WHITE if dark else INK; muted=MUTED if dark else (60,78,67); accent=GREEN3 if dark else GREEN
    # content safe panel to kill clutter and protect type
    panel=(0,0,0,128) if dark else (248,250,246,216)
    rr(d,(52,44,752,1018),36,fill=panel,outline=(85,174,116,55),width=1)
    logo(d,78,70,1.0,dark); text(d,(78,185),f'DAY {day:02d} / {pillar}',18,accent,True)
    text(d,(78,266),wrap(h,17),68 if len(h)<44 else 60,fg,True,spacing=2)
    text(d,(82,590),wrap(b,31),29,muted,False,spacing=10)
    # unique structure cue instead of repetitive bullets on every card
    if day%3==0:
        rr(d,(82,765,700,868),28,fill=(20,88,56,235),outline=GREEN3,width=2)
        text(d,(112,800),'SYSTEM FIX',20,WHITE,True); text(d,(112,830),'Design → Intake → Follow-up',27,WHITE,True)
    elif day%3==1:
        for i,pt in enumerate(['Capture','Route','Follow up']):
            x=92+i*190; d.ellipse((x,790,x+54,844),fill=GREEN); text(d,(x+27,817),str(i+1),25,WHITE,True,'mm'); text(d,(x,862),pt,22,fg,True)
            if i<2: d.line((x+64,817,x+170,817),fill=GREEN3,width=4)
    else:
        text(d,(82,790),'Revenue leak → clean workflow',30,fg,True); d.line((82,845,650,845),fill=GREEN3,width=5)
    if day%4!=0:
        rr(d,(78,948,704,1000),26,fill=GREEN if dark else INK,outline=GREEN3,width=2); text(d,(391,974),'DM STRATOS FOR A CLEAN AUDIT',19,WHITE,True,'mm')
    else:
        text(d,(82,956),'STRATOS AI / MODERN FRONT OFFICE',22,accent,True)
    out=ROOT/'assets/feed'/f'day_{day:02d}_{slug(h)}.png'; im.convert('RGB').save(out,quality=95); feed.append(out)
# preview
imgs=[Image.open(p).resize((270,270)) for p in feed[:12]]; sheet=Image.new('RGB',(1080,930),BLACK); sd=ImageDraw.Draw(sheet)
for idx,im in enumerate(imgs):
    x=(idx%4)*270; y=(idx//4)*310; sheet.paste(im,(x,y)); sd.text((x+8,y+275),Path(feed[idx]).name[:30],fill=(220,240,230),font=font(12))
sheet.save(ROOT/'PREVIEW_CONTACT_SHEET.jpg',quality=90)
# rerender videos from refined posts
for p in (ROOT/'videos').glob('*.mp4'): p.unlink()
scripts=[('Your website is not the system','It is the front door. Stratos connects the front door to follow-up, scheduling, and revenue.'),('Big firms lose in small gaps','Departments, inboxes, tools, and forms create silent friction. Stratos simplifies the path.'),('Missed calls are revenue leaks','After-hours should trigger text-back, qualification, alerts, and booking.'),('Simple feels premium','The best digital systems are easy to understand and fast to act on.'),('AI without the gimmick','Stratos uses automation to protect service, not replace it.'),('Build the system customers feel','From first click to follow-up, make the business sharper and easier to choose.')]
for idx,(h,b) in enumerate(scripts,1):
    base=Image.open(feed[(idx-1)*4]).resize((1080,1080)).convert('RGBA')
    canvas=Image.new('RGBA',(1080,1920),BLACK); canvas.paste(base,(0,360)); od=ImageDraw.Draw(canvas,'RGBA'); od.rectangle((0,0,1080,1920),fill=(0,0,0,90)); logo(od,78,110,1.15,True); text(od,(78,360),wrap(h,15),86,WHITE,True,spacing=4); text(od,(84,740),wrap(b,28),40,MUTED,False,spacing=12); rr(od,(78,1640,1002,1718),39,GREEN,GREEN3,2); text(od,(540,1680),'STRATOS AI / REVENUE FLOW AUDIT',27,WHITE,True,'mm')
    frames=[]
    for f in range(125):
        frame=canvas.copy(); ld=ImageDraw.Draw(frame,'RGBA'); x=int(80+f*2.0); ld.line((x,1510,x+420,1510),fill=(85,174,116,160),width=6); frames.append(np.array(frame.convert('RGB')))
    imageio.mimsave(ROOT/'videos'/f'reel_{idx:02d}_{slug(h)}.mp4',frames,fps=25,quality=8,macro_block_size=1)
# zip
zip_path=Path('/Users/bradleydipaolo/stratos-ai/instagram-month-pack-v2.zip')
if zip_path.exists(): zip_path.unlink()
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for p in ROOT.rglob('*'):
        if p.is_file(): z.write(p,p.relative_to(ROOT.parent))
print(json.dumps({'refined':True,'feed_posts':len(feed),'zip':str(zip_path),'size_mb':round(zip_path.stat().st_size/1024/1024,2)},indent=2))
