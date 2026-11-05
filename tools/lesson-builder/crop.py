"""Run from a work folder holding <dir>/hi-1.png and <dir>/hi-3.png (pages rendered at 165 dpi; 2.1 = original PNGs).
Crop word cards, hero and story panels from lesson pages.
Coordinates are given in preview space (1287 wide for PDFs, 1491 for 2.1 PNGs)."""
import os, json
from PIL import Image

R = lambda xs, y0, y1: [(a, y0, b, y1) for a, b in xs]
X5a = [(30, 272), (284, 522), (532, 765), (776, 1010), (1022, 1262)]
XB = [(275, 465), (473, 660), (668, 855), (862, 1050), (1058, 1260)]

L = {
 'h14': dict(base=1287, words=['house','home','room','kitchen','bedroom','bathroom','living room','garden','door','window'],
   boxes=R([(608,808),(834,1030),(1056,1252)],125,298)+R([(608,808),(834,1030),(1056,1252)],377,545)+R([(553,728),(750,915),(938,1095),(1115,1260)],625,795),
   hero=(10,185,532,860),
   panels=[(512,105,887,365),(905,105,1278,365),(512,378,887,622),(905,378,1278,622),(512,636,887,870),(905,636,1278,870)]),
 'r15': dict(base=1287, words=['bed','desk','chair','wardrobe','shelf','lamp','carpet','cupboard','curtains','toy box','bunk bed','mirror','poster','pillow','messy'],
   boxes=R(X5a,272,420)+R(X5a,492,640)+R(XB,727,850),
   hero=(690,5,1278,250),
   panels=[(435,245,860,540),(870,245,1278,540),(435,555,860,885),(870,555,1278,885)]),
 'c16': dict(base=1287, words=['T-shirt','jumper','trousers','shorts','skirt','dress','shoes','socks','jacket','hat','school uniform','tie','trainers','cap','sunglasses'],
   boxes=R(X5a,240,405)+R(X5a,470,635)+R(XB,712,840),
   hero=(655,5,1278,225),
   panels=[(515,230,878,515),(890,230,1278,515),(515,527,878,885),(890,527,1278,885)]),
 'k21': dict(base=1491, words=['board','pen','pencil','ruler','rubber','scissors','glue','notebook','pencil case','crayons','teacher','pupil','classroom','table','window'],
   boxes=R([(318,530),(550,762),(780,993),(1012,1226),(1245,1462)],278,440)+R([(338,545),(563,768),(785,997),(1015,1228),(1246,1462)],518,680)+R([(272,500),(520,735),(755,985),(1005,1228),(1246,1468)],832,985),
   hero=(0,280,312,1000),
   panels=[(583,190,1000,545),(1018,190,1478,545),(583,565,955,1035),(975,565,1478,1035)]),
}

def cut(im, box, s, out, w):
    x0, y0, x1, y1 = box
    c = im.crop((int(x0*s), int(y0*s), int(x1*s), int(y1*s)))
    c.thumbnail((w, w*3))
    c.save(out, quality=80)

for k, d in L.items():
    os.makedirs(f'{k}/img', exist_ok=True)
    p1 = Image.open(f'{k}/hi-1.png').convert('RGB'); p3 = Image.open(f'{k}/hi-3.png').convert('RGB')
    s = p1.width / d['base']
    for w, b in zip(d['words'], d['boxes']):
        x0, y0, x1, y1 = b
        cut(p1, (x0+4, y0+4, x1-4, y1-2), s, f"{k}/img/{w.replace(' ','_')}.jpg", 260)
    cut(p1, d['hero'], s, f'{k}/img/hero.jpg', 460)
    for i, b in enumerate(d['panels'], 1):
        cut(p3, b, s, f'{k}/img/s{i}.jpg', 420)
    # contact sheet
    ims = [Image.open(f"{k}/img/{w.replace(' ','_')}.jpg") for w in d['words']]
    sh = Image.new('RGB', (5*270, ((len(ims)+4)//5)*230), 'white')
    for i, im in enumerate(ims):
        im2 = im.copy(); im2.thumbnail((260, 220)); sh.paste(im2, ((i % 5)*270, (i//5)*230))
    sh.save(f'{k}/sheet.jpg')
    ps = [Image.open(f'{k}/img/hero.jpg')] + [Image.open(f'{k}/img/s{i}.jpg') for i in range(1, len(d['panels'])+1)]
    sh2 = Image.new('RGB', (1400, 900), 'white'); x = y = h = 0
    for im in ps:
        im2 = im.copy(); im2.thumbnail((330, 300))
        if x + im2.width > 1400: x = 0; y += h + 8; h = 0
        sh2.paste(im2, (x, y)); x += im2.width + 8; h = max(h, im2.height)
    sh2.save(f'{k}/sheet2.jpg')
json.dump({k: d['words'] for k, d in L.items()}, open('words.json', 'w'))
print('ok')
