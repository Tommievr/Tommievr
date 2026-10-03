from PIL import Image
import statistics as st
def f(img,name,box,pred,stat='median'):
    im=Image.open(img).convert('RGBA'); x0,y0,x1,y1=box
    px=[im.getpixel((x,y)) for x in range(x0,x1) for y in range(y0,y1)]
    px=[p for p in px if p[3]>200 and pred(*p[:3])]
    if len(px)<5: print(name,'none');return
    m=[int(st.median(p[i] for p in px)) for i in range(3)]
    # also brighter (75th pct by luminance)
    px.sort(key=lambda p:sum(p[:3])); q=px[int(len(px)*.8)]
    print(f"{name:22s} med #{m[0]:02X}{m[1]:02X}{m[2]:02X}  lit #{q[0]:02X}{q[1]:02X}{q[2]:02X} n={len(px)}")
C='assets/characters/evie-and-justin-reference.png'; L='assets/characters/lambs-reference.png'
blue=lambda r,g,b:b>r+50 and b>90
green=lambda r,g,b:g>r+35 and g>b+20 and g>70
f(C,'evie iris',(540,330,790,420),blue)
f(C,'justin iris',(1000,290,1280,460),green)
f(L,'cotton iris',(500,230,780,350),blue)
f(L,'toffee iris',(1030,220,1330,370),green)
f(C,'evie collar',(480,510,700,570),lambda r,g,b:r>120 and g<80)
f(C,'evie tag',(590,570,670,650),lambda r,g,b:r>150 and g>90 and b<80)
f(C,'justin tag',(1110,590,1200,660),lambda r,g,b:r>150 and g>90 and b<80)
f(C,'justin collar',(1050,545,1260,590),lambda r,g,b:r<70 and abs(r-b)<40)
f(C,'evie fur white',(300,200,560,330),lambda r,g,b:r>200)
f(C,'evie fur shade',(150,560,330,700),lambda r,g,b:r>170)
f(C,'evie ear pink',(700,50,760,120),lambda r,g,b:r>200 and g<190)
f(C,'evie nose',(670,380,720,415),lambda r,g,b:r>200 and g<170)
f(C,'justin fur',(1100,200,1400,300),lambda r,g,b:r<90 and r>25)
f(C,'justin ear back',(1420,190,1520,270),lambda r,g,b:r>190)
f(C,'justin nose',(1100,405,1160,440),lambda r,g,b:r>130)
f(C,'justin inner ear',(1020,70,1090,160),lambda r,g,b:r>90)
f(L,'cotton wool',(380,480,640,620),lambda r,g,b:r>220)
f(L,'cotton ear',(240,310,350,400),lambda r,g,b:r>220 and g<170)
f(L,'cotton collar',(530,455,690,490),lambda r,g,b:b>r+8)
f(L,'cotton bell',(620,500,690,570),lambda r,g,b:r>190 and g>110 and b<90)
f(L,'cotton hoof',(730,680,830,740),lambda r,g,b:r<120)
f(L,'toffee wool',(1150,520,1320,640),lambda r,g,b:r>80 and g<90 and r>g+30)
f(L,'toffee chest',(1100,560,1170,650),lambda r,g,b:r>200)
f(L,'toffee collar',(1100,455,1260,490),lambda r,g,b:g>r and g>b+10)
f(L,'toffee bell',(1070,500,1140,570),lambda r,g,b:r>190 and g>110 and b<90)
f(L,'toffee ear',(1440,310,1560,380),lambda r,g,b:r>110 and g<100 and abs(r-g)>40)
f(L,'toffee leg cream',(940,720,1080,790),lambda r,g,b:r>220)
f(L,'toffee hoof',(910,780,1010,830),lambda r,g,b:r<110)
f(L,'toffee face',(1100,250,1240,300),lambda r,g,b:r>220)
