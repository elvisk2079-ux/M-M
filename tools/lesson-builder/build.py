"""Build lesson index.html + homework.html for each lesson in data.LESSONS into the M&M repo."""
import base64, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import LESSONS

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))

t13 = open(f'{REPO}/lessons/1.3/index.html').read()
CSS = re.search(r'<style>\n(.*?)</style>', t13, re.S).group(1)
hw13 = open(f'{REPO}/lessons/1.3/homework.html').read()
HWCSS = re.search(r'<style>\n(.*?)</style>', hw13, re.S).group(1)
TTS = re.search(r'(const TTS=.*?else start\(\)\})', hw13, re.S).group(1)

def b64(path):
    return 'data:image/jpeg;base64,' + base64.b64encode(open(path, 'rb').read()).decode()

def js(o):
    return json.dumps(o, ensure_ascii=False)

def build(lid, L):
    d = os.path.join(HERE, 'img', L['dir'])
    imgs = {w['en'].replace(' ', '_'): b64(f"{d}/{w['en'].replace(' ', '_')}.jpg") for w in L['words']}
    panels = [b64(f'{d}/{f}') for f in sorted(os.listdir(d)) if re.fullmatch(r's\d+\.jpg', f)]
    for w in L['spell']:
        assert w.replace(' ', '_') in imgs, w
    for it in L['hw']['gap']['items']:
        if it[1]: assert it[1] in imgs, it[1]
    lesson_data = {k: L[k] for k in ['intro', 'words', 'storyTitle', 'story', 'spell', 'choose', 'tf', 'odd', 'oddGroup', 'order', 'frames', 'game', 'talk', 'paper', 'teacher']}
    rep = {'{{CSS}}': CSS, '{{TITLE}}': L['title'], '{{ID}}': lid, '{{HERO}}': b64(f'{d}/hero.jpg'),
           '{{IMGS}}': js(imgs), '{{PANELS}}': js(panels), '{{DATA}}': js(lesson_data), '{{TTS}}': TTS}
    t = open(os.path.join(HERE, 'tpl_lesson.html')).read()
    for k, v in rep.items():
        t = t.replace(k, v)
    assert '{{' not in t
    out = f'{REPO}/lessons/{lid}'
    os.makedirs(out, exist_ok=True)
    open(f'{out}/index.html', 'w').write(t)

    hw_data = dict(words=L['words'], **L['hw'])
    rep = {'{{HWCSS}}': HWCSS, '{{TITLE}}': L['title'], '{{ID}}': lid, '{{IMGS}}': js(imgs), '{{DATA}}': js(hw_data), '{{TTS}}': TTS}
    t = open(os.path.join(HERE, 'tpl_homework.html')).read()
    for k, v in rep.items():
        t = t.replace(k, v)
    assert '{{' not in t
    open(f'{out}/homework.html', 'w').write(t)
    print(lid, os.path.getsize(f'{out}/index.html')//1024, 'KB +', os.path.getsize(f'{out}/homework.html')//1024, 'KB')

for lid in (sys.argv[1:] or LESSONS):
    build(lid, LESSONS[lid])
