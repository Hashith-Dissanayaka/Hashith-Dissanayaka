from PIL import Image,ImageDraw,ImageFont,ImageOps
from pathlib import Path
import math,functools,os
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'assets/atlas'; W=1000; N=32
BG='#141a20'; PANEL='#1d272e'; LINE='#37454b'; INK='#f5f7f2'; MUT='#a7b8ba'; LIME='#cefa84'; LAV='#b5aaff'; CYAN='#83ded3'
@functools.lru_cache(None)
def f(s,w='Regular'):
 try:return ImageFont.truetype(os.environ.get('ATLAS_FONT_DIR','/usr/share/fonts/opentype/inter')+f'/Inter-{w}.otf',s)
 except OSError:return ImageFont.truetype('DejaVuSans.ttf',s)
def tx(d,x,y,s,z=20,c=INK,w='Regular',a=None):d.text((x,y),s,font=f(z,w),fill=c,anchor=a)
def box(d,x,y,w,h,fill=PANEL,edge=LINE,r=14):d.rounded_rectangle((x,y,x+w,y+h),r,fill,edge)
def dot(d,x,y,r,c):d.ellipse((x-r,y-r,x+r,y+r),fill=c)
def blend(a,b,t):return tuple(round(x+(y-x)*t) for x,y in zip(bytes.fromhex(a[1:]),bytes.fromhex(b[1:])))
def pulse(t,i,n):return (.5+.5*math.cos(math.tau*(t-i/n)))**6
def top(d,no,label,title):
 tx(d,32,25,no,15,LIME,'SemiBold');tx(d,76,25,label,15,MUT,'Medium');tx(d,32,58,title,32,INK,'Bold')
def track(d,h,t):
 y=h-18;d.line((32,y,968,y),LINE,2);x=32+int(t*890);d.line((x,y,x+46,y),LIME,2)
def hero(im,d,t):
 tx(d,32,27,'ATLAS / DIGITAL CRAFT',16,LIME,'SemiBold');tx(d,965,27,'DEVELOPER PORTFOLIO  /  LK',15,MUT,'Medium','ra');d.line((32,60,968,60),LINE)
 tx(d,32,88,'Hashith',65,INK,'Bold');tx(d,32,158,'Dissanayaka.',65,INK,'Bold');tx(d,37,246,'FULL STACK DEVELOPER',23,LIME,'SemiBold');tx(d,37,290,'Thoughtful interfaces. Reliable systems.',19,MUT);tx(d,37,318,'Code built for the real world.',19,MUT)
 a=t*math.tau;cx,cy=780,220;scale=127
 def p(lat,lon):
  r=1+.14*math.sin(3*lon+2*lat+a)*math.cos(lat)**2;x=r*math.cos(lat)*math.cos(lon+a);y=r*math.sin(lat);z=r*math.cos(lat)*math.sin(lon+a);y,z=y*.94-z*.34,y*.34+z*.94;k=1/(1-.17*z);return (cx+x*scale*k,cy+y*scale*k,z)
 for j in range(11):
  pts=[p(-1.42+j*2.84/10,k*math.tau/64) for k in range(65)]
  for u,v in zip(pts,pts[1:]):d.line((u[:2],v[:2]),blend('#2a3c3c',LIME,max(0,(u[2]+1)/2)**2),2)
 for j in range(16):
  pts=[p(-math.pi/2+k*math.pi/40,j*math.tau/16) for k in range(41)]
  for u,v in zip(pts,pts[1:]):d.line((u[:2],v[:2]),blend('#293a42',CYAN,max(0,(u[2]+1)/2)**2),1)
 for r in [-.5,.52]:
  pts=[(cx+172*math.cos(q)*math.cos(r)-52*math.sin(q)*math.sin(r),cy+172*math.cos(q)*math.sin(r)+52*math.sin(q)*math.cos(r)) for q in [k*math.tau/120 for k in range(121)]];d.line(pts,'#536668',1);dot(d,*pts[int(((t+r)%1)*120)],4,LAV)
 if (OUT/'portrait.png').exists():
  photo=ImageOps.fit(Image.open(OUT/'portrait.png').convert('RGB'),(62,62));mask=Image.new('L',(62,62));ImageDraw.Draw(mask).ellipse((0,0,61,61),fill=255);d.ellipse((901,77,971,147),outline=LAV,width=2);im.paste(photo,(905,81),mask)
 d.line((32,369,968,369),LINE);dot(d,42,397,4+math.sin(a),LIME);tx(d,56,397,'DESIGN / DEVELOP / DELIVER',15,MUT,'Medium','lm');tx(d,965,397,'01 — ∞',17,LIME,'Medium','rm');track(d,440,t)
FOCUS=[('Web development','Interfaces & experiences'),('Software development','Systems & applications'),('Mobile app development','Portable experiences'),('Cyber security','Security-minded engineering'),('UI/UX design','Human-centered design'),('Database management','Structured information'),('DevOps','Delivery & automation'),('Open source','Collaborative development'),('Game development','Interactive experiences')]
def focus(im,d,t):
 top(d,'01','WHAT I DO','Ideas into useful products.')
 for i,(n,desc) in enumerate(FOCUS):
  x=32+i%3*315;y=121+i//3*82;q=pulse(t,i,9);box(d,x,y,301,70,blend(PANEL,'#354838',q*.7));tx(d,x+13,y+11,f'{i+1:02}',13,LIME,'Medium');tx(d,x+42,y+9,n,17,INK,'SemiBold');tx(d,x+42,y+37,desc,14,MUT);d.line((x+13,y+55,x+13+int(18+12*q),y+55),blend(LINE,LIME,q),2)
 track(d,386,t)
LANG=[('HTML','html','#ff9064'),('CSS','css','#87aeff'),('JavaScript','javascript','#f6db77'),('React','react','#6fdef1'),('Java','java','#ffb19a'),('C#','csharp','#b6aaff'),('Python','python','#81c9ff'),('C','c','#96b8f8'),('SQL','sql','#81e0c9')]
def stack(im,d,t):
 top(d,'02','TECHNOLOGY STACK','A toolkit for every layer.')
 for i,(n,k,c) in enumerate(LANG):
  x=32+i*104;y=123;q=pulse(t,i,9);box(d,x,y,96,125,blend(PANEL,'#344640',q*.55));p=OUT/f'icon-{k}.png'
  if p.exists():
   ico=Image.open(p).convert('RGBA').resize((57,57),Image.Resampling.LANCZOS);im.paste(ico,(x+19,y+12),ico)
  else:tx(d,x+48,y+41,n,22,c,'Bold','mm')
  tx(d,x+48,y+90,n,14,INK,'SemiBold','mm');d.line((x+12,y+108,x+84,y+108),LINE,2);d.line((x+12,y+108,x+12+int(72*q),y+108),c,2)
 tx(d,32,278,'FRONTEND  /  BACKEND  /  DATA  /  SYSTEMS',15,MUT,'Medium');track(d,316,t)
TOOLS=['Git','GitHub','VS Code','Visual Studio','Figma','MySQL','Node.js','Bootstrap','.NET','SQL Server','IntelliJ IDEA','Linux','Unity']
def tools(im,d,t):
 top(d,'03','TOOLS & PLATFORMS','The tools behind the build.')
 for i,n in enumerate(TOOLS):
  x=32+i%5*188;y=122+i//5*50;q=pulse(t,i,13);box(d,x,y,177,39,blend(PANEL,'#39483a',q*.65),LINE,20);dot(d,x+17,y+20,3,blend('#657779',LIME,q));tx(d,x+29,y+20,n,15,INK,'Medium','lm')
 track(d,287,t)
def work(im,d,t):
 top(d,'04','SELECTED WORK','Building across platforms.');tx(d,966,70,'CONCEPT VISUALS',13,MUT,'Medium','ra')
 for i,(name,desc,c) in enumerate([('Websites','Web development',CYAN),('City Management','Desktop application',LAV),('Mobile apps','Mobile development',LIME)]):
  x=32+i*316;y=119;box(d,x,y,302,221);box(d,x+14,y+14,274,126,'#111a20',LINE,9);a=t*math.tau+i*1.7;dy=int(6*math.sin(a))
  if i==0:
   box(d,x+34,y+29,235,96,'#293840',None,7);d.line((x+34,y+44,x+269,y+44),LINE);[dot(d,x+44+j*9,y+37,2,MUT) for j in range(3)];box(d,x+48,y+57,83,8,c,None,3);box(d,x+48,y+76,67,5,MUT,None,2);box(d,x+48,y+91,54,5,MUT,None,2);box(d,x+150,y+53+dy,103,58,'#3c5652',None,7);d.line([(x+159,y+99+dy),(x+184,y+70+dy),(x+204,y+90+dy),(x+239,y+62+dy)],c,2)
  elif i==1:
   box(d,x+34,y+29,235,96,'#29313f',None,6);box(d,x+41,y+36,42,81,'#161e28',None,4)
   for j in range(4):box(d,x+49,y+47+j*16,27,4,c if j==1 else MUT,None,2)
   for j in range(3):box(d,x+92+j*55,y+43,46,17,'#46425e',None,4)
   for j in range(7):
    bh=12+int(25*(.5+.5*math.sin(a+j*.8)));box(d,x+100+j*21,y+112-bh,10,bh,c,None,2)
  else:
   for j in range(2):
    xx=x+78+j*85;yy=y+22+int(5*math.sin(a+j*1.7));box(d,xx,yy,63,108,'#293c32',c,11);box(d,xx+7,yy+13,49,25,'#4e6245',None,5);box(d,xx+7,yy+46,49,9,c,None,3);box(d,xx+7,yy+65,49,4,MUT,None,2);box(d,xx+7,yy+75,37,4,MUT,None,2)
  tx(d,x+16,y+153,name,22,INK,'SemiBold');tx(d,x+16,y+186,desc,15,MUT)
 track(d,378,t)
def git(im,d,t):
 top(d,'05','GIT / VERSION CONTROL','From the first commit to release.');tx(d,966,72,'WORKFLOW / ILLUSTRATION',13,MUT,'Medium','ra')
 y=192;by=137;route=[(95,y),(238,y),(266,y),(315,by),(542,by),(575,by),(630,y),(695,y),(870,y)];d.line((95,y,870,y),'#60766a',3);d.line(route[1:-1],LAV,3,joint='curve')
 for x,yy,n,c in [(95,y,'init',LIME),(238,y,'branch',LIME),(390,by,'commit',LAV),(542,by,'review',LAV),(695,y,'merge',LIME),(870,y,'release',LIME)]:dot(d,x,yy,8,c);dot(d,x,yy,4,BG);tx(d,x,yy-25 if yy==by else yy+27,n,15,INK,'Medium','mm')
 ds=[0]
 for a,b in zip(route,route[1:]):ds.append(ds[-1]+math.dist(a,b))
 k=t*ds[-1]
 for j in range(len(ds)-1):
  if ds[j]<=k<ds[j+1]:
   u=(k-ds[j])/(ds[j+1]-ds[j]);x=route[j][0]+u*(route[j+1][0]-route[j][0]);yy=route[j][1]+u*(route[j+1][1]-route[j][1]);dot(d,x,yy,8,LIME);dot(d,x,yy,3,INK);break
 tx(d,32,269,'BRANCHING  /  MERGING  /  REBASING  /  COLLABORATION',15,MUT,'Medium');track(d,315,t)
def goal(im,d,t):
 tx(d,32,25,'07 / WHAT COMES NEXT',15,LIME,'SemiBold');tx(d,32,62,'Build something that matters.',32,INK,'Bold');tx(d,32,112,'From developer to software company founder.',19,MUT)
 for i in range(4):
  yy=35+i*33;d.line([(660,yy),(741,yy),(790,85),(934,85)],LINE,2);x=660+274*((t+i/4)%1);y=yy+(85-yy)*min(1,max(0,(x-741)/49));dot(d,x,y,4,LIME if i%2==0 else LAV)
 dot(d,947,85,18,LIME);tx(d,947,85,'↗',21,BG,'Bold','mm');track(d,170,t)
def save(name,h,fun):
 frames=[]
 for i in range(N):
  im=Image.new('RGB',(W,h),'#10151a');d=ImageDraw.Draw(im);box(d,1,1,W-3,h-3,BG,LINE,22);fun(im,d,i/N)
  frames.append(im.quantize(colors=128,dither=Image.Dither.NONE))
 frames[0].save(OUT/(name+'.gif'),save_all=True,append_images=frames[1:],duration=110,loop=0,optimize=True,disposal=1);frames[0].convert('RGB').save(OUT/(name+'-still.png'));print(name,flush=True)
if __name__=='__main__':
 for n,h,fn in [('hero',440,hero),('focus',386,focus),('stack',316,stack),('tools',287,tools),('work',378,work),('git',315,git),('goal',170,goal)]:save(n,h,fn)
