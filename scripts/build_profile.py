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
MANIFEST = json.loads((ROOT/'data/projects.json').read_text())
PROJECTS = MANIFEST['projects']
CATEGORIES = MANIFEST['categories']
REPOSITORIES = ORG + '?tab=repositories'

def filename(code):
    return 'README.md' if code == 'en' else f'README_{code}.md'

def site(code, route=''):
    return 'https://seaimagine.com/' + ('' if code == 'en' else code+'/') + route

def project_link(project, code):
    repository = f"{ORG}/{project['repository']}"
    readmes = project.get('readmes', {})
    file = readmes.get(code, readmes.get('en'))
    return f'{repository}/blob/main/{file}' if file else repository

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

def render_project(project, code):
    t = COPY[code]
    copy = t['projects'][project['id']]
    title = project['title']
    link = project_link(project, code)
    out = [f'#### [{title}]({link})']
    if project.get('image'):
        out.append(f'[![{title}]({RAW}{project["image"]})]({link})')
    out += [copy['description'], f'**{t["best_for"]}** {copy["audience"]}']
    buttons = f'[![{t["browse"]}]({badge(title,t["browse"],"7c3aed","for-the-badge")})]({link})'
    if project.get('website_route'):
        label = t[project.get('website_label_key', 'visit')]
        buttons += f' [![{label}]({badge("SeaImagine",label,"181717","for-the-badge")})]({site(code,project["website_route"])})'
    out.append(buttons)
    return '\n\n'.join(out)

def render(code):
    t = COPY[code]
    language_links = ' '.join(f'[![{COPY[c]["name"]}]({badge(COPY[c]["name"],t["current"] if c==code else t["view"],"brightgreen" if c==code else "lightgrey")})]({ORG}/.github/blob/main/profile/{filename(c)})' for c in LOCALES)
    out = [f'<div align="center">\n\n<a href="{site(code)}"><img src="{RAW}logo.png" alt="SeaImagine" width="88" height="88"></a>\n\n# SeaImagine\n\n**{t["tagline"]}**\n\n[![{t["visit"]}]({badge("SeaImagine",t["visit"],"7c3aed","for-the-badge")})]({site(code)}) [![{t["opensource"]}]({badge("GitHub",t["opensource"],"181717","for-the-badge","github")})]({REPOSITORIES})\n\n</div>', '---', language_links, '---']
    if code == 'ar': out.append('<div dir="rtl">')
    out += [f'## {t["intro_title"]}\n\n{t["intro"]}', f'## {t["why_title"]}\n\n{t["why"]}', f'## {t["projects_title"]}\n\n{t["projects_intro"]}']
    for category in CATEGORIES:
        projects = [p for p in PROJECTS if p['category'] == category]
        if not projects: continue
        copy = t['categories'][category]
        out.append(f'### {copy["title"]}\n\n{copy["intro"]}')
        out.extend(render_project(project,code) for project in projects)
    out.append(f'[![{t["opensource"]}]({badge("GitHub",t["opensource"],"181717","for-the-badge","github")})]({REPOSITORIES})')
    out += [f'## {t["tools_title"]}', f'| {t["tools_title"]} | {t["best_for"].rstrip(":：")} |\n| --- | --- |']
    for i,route in enumerate(['text-to-video/','image-to-video/','ai-image-generator/','ai-photo-editor/']):
        out[-1] += f'\n| **[{t["tool_labels"][i]}]({site(code,route)})** | {t["tool_uses"][i]} |'
    out += [f'[![{t["visit"]}]({badge("SeaImagine",t["visit"],"7c3aed","for-the-badge")})]({site(code,"create/")})', f'## {t["start_title"]}\n\n'+'\n'.join(f'{i+1}. {step}' for i,step in enumerate(t['steps'])), f'## {t["contribute_title"]}\n\n{t["contribute"]}']
    out.append(' · '.join(f'[{p["title"]}]({ORG}/{p["repository"]}/issues)' for p in PROJECTS))
    if code == 'ar': out.append('</div>')
    out.append(f'<div align="center">\n\n<strong>{html.escape(t["footer"])}</strong>\n\n<a href="{site(code)}">{html.escape(t["visit"])}</a> · <a href="{REPOSITORIES}">{html.escape(t["opensource"])}</a>\n\n</div>')
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
