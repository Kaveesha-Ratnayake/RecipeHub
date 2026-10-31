from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from html import escape

out=Path(__file__).resolve().parent
W,H=1800,1530
im=Image.new('RGB',(W,H),'white'); dr=ImageDraw.Draw(im)
font_path='C:/Windows/Fonts/times.ttf'
bold_path='C:/Windows/Fonts/timesbd.ttf'
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">','<rect width="100%" height="100%" fill="white"/>']
def text(x,y,t,size=27,bold=False,anchor='start'):
 f=ImageFont.truetype(bold_path if bold else font_path,size)
 dr.text((x,y),t,font=f,fill='#17232c',anchor='mt' if anchor=='middle' else 'lt')
 svg.append(f'<text x="{x}" y="{y+size*.83}" font-family="Times New Roman" font-size="{size}" font-weight="{"bold" if bold else "normal"}" text-anchor="{anchor}" fill="#17232c">{escape(t)}</text>')
def line(points):
 dr.line(points,fill='#485864',width=3)
 svg.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in points)+'" fill="none" stroke="#485864" stroke-width="3"/>')
def box(x,y,w,title,fields):
 height=65+len(fields)*36+20
 dr.rectangle((x,y,x+w,y+height),fill='white',outline='#485864',width=3)
 dr.rectangle((x+2,y+2,x+w-2,y+60),fill='#e5ebf0')
 svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{height}" fill="white" stroke="#485864" stroke-width="3"/><rect x="{x+2}" y="{y+2}" width="{w-4}" height="58" fill="#e5ebf0"/>')
 text(x+w/2,y+15,title,31,True,'middle')
 line([(x,y+61),(x+w,y+61)])
 for i,t in enumerate(fields):text(x+20,y+76+i*36,t,26)

text(W/2,25,'RecipeHub Database ER Diagram',39,True,'middle')
text(W/2,78,'MongoDB collections and logical relationships',27,False,'middle')
# Draw connectors first so entity boxes remain clean.
line([(680,230),(1080,230)]);text(705,190,'1');text(1005,190,'0..*');text(875,247,'owns',25,False,'middle')
line([(375,395),(375,600)]);text(393,451,'1');text(393,555,'0..*');text(420,495,'has sessions',25,False,'end' if False else 'start')
line([(680,375),(850,375),(850,965),(1080,965)]);text(700,337,'1');text(1002,923,'0..*');text(875,922,'saves',25)
line([(1400,611),(1400,870)]);text(1418,706,'1');text(1418,823,'0..*');text(1438,765,'is saved in',25)
line([(80,285),(30,285),(30,1320),(650,1320)]);text(42,300,'1');text(565,1277,'0..*');text(290,1277,'submits',25)
line([(1720,400),(1770,400),(1770,1320),(1250,1320)]);text(1735,420,'1');text(1270,1277,'0..*');text(1470,1277,'receives',25)
box(80,130,600,'User  |  users',[
 '_id : ObjectId  [PK]','name : String','email : String  [unique]','passwordHash : String','salt : String'])
box(1080,130,640,'Recipe  |  recipes',[
 '_id : ObjectId  [PK]','owner : ObjectId  [reference → User]', 'title : String','category : String  [enum]','time : Number  [1–1440]', 'servings : Number  [1–100]','description : String','image : String  [URL]','ingredients : String[]','instructions : String[]','createdAt, updatedAt : Date'])
box(80,600,600,'Session  |  sessions',[
 '_id : ObjectId  [PK]','digest : String  [unique]','user : ObjectId  [reference → User]','expires : Date  [TTL index]'])
box(1080,870,640,'Favourite  |  favourites',[
 '_id : ObjectId  [PK]','user : ObjectId  [reference → User]','recipe : ObjectId  [reference → Recipe]','createdAt, updatedAt : Date'])
box(650,1220,600,'Rating  |  ratings',[
 '_id : ObjectId  [PK]','user : ObjectId  [reference → User]','recipe : ObjectId  [reference → Recipe]','value : Number  [integer 1–5]'])
text(80,1110,'Favourite and Rating each have a unique compound index on (user, recipe).',25)
text(80,1150,'1 = one    0..* = zero or many    PK = document identifier',25)
text(80,1460,'References are logical links; MongoDB does not enforce foreign keys. Legacy recipes may have no owner.',24)
svg.append('</svg>')
im.save(out/'RecipeHub_ER_Diagram.png',dpi=(300,300))
(out/'RecipeHub_ER_Diagram.svg').write_text('\n'.join(svg),encoding='utf-8')
print('PNG and editable SVG created')

