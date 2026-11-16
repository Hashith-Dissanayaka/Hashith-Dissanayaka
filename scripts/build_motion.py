from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math
P=Path(__file__).resolve().parents[1]/'assets/prism'; P.mkdir(parents=True,exist_ok=True)
W=1000; N=36; BG='#151523'; PAPER='#f4f2ed'; INK='#19192b'; LAV='#b9b5ff'; ACC='#c4ff66'; MUT='#aaa9bf'; T=math.tau
fonts={}
def f(s,w='Regular'):
 if (s,w) not in fonts: fonts[s,w]=ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{w}.otf',s)
 return fonts[s,w]
def txt(d,xy,s,size=20,fill=INK,w='Regular',anchor=None):d.text(xy,s,font=f(size,w),fill=fill,anchor=anchor)
def base(h,bg=BG):
 im=Image.new('RGB',(W,h),bg);return im,ImageDraw.Draw(im)
def label(d,n,s,col=MUT):
 txt(d,(36,22),n+'  /  '+s,16,col,'Medium');txt(d,(962,22),'HD  /  PORTFOLIO',14,col,'Medium','ra')
def ring(d,x,y,r,c,w=1):d.ellipse((x-r,y-r,x+r,y+r),outline=c,width=w)
def hero(t):
 im,d=base(438); label(d,'00','INDEPENDENT DEVELOPER')
 for i in range(8):ring(d,778,215,85+i*12,(30+i*3,30+i*3,52+i*5))
 pts=[]
 for a in range(60):
  u=T*a/60
  for b in range(20):
   v=T*b/20;r=1.22+.51*math.cos(v);x=r*math.cos(u);y=r*math.sin(u);z=.51*math.sin(v);th=.7+.24*math.sin(t)
   y,z=y*math.cos(th)-z*math.sin(th),y*math.sin(th)+z*math.cos(th); x,z=x*math.cos(t)+z*math.sin(t),-x*math.sin(t)+z*math.cos(t)
   p=2.9/(4.2-z);pts.append((z,778+x*p*142,215+y*p*142))
 for z,x,y in sorted(pts):
  q=max(0,min(1,(z+2)/4));c=(int(88+120*q),int(80+118*q),int(188+66*q));r=1.2+1.1*q;d.ellipse((x-r,y-r,x+r,y+r),fill=c)
 txt(d,(36,76),'HASHITH',90,PAPER,'Bold');txt(d,(36,168),'DISSANAYAKA',66,PAPER,'Bold');txt(d,(39,255),'Full Stack Developer',35,LAV,'Medium');txt(d,(40,309),'Design with intent. Build with purpose.',21,'#d6d4e1')
 d.line((36,374,964,374),fill='#45465c');d.ellipse((39,397,49,407),fill=ACC);txt(d,(64,390),'WEB  /  SOFTWARE  /  MOBILE',16,PAPER,'Medium');txt(d,(960,390),'SL  /  01—∞',16,LAV,'Medium','ra');return im
def focus(t):
 im,d=base(184,PAPER);label(d,'01','WHAT I DO','#66677b');txt(d,(36,54),'Ideas, made usable.',47,INK,'Bold')
 for i,(x,s) in enumerate(zip([36,350,664],['DESIGN','DEVELOP','DELIVER'])):
  d.line((x,130,x+275,130),fill='#cbc8dd',width=2);d.line((x,130,x+40+235*(math.sin(t+i*2)+1)/2,130),fill='#6b61e8',width=4);txt(d,(x,145),s,20,INK,'SemiBold')
 return im
def stack(t):
 im,d=base(235);label(d,'02','TECHNOLOGIES')
 for i,(s,c) in enumerate(zip(['HTML','CSS','JavaScript','React','Java','C#','Python','C','SQL'],['#ff885d','#75b4ff','#ffe16e','#7ae8f5','#ffac87','#c8a9ff','#ffe16e','#9ebaff','#a7dbff'])):
  x=36+(i%3)*317;y=62+(i//3)*54;a=(1+math.sin(t-i*.65))/2;d.line((x,y+42,x+287,y+42),fill='#34364a');d.ellipse((x,y+13,x+8,y+21),fill=c);txt(d,(x+20,y+3),s,28,PAPER,'SemiBold');d.line((x,y+42,x+20+int(85*a),y+42),fill=c,width=3)
 return im
def work(t):
 im,d=base(298,PAPER);label(d,'03','SELECTED WORK','#66677b')
 for i,(name,sub) in enumerate([('Web','Interfaces'),('City','Desktop systems'),('Mobile','Applications')]):
  x=36+i*312;y=64;c=[LAV,ACC,'#f7b2db'][i];k=(math.sin(t+i*1.4)+1)/2;d.rounded_rectangle((x,y,x+288,y+147),radius=10,fill=BG)
  if i==0:
   d.rounded_rectangle((x+22,y+18,x+266,y+122),radius=7,outline=c,width=2);d.line((x+22,y+38,x+266,y+38),fill=c)
   for a in range(3):ring(d,x+32+a*8,y+29,2,c)
   d.rectangle((x+35,y+52,x+110,y+109),fill='#35364e');d.rectangle((x+125,y+52,x+250,y+64),fill=c)
   for a in range(3):d.line((x+125,y+76+a*13,x+155+int(90*(.45+.5*k)),y+76+a*13),fill='#75758e',width=3)
  elif i==1:
   for a in range(5):
    for b in range(3):
     xx=x+37+a*48;yy=y+20+b*38;d.rounded_rectangle((xx,yy,xx+33,yy+26),radius=3,outline=c if (a+b)%3==0 else '#53576c')
   d.line((x+24,y+110,x+85,y+110,x+85,y+49,x+200,y+49,x+200,y+88,x+263,y+88),fill=c,width=2);d.ellipse((x+85+110*k-4,y+45,x+85+110*k+4,y+53),fill=c)
  else:
   xx=x+99;yy=y+13;d.rounded_rectangle((xx,yy,xx+90,yy+120),radius=14,outline=c,width=2);d.rounded_rectangle((xx+12,yy+20,xx+78,yy+56),radius=6,fill='#363849');d.rounded_rectangle((xx+12,yy+65,xx+78,yy+82),radius=6,fill=c);d.line((xx+22,yy+98,xx+22+45*k,yy+98),fill=c,width=3)
  txt(d,(x,224),name,31,INK,'Bold');txt(d,(x,263),sub,18,'#656579')
 return im
def git(t):
 im,d=base(255);label(d,'04','VERSION CONTROL');txt(d,(36,55),'From branch to delivery.',35,PAPER,'Bold');p=[(70,157),(225,157),(360,112),(525,112),(660,157),(807,157),(930,157)]
 d.line((70,157,930,157),fill='#46506e',width=3);d.line(p,fill=LAV,width=4,joint='curve');lengths=[math.dist(a,b) for a,b in zip(p,p[1:])];step=t/T*sum(lengths);point=p[-1]
 for a,b,l in zip(p,p[1:],lengths):
  if step<=l:point=(a[0]+(b[0]-a[0])*step/l,a[1]+(b[1]-a[1])*step/l);break
  step-=l
 for (x,y),s in zip(p,['Branch','Commit','Feature','Review','Merge','Push','Deliver']):
  ring(d,x,y,6,LAV,2);txt(d,(x,y+21),s,15,PAPER,'Medium','ma')
 x,y=point;ring(d,x,y,15,'#6467bb',2);d.ellipse((x-6,y-6,x+6,y+6),fill=ACC);txt(d,(36,220),'GIT   /   GITHUB   /   COLLABORATIVE ENGINEERING',14,MUT,'Medium');return im
def closing(t):
 im,d=base(160,PAPER);label(d,'05','THE NEXT STEP','#66677b');txt(d,(36,56),'Build something meaningful.',44,INK,'Bold');d.line((36,130,964,130),fill='#cbc8ff',width=3);d.line((36,130,36+int(928*(1+math.sin(t))/2),130),fill='#7467ea',width=4);return im
if __name__=='__main__':
 for name,func in [('hero',hero),('focus',focus),('stack',stack),('work',work),('git',git),('closing',closing)]:
  frames=[func(T*i/N) for i in range(N)];frames[0].save(P/(name+'.gif'),save_all=True,append_images=frames[1:],duration=80,loop=0,optimize=True,disposal=2);frames[9].save(P/(name+'-still.png'));print(name,flush=True)
