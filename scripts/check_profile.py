#!/usr/bin/env python3
"""Check locale parity, published project destinations and local image targets."""
import json
import re
from pathlib import Path
from urllib.parse import urlparse
from build_profile import ROOT, COPY, LOCALES, PROJECTS, RAW, filename, project_link

required = {'name','tagline','visit','opensource','current','view','intro_title','intro','why_title','why','projects_title','best_for','browse','project_descriptions','project_audiences','image_note','tools_title','tool_labels','tool_uses','start_title','steps','contribute_title','contribute','footer','try_model','prompt_languages'}
remote=json.loads((ROOT/'data/project-files.json').read_text())
for code in LOCALES:
    t=COPY[code]
    assert set(t)==required,(code,'schema')
    assert all(t.values()),(code,'empty copy')
    for key,count in [('project_descriptions',3),('project_audiences',3),('tool_labels',4),('tool_uses',4),('steps',3)]:assert len(t[key])==count,(code,key)
    path=ROOT/'profile'/filename(code);text=path.read_text()
    assert text.count('## ')==9,(code,'section coverage')
    for other in LOCALES:assert '/profile/'+filename(other) in text,(code,other)
    for i,(_,repo,img) in enumerate(PROJECTS):
        link=project_link(i,code)
        if '/blob/main/' in link:assert link.split('/blob/main/')[1] in remote[repo],link
        assert (ROOT/'assets'/img).is_file(),img
    assert '/Users/' not in text and 'flaq.ai' not in text,(code,'foreign/private content')
    assert not re.search(r'TODO|TBD|Lorem ipsum',text)
print(f'Validated {len(LOCALES)} languages, all 45 project destinations and image paths')
