#!/usr/bin/env python3
"""Build GitHub organization overviews from localized source copy."""
import argparse
import hashlib
import unicodedata
import html
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
ORG = 'https://github.com/seaimagineai'
RAW = 'https://raw.githubusercontent.com/seaimagineai/.github/main/assets/'
LOCALES = [x['locale'] for x in json.loads((ROOT/'data/website-locales.json').read_text())['locales']]
COPY = {code: json.loads((ROOT/'i18n'/f'{code}.json').read_text()) for code in LOCALES}
MODEL_ROUTES = ['model/gemini-omni-1-1-flash/', 'model/grok-imagine-1-5/', 'model/seedance-2-5/']
PROJECTS = [('Gemini Omni', 'awesome-gemini-omni-prompts', 'gemini-omni.png'), ('Grok Imagine 1.5', 'awesome-grok-imagine-prompts', 'grok-imagine.webp'), ('Seedance 2.5', 'awesome-seedance-2-5-prompts', 'seedance.jpg')]
SUFFIX = {'cn':'ZH','tw':'ZH-TW','en':'EN', **{c:c.upper() for c in LOCALES if c not in ('cn','tw','en')}}
GROK = {'en':'','cn':'.zh-CN','tw':'.zh-TW','ja':'.ja-JP','ko':'.ko-KR','th':'.th-TH','vi':'.vi-VN','id':'.id-ID','es':'.es-ES','fr':'.fr-FR','de':'.de-DE','it':'.it-IT','pt':'.pt-BR','ru':'.ru-RU','ar':'.ar'}

def filename(code):
    return 'README.md' if code == 'en' else f'README_{code}.md'

def site(code, route=''):
    return 'https://seaimagine.com/' + ('' if code == 'en' else code+'/') + route

def project_link(index, code):
    name = PROJECTS[index][1]
    if code == 'en': return f'{ORG}/{name}'
    file = f'README{GROK[code]}.md' if index == 1 else f'README_{"TW" if index == 2 and code == "tw" else SUFFIX[code]}.md'
    return f'{ORG}/{name}/blob/main/{file}'

BADGE_ASSETS = {}

def badge(label, message, color, style='flat', logo=None):
    # Shields flattens Thai and Arabic glyphs with incorrect spacing. Keep the
    # same two-color badge layout, but let the SVG text renderer shape them.
    if any('\u0600' <= c <= '\u06ff' or '\u0e00' <= c <= '\u0e7f' for c in label+message):
        size = 12 if style == 'for-the-badge' else 11
        height = 28 if style == 'for-the-badge' else 20
        def width(text):
            return max(32, int(sum(1 if unicodedata.east_asian_width(c) in 'WF' else .75 for c in text)*size)+24)
        left,right = width(label),width(message)
        fill = {'brightgreen':'#4c1','lightgrey':'#9f9f9f'}.get(color, '#'+color)
        def text(value, x):
            direction = 'rtl' if any('\u0600' <= c <= '\u06ff' for c in value) else 'ltr'
            return f'<text x="{x}" y="{height/2}" dominant-baseline="central" text-anchor="middle" direction="{direction}" fill="white" font-family="Arial, sans-serif" font-size="{size}">{html.escape(value)}</text>'
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{left+right}" height="{height}" role="img"><title>{html.escape(label+": "+message)}</title><rect width="{left}" height="{height}" fill="#555"/><rect x="{left}" width="{right}" height="{height}" fill="{fill}"/>{text(label,left/2)}{text(message,left+right/2)}</svg>\n'
        name = 'badges/'+hashlib.sha256(svg.encode()).hexdigest()[:16]+'.svg'
        BADGE_ASSETS[name] = svg
        return RAW+name
    enc = lambda s: quote(s.replace('-', '--').replace('_','__'), safe='')
    return f'https://img.shields.io/badge/{enc(label)}-{enc(message)}-{color}?style={style}' + (f'&logo={logo}' if logo else '')

def render(code):
    t = COPY[code]
    # Absolute links also work in the organization Overview, outside the repository.
    language_links = ' '.join(f'[![{COPY[c]["name"]}]({badge(COPY[c]["name"],t["current"] if c==code else t["view"],"brightgreen" if c==code else "lightgrey")})]({ORG}/.github/blob/main/profile/{filename(c)})' for c in LOCALES)
    out = [f'<div align="center">\n\n<a href="{site(code)}"><img src="{RAW}logo.png" alt="SeaImagine" width="88" height="88"></a>\n\n# SeaImagine\n\n**{t["tagline"]}**\n\n[![{t["visit"]}]({badge("SeaImagine",t["visit"],"7c3aed","for-the-badge")})]({site(code)}) [![{t["opensource"]}]({badge("GitHub",t["opensource"],"181717","for-the-badge","github")})]({ORG}?tab=repositories)\n\n</div>', '---', language_links, '---', f'## {t["intro_title"]}\n\n{t["intro"]}', f'## {t["why_title"]}\n\n{t["why"]}', f'## {t["projects_title"]}\n\n{t["image_note"]}\n\n{t["prompt_languages"]}']
    for i,(title,repo,img) in enumerate(PROJECTS):
        link=project_link(i,code)
        out.append(f'### [{title}]({link})\n\n[![{title}]({RAW}{img})]({link})\n\n{t["project_descriptions"][i]}\n\n**{t["best_for"]}** {t["project_audiences"][i]}\n\n[![{t["browse"]}]({badge(title,t["browse"],"7c3aed","for-the-badge")})]({link}) [![{t["try_model"]}]({badge("SeaImagine",t["try_model"],"181717","for-the-badge")})]({site(code,MODEL_ROUTES[i])})')
    out += [f'## {t["tools_title"]}', f'| {t["tools_title"]} | {t["best_for"].rstrip(":：")} |\n| --- | --- |']
    for i,route in enumerate(['text-to-video/','image-to-video/','ai-image-generator/','ai-photo-editor/']):
        out[-1] += f'\n| **[{t["tool_labels"][i]}]({site(code,route)})** | {t["tool_uses"][i]} |'
    out += [f'[![{t["visit"]}]({badge("SeaImagine",t["visit"],"7c3aed","for-the-badge")})]({site(code,"create/")})', f'## {t["start_title"]}\n\n'+'\n'.join(f'{i+1}. {step}' for i,step in enumerate(t['steps'])), f'## {t["contribute_title"]}\n\n{t["contribute"]}\n\n'+' · '.join(f'[{name}](https://github.com/seaimagineai/{repo}/issues)' for name,repo,_ in PROJECTS), f'<div align="center">\n\n<strong>{html.escape(t["footer"])}</strong>\n\n<a href="{site(code)}">{html.escape(t["visit"])}</a> · <a href="{ORG}?tab=repositories">{html.escape(t["opensource"])}</a>\n\n</div>']
    if code == 'ar':
        out.insert(4, '<div dir="rtl">')
        out.insert(len(out)-1, '</div>')
    return '\n\n'.join(out)+'\n'

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    bad=[]
    for code in LOCALES:
        path=ROOT/'profile'/filename(code);content=render(code)
        if args.check:
            if not path.exists() or path.read_text()!=content:bad.append(str(path.relative_to(ROOT)))
        else:path.parent.mkdir(exist_ok=True);path.write_text(content)
    for name, content in BADGE_ASSETS.items():
        path=ROOT/'assets'/name
        if args.check:
            if not path.exists() or path.read_text()!=content:bad.append(name)
        else:
            path.parent.mkdir(exist_ok=True);path.write_text(content)
    if bad:raise SystemExit('Out of date: '+', '.join(bad))
    print(f'{"Checked" if args.check else "Built"} {len(LOCALES)} profiles')
if __name__=='__main__':main()
