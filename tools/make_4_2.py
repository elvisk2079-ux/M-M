"""Build lesson 4.2 Winter Fun (lesson + homework) in the same format as lesson 4.1 First Snow.
Reuses 4.1 CSS and helper JS; only the sections and data change."""
import json, os, re
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_l = open(f'{R}/lessons/4.1/index.html').read()
src_h = open(f'{R}/lessons/4.1/homework.html').read()

W = [
 dict(en='make a snowman', ru='слепить снеговика', pic='⛄', verb='make', key='snowman'),
 dict(en='make snowballs', ru='лепить снежки', pic='🤲⚪', verb='make', key='snowballs'),
 dict(en='have a snowball fight', ru='играть в снежки', pic='⚪💥😄', verb='have', key='snowball fight'),
 dict(en='go sledding', ru='кататься на санках', pic='🛷', verb='go', key='sledding'),
 dict(en='go skiing', ru='кататься на лыжах', pic='⛷️', verb='go', key='skiing'),
 dict(en='go ice skating', ru='кататься на коньках', pic='⛸️', verb='go', key='ice skating'),
 dict(en='build a snow fort', ru='строить снежную крепость', pic='🏰❄️', verb='build', key='snow fort'),
 dict(en='make snow angels', ru='делать снежных ангелов', pic='👼❄️', verb='make', key='snow angels'),
 dict(en='catch snowflakes', ru='ловить снежинки', pic='🙌❄️', verb='catch', key='snowflakes'),
 dict(en='go for a winter walk', ru='пойти на зимнюю прогулку', pic='🚶🌲', verb='go', key='winter walk'),
 dict(en='wear warm clothes', ru='носить тёплую одежду', pic='🧥🧤', verb='wear', key='warm clothes'),
 dict(en='drink hot chocolate', ru='пить горячий шоколад', pic='☕🍫', verb='drink', key='hot chocolate'),
]
N = len(W)
js = lambda o: json.dumps(o, ensure_ascii=False)

def sec(id_, title, help_, extra='', check='checkChoice'):
    return (f'<section class="task" data-id="{id_}"><h2>{title}</h2><p class="help">{help_}</p>{extra}<div id="{id_}"></div>'
            f'<div class="controls"><button class="btn primary" onclick="{check}(\'{id_}\')" type="button">✓ Check answers</button></div>'
            f'<div class="controls"><span class="feedback"></span></div></section>')

STORY = ("<p>It is Saturday morning. Matvey and Makar look out of the window. The sky is blue and the snow is white. ‘Let’s go outside!’ says Matvey. "
         "The boys put on <b>warm</b> coats, hats and gloves. Their dog Spot is very excited.</p>"
         "<p>First, the boys <b>make a big snowman</b> in the garden. Makar finds a carrot for its nose. Then they <b>make snowballs</b> and "
         "<b>have a friendly snowball fight</b>. Spot runs after the snowballs, but he cannot catch them all!</p>"
         "<p>After lunch, the boys <b>go sledding</b> in the park. Matvey loves going fast, but Makar likes going slowly. They see some children "
         "<b>skiing</b> and <b>ice skating</b>. ‘I want to try skiing one day,’ says Makar.</p>"
         "<p>In the afternoon, the wind gets stronger. It is <b>cold</b> and <b>snowy</b>. The boys go home and <b>drink hot chocolate</b>. "
         "‘I love winter <b>because</b> we can do so many fun things!’ says Matvey. ‘Me too!’ says Makar.</p>")

HWSTORY = ("<p>It is Sunday. It is <b>sunny</b> but <b>cold</b>. Matvey and Makar <b>wear warm clothes</b>. They <b>go for a winter walk</b> in the park.</p>"
           "<p>Matvey <b>catches snowflakes</b>. Makar <b>makes snow angels</b> in the snow. Then they <b>build a snow fort</b> with Dad. "
           "They do not go skiing because they have no skis.</p>"
           "<p>At home Mum makes <b>hot chocolate</b>. The boys are happy and <b>warm</b>.</p>")

WEATHER = ('<div class="sequence"><div class="seqitem">☀️ sunny</div><div class="seqitem">🌬️ windy</div>'
           '<div class="seqitem">❄️ snowy</div><div class="seqitem">🥶 cold</div><div class="seqitem">☕ warm</div></div>')

lesson_secs = [
 '<section class="task" data-id="vocab"><h2>1. Flip the cards — 12 winter activities</h2><p class="help">Front: picture, English and 🔊. Back: Russian translation only. Tap to flip.</p>'
 f'<p id="lesson-flash-stat" class="flash-stat">Запомнил: 0 / {N}</p><div id="vocab"></div><div class="flash-actions"><button type="button" class="flash-no" id="lesson-again">← Не запомнил</button>'
 '<button type="button" class="flash-yes" id="lesson-know">Запомнил →</button></div><div class="controls" style="justify-content:center"><button type="button" class="btn blue" id="lesson-restart">↻ Повторить карточки</button></div>'
 '<div class="controls"><span class="feedback"></span></div></section>',
 sec('russian', '2. English → Russian', 'Choose the Russian meaning. These are the SAME phrases as on the cards.'),
 sec('listen', '3. Look and choose', 'Look at the picture and choose the correct English phrase.'),
 sec('verbs', '4. Which word goes first?', 'make, go, have, build, catch, wear or drink? Choose the first word of the phrase.'),
 sec('picture', '5. Choose the picture', 'Read the phrase and choose a picture.'),
 sec('weather', '6. Winter weather', 'Choose one weather word. Look at the pictures for help.', WEATHER),
 sec('reading', '7. Read: A Snowy Saturday', 'Read the story and choose the answer. No audio in the story.', f'<div class="story" id="story">{STORY}</div>'),
 sec('final', '8. I can · I like · because', 'Choose the correct sentence part. I can go… · I like going… · because…'),
]
hw_secs = [
 sec('hwlisten', '1. Look and choose', 'Look at the picture and Russian meaning. Choose the English phrase.'),
 sec('hwtranslate', '2. Russian → English', 'Choose the English phrase.'),
 sec('letters', '3. Choose the missing letter', 'The word is almost complete. Pick its missing letter.'),
 sec('write', '4. Look and write the missing word', 'Look at the picture and Russian translation. Write the missing word(s).', check='checkInput'),
 sec('verbwrite', '5. Write the first word', 'make, go, have, build, catch, wear or drink? Write it.', check='checkInput'),
 sec('hwweather', '6. What is the weather like?', 'Choose the weather word.', WEATHER),
 sec('hwreading', '7. Mini story: Sunday in the park', 'Read a NEW little story with the same phrases. Then choose the answer.', f'<div class="story" id="hwstory">{HWSTORY}</div>'),
 sec('hwfinal', '8. Last round — I can, I like', 'Choose the correct form. Try to get your final star.'),
]

def opts3(i, f, a, b):
    return [f(W[i]), f(W[(i + a) % N]), f(W[(i + b) % N])]

def rot(lst, i):
    k = i % len(lst); return lst[k:] + lst[:k]

VERBS = ['make', 'go', 'have', 'build', 'catch', 'drink', 'wear']
VERB_Q = []
for i, w in enumerate(W):
    others = [v for v in VERBS if v != w['verb']]
    o = [w['verb'], others[i % len(others)], others[(i + 3) % len(others)]]
    VERB_Q.append(dict(prompt=f'<span class="iconchoices">{w["pic"]}</span> ___ {" ".join(w["en"].split()[1:])}', answer=w['verb'], options=rot(o, i)))

L_DATA = f"""
window.addEventListener('DOMContentLoaded',()=>{{
qChoice('russian', W.map((w,i)=>({{prompt:w.en,answer:w.ru,options:[w.ru,W[(i+3)%{N}].ru,W[(i+7)%{N}].ru].sort((a,b)=>((a.length+i)%5)-((b.length+i)%5))}})));
qChoice('listen', W.map((w,i)=>({{prompt:`<span class="iconchoices">${{w.pic}}</span> ${{w.ru}}`,answer:w.en,options:[[w.en,W[(i+4)%{N}].en,W[(i+8)%{N}].en],[W[(i+5)%{N}].en,w.en,W[(i+9)%{N}].en],[W[(i+2)%{N}].en,W[(i+6)%{N}].en,w.en]][i%3]}})));
qChoice('verbs', {js(VERB_Q)});
qChoice('picture',W.map((w,i)=>({{prompt:w.en,answer:w.en,options:[[w,W[(i+3)%{N}],W[(i+7)%{N}]],[W[(i+5)%{N}],w,W[(i+9)%{N}]],[W[(i+2)%{N}],W[(i+6)%{N}],w]][i%3].map(v=>({{value:v.en,label:`<span class="iconchoices">${{v.pic}}</span>`}}))}})));
qChoice('weather', [
{{prompt:'🥶 It is ___ in winter. We wear hats and gloves.',answer:'cold',options:['cold','warm']}},
{{prompt:'❄️ Today it is ___. Snow is everywhere!',answer:'snowy',options:['sunny','snowy']}},
{{prompt:'🌬️ It is ___. The trees move.',answer:'windy',options:['windy','warm']}},
{{prompt:'☀️ Sometimes it is ___ and the snow shines.',answer:'sunny',options:['snowy','sunny']}},
{{prompt:'☕ After playing outside I feel ___ at home.',answer:'warm',options:['cold','warm']}},
{{prompt:'🌨️ In the afternoon it is cold and ___.',answer:'snowy',options:['snowy','sunny']}}]);
qChoice('reading',[
{{prompt:'What do the boys wear outside? (Что надевают мальчики?)',answer:'coats, hats and gloves',options:['T-shirts and shorts','coats, hats and gloves']}},
{{prompt:'What do they make in the garden?',answer:'a snowman',options:['a snowman','a sandcastle']}},
{{prompt:'What does Makar find for the nose? (Что нашёл Макар для носа?)',answer:'a carrot',options:['a banana','a carrot']}},
{{prompt:'Where do they go sledding?',answer:'in the park',options:['in the park','in the garden']}},
{{prompt:'Who loves going fast? (Кто любит быстро?)',answer:'Matvey',options:['Matvey','Makar']}},
{{prompt:'What does Makar want to try?',answer:'skiing',options:['swimming','skiing']}},
{{prompt:'What do they drink at home?',answer:'hot chocolate',options:['hot chocolate','cold juice']}},
{{prompt:'Why does Matvey love winter?',answer:'because we can do many fun things',options:['because it is hot','because we can do many fun things']}}]);
qChoice('final',[
{{prompt:'⛷️ I can ___.',answer:'go skiing',options:['go skiing','going skiing']}},
{{prompt:'🛷 I like ___.',answer:'going sledding',options:['go sledding','going sledding']}},
{{prompt:'⛸️ He ___ ice skating on Saturday.',answer:'goes',options:['go','goes']}},
{{prompt:'⛄ We can ___ a snowman.',answer:'make',options:['make','drink']}},
{{prompt:'⚪ I like ___ snowballs.',answer:'making',options:['make','making']}},
{{prompt:'❄️ I like winter ___ I can play in the snow.',answer:'because',options:['because','but']}},
{{prompt:'☕ After the walk we ___ hot chocolate.',answer:'drink',options:['wear','drink']}},
{{prompt:'🧥 In winter we ___ warm clothes.',answer:'wear',options:['wear','catch']}}]);
}});"""

letters = [('make a snow _ an', 'm', ['m', 'n', 'w'], 'слепить снеговика'), ('make snowb _ lls', 'a', ['a', 'o', 'e'], 'лепить снежки'),
           ('have a snowball f _ ght', 'i', ['e', 'i', 'a'], 'играть в снежки'), ('go sle _ ding', 'd', ['t', 'd', 'b'], 'кататься на санках'),
           ('go sk _ ing', 'i', ['e', 'y', 'i'], 'кататься на лыжах'), ('go ice ska _ ing', 't', ['d', 't', 'p'], 'кататься на коньках'),
           ('build a snow f _ rt', 'o', ['o', 'a', 'u'], 'строить снежную крепость'), ('make snow an _ els', 'g', ['j', 'g', 'k'], 'делать снежных ангелов'),
           ('c _ tch snowflakes', 'a', ['e', 'u', 'a'], 'ловить снежинки'), ('go for a winter w _ lk', 'a', ['a', 'o', 'e'], 'пойти на зимнюю прогулку'),
           ('wear warm cl _ thes', 'o', ['a', 'o', 'u'], 'носить тёплую одежду'), ('drink hot ch _ colate', 'o', ['a', 'o', 'e'], 'пить горячий шоколад')]
LETTERS = ',\n'.join(js(dict(prompt=f'{p} · {ru}', answer=a, options=o)) for p, a, o, ru in letters)

write_items = []
for w in W:
    blank = w['en'].replace(w['key'], '_____')
    ans = w['key'] + ('|ice-skating|iceskating' if w['key'] == 'ice skating' else '')
    write_items.append(dict(prompt=f'<span class="iconchoices">{w["pic"]}</span> {blank} · {w["ru"]}', answer=ans,
                            hint=w['key'][0] + '… (' + ' + '.join(str(len(x)) for x in w['key'].split()) + ' letters)'))
order = [3, 0, 6, 8, 11, 1, 4, 9, 2, 10, 5, 7]
verb_items = [dict(prompt=f'<span class="iconchoices">{W[i]["pic"]}</span> ___ {" ".join(W[i]["en"].split()[1:])} · {W[i]["ru"]}',
                   answer=W[i]['verb'], hint=W[i]['verb'][0] + '…') for i in order]

H_DATA = f"""
window.addEventListener('DOMContentLoaded',()=>{{
qChoice('hwlisten', W.map((w,i)=>({{prompt:`<span class="iconchoices">${{w.pic}}</span> ${{w.ru}}`,answer:w.en,options:[[W[(i+2)%{N}].en,w.en,W[(i+5)%{N}].en],[w.en,W[(i+7)%{N}].en,W[(i+3)%{N}].en],[W[(i+9)%{N}].en,W[(i+4)%{N}].en,w.en]][i%3]}})));
qChoice('hwtranslate',W.map((w,i)=>({{prompt:`${{w.ru}}`,answer:w.en,options:[[W[(i+4)%{N}].en,W[(i+7)%{N}].en,w.en],[w.en,W[(i+6)%{N}].en,W[(i+1)%{N}].en],[W[(i+8)%{N}].en,w.en,W[(i+5)%{N}].en]][i%3]}})));
qChoice('letters',[
{LETTERS}]);
qInput('write',{js(write_items)});
qInput('verbwrite',{js(verb_items)});
qChoice('hwweather',[
{{prompt:'🌬️ The wind is strong. It is ___.',answer:'windy',options:['windy','sunny']}},
{{prompt:'☀️ The sun shines. It is ___.',answer:'sunny',options:['snowy','sunny']}},
{{prompt:'❄️ It snows all day. It is ___.',answer:'snowy',options:['snowy','warm']}},
{{prompt:'🧣 Put on your hat! It is ___.',answer:'cold',options:['warm','cold']}},
{{prompt:'☕ Hot chocolate makes me ___.',answer:'warm',options:['warm','windy']}},
{{prompt:'⛄ It is ___ in winter.',answer:'cold',options:['cold','hot']}}]);
qChoice('hwreading',[
{{prompt:'What day is it? (Какой день?)',answer:'Sunday',options:['Saturday','Sunday']}},
{{prompt:'What is the weather like?',answer:'sunny but cold',options:['sunny but cold','windy and warm']}},
{{prompt:'Who catches snowflakes?',answer:'Matvey',options:['Matvey','Makar']}},
{{prompt:'What does Makar make? (Что делает Макар?)',answer:'snow angels',options:['a snowman','snow angels']}},
{{prompt:'Who builds a snow fort with the boys?',answer:'Dad',options:['Dad','Mum']}},
{{prompt:'Why don’t they go skiing?',answer:'they have no skis',options:['it is too hot','they have no skis']}},
{{prompt:'What does Mum make?',answer:'hot chocolate',options:['a cake','hot chocolate']}}]);
qChoice('hwfinal',[
{{prompt:'🛷 I can ___.',answer:'go sledding',options:['going sledding','go sledding']}},
{{prompt:'⛸️ I like ___.',answer:'going ice skating',options:['going ice skating','go ice skating']}},
{{prompt:'❄️ She ___ snowflakes.',answer:'catches',options:['catch','catches']}},
{{prompt:'🏰 Can you ___ a snow fort?',answer:'build',options:['build','building']}},
{{prompt:'👼 I like ___ snow angels.',answer:'making',options:['making','make']}},
{{prompt:'☀️ I like winter ___ it is beautiful.',answer:'because',options:['and','because']}},
{{prompt:'🚶 We ___ for a winter walk.',answer:'go',options:['go','make']}},
{{prompt:'⚪💥 We ___ a snowball fight.',answer:'have',options:['have','go']}},
{{prompt:'⛷️ My favourite winter activity is ___.',answer:'skiing',options:['ski','skiing']}},
{{prompt:'🧤 Do you like winter? — Yes, I ___.',answer:'do',options:['do','am']}}]);
}});"""

def build(src, title, sub, badges, secs, data, keyname, link, out):
    head = src[:src.index('<body>')]
    head = re.sub(r'<title>.*?</title>', f'<title>{title} · M&amp;M English</title>', head)
    common = re.search(r'<script>\n(const W=.*?)</script>', src, re.S).group(1)
    common = re.sub(r'const W=\[.*?\];', 'const W=' + js(W) + ';', common, count=1, flags=re.S)
    common = common.replace("'mm_first_snow_easy_'", "'mm_winter_fun_'").replace("_v2'", "_v1'")
    common = common.replace('Все 10 слов запомнены', f'Все {N} фраз запомнены')
    if 'function wordsGrid' not in common:
        common = common.replace('{wordsGrid();refresh()}', '{refresh()}')
    body = (f'<body><main class="wrap"><a class="back" href="../../">← M&amp;M English</a><header class="hero"><h1>⛄ {title}</h1><p>{sub}</p>'
            + ''.join(f'<span class="badge">{b}</span>' for b in badges)
            + f'<div class="track"><div id="fill"></div></div></header><div class="toolbar"><span id="count">⭐ 0 / 0</span>{link}</div>'
            + ''.join(secs) + '<div class="finish" id="end"></div></main><script>\n' + common + '</script><script>' + data + '</script></body></html>')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w').write(head + body)

build(src_l, 'Winter Fun — Lesson', 'Winter activities · Matvey &amp; Makar', ['🔊 British English audio on cards', '📱 All activities one after another', '⭐ Stars for correct work'],
      lesson_secs, L_DATA, 'lesson', '<a href="homework.html">↗ Homework</a>', f'{R}/lessons/4.2/index.html')
build(src_h, 'Winter Fun — Homework', 'Lots of short, simple games with the same 12 phrases', ['✏️ Practice without audio', '📱 All activities one after another', '⭐ Stars for correct work'],
      hw_secs, H_DATA, 'hw', '<a href="./">↗ Lesson</a>', f'{R}/lessons/4.2/homework.html')
print('ok')
