#!/usr/bin/env python3
"""Validate translated content, project metadata and generated destinations."""
import re
import json
from pathlib import Path
from build_profile import ROOT, COPY, LOCALES, PROJECTS, CATEGORIES, filename, project_link

required = {'name','tagline','visit','opensource','current','view','intro_title','intro','why_title','why','projects_title','projects_intro','best_for','browse','projects','categories','tools_title','tool_labels','tool_uses','start_title','steps','contribute_title','contribute','footer','try_model'}
remote = json.loads((ROOT/'data/project-files.json').read_text())
ids = [p['id'] for p in PROJECTS]
assert len(ids) == len(set(ids)), 'Duplicate project ID'
assert len(CATEGORIES) == len(set(CATEGORIES)), 'Duplicate category ID'
for project in PROJECTS:
    assert project['category'] in CATEGORIES, project['id']
    assert re.fullmatch(r'[A-Za-z0-9_.-]+',project['repository']), project['id']
    if project.get('image'):
        assert (ROOT/'assets'/project['image']).is_file(), project['image']
    if project.get('website_route'):
        assert not project['website_route'].startswith(('/', 'http')), project['id']
    for path in project.get('readmes', {}).values():
        assert path in remote[project['repository']], (project['repository'],path)
for code in LOCALES:
    t = COPY[code]
    assert set(t) == required, (code,'schema')
    assert all(t.values()), (code,'empty copy')
    assert set(t['projects']) == set(ids), (code,'project translations')
    assert set(t['categories']) == set(CATEGORIES), (code,'category translations')
    for p in PROJECTS:
        copy = t['projects'][p['id']]
        assert set(copy) == {'description','audience'} and all(copy.values()), (code,p['id'])
        if p.get('website_route'):
            assert p.get('website_label_key','visit') in t, p['id']
    for c in CATEGORIES:
        assert set(t['categories'][c]) == {'title','intro'} and all(t['categories'][c].values()), (code,c)
    for key,count in [('tool_labels',4),('tool_uses',4),('steps',3)]:
        assert len(t[key]) == count, (code,key)
    text = (ROOT/'profile'/filename(code)).read_text()
    assert len(re.findall(r'^#### ',text,re.M)) == len(PROJECTS), (code,'project coverage')
    assert len(re.findall(r'^### ',text,re.M)) == len({p['category'] for p in PROJECTS}), (code,'category coverage')
    for other in LOCALES: assert '/profile/'+filename(other) in text, (code,other)
    for project in PROJECTS: assert project_link(project,code) in text
    assert '/Users/' not in text and 'flaq.ai' not in text, (code,'foreign/private content')
    assert not re.search(r'TODO|TBD|Lorem ipsum',text)
print(f'Validated {len(LOCALES)} languages and {len(PROJECTS)*len(LOCALES)} project destinations')
