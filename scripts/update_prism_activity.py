#!/usr/bin/env python3
"""Create a self-hosted public GitHub activity card. No external stats service."""
import datetime as dt
import json
import os
import sys
import urllib.request
import urllib.parse
from collections import Counter
from urllib.error import HTTPError, URLError
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/prism/activity.svg'
QUERY = '''query($login:String!) { user(login:$login) {
  contributionsCollection {
    totalCommitContributions totalPullRequestContributions
    totalPullRequestReviewContributions totalIssueContributions
    contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
  }
  repositories(first:1, ownerAffiliations:OWNER, privacy:PUBLIC, isFork:false) { totalCount }
} }'''

def fetch(login, token):
    headers = {'Authorization': 'Bearer '+token, 'Accept':'application/vnd.github+json', 'User-Agent':'prism-profile', 'Content-Type':'application/json'}
    req = urllib.request.Request('https://api.github.com/graphql', data=json.dumps({'query':QUERY,'variables':{'login':login}}).encode(), headers=headers)
    with urllib.request.urlopen(req, timeout=45) as r:
        response=json.load(r)
    if response.get('errors') or not (response.get('data') or {}).get('user'):
        raise RuntimeError('GitHub contribution data is not available to this token.')
    return response['data']['user']

def fetch_public(login, token):
    login = urllib.parse.quote(login, safe='')
    def get(path):
        headers = {'Accept':'application/vnd.github+json','User-Agent':'prism-profile'}
        if token:
            headers['Authorization'] = 'Bearer '+token
        req = urllib.request.Request('https://api.github.com'+path, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except HTTPError as exc:
            if not token or exc.code not in (401,403,404):
                raise
            headers.pop('Authorization',None)
            with urllib.request.urlopen(urllib.request.Request(req.full_url,headers=headers),timeout=30) as r:
                return json.load(r)
    events = {}
    for page in range(1,4):
        batch = get(f'/users/{login}/events/public?per_page=100&page={page}')
        if not isinstance(batch,list):
            raise RuntimeError('Unexpected REST response')
        events.update({e['id']:e for e in batch})
        if len(batch)<100: break
    return list(events.values()), get(f'/users/{login}')['public_repos']

def render_public(events, repos):
    today=dt.datetime.now(dt.timezone.utc).date()
    start=today-dt.timedelta(days=29)
    counts=Counter(); days=Counter()
    for e in events:
        day=dt.date.fromisoformat(e['created_at'][:10])
        if not start<=day<=today: continue
        days[day]+=1
        typ=e['type']; action=e.get('payload',{}).get('action')
        if typ=='PushEvent': counts['push']+=1
        elif typ=='PullRequestEvent' and action=='opened': counts['pr']+=1
        elif typ=='PullRequestReviewEvent' and action=='submitted': counts['review']+=1
        elif typ=='IssuesEvent' and action=='opened': counts['issues']+=1
    b=['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="405" viewBox="0 0 1000 405" role="img" aria-label="Recent public GitHub events">','<rect x="1" y="1" width="998" height="403" rx="22" fill="#151523" stroke="#45465c"/>']
    def t(x,y,msg,size=16,color='#f5f7f2',weight=400,anchor='start'):
        b.append(f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{escape(str(msg))}</text>')
    t(28,37,'06 / GITHUB ACTIVITY',13,'#b9b5ff',600); t(28,76,'Progress, one push at a time.',29,weight=700); t(972,36,'RECENT PUBLIC EVENTS',12,'#a7b8ba',anchor='end')
    for i,(label,key) in enumerate([('PUSH EVENTS','push'),('PULL REQUESTS','pr'),('PR REVIEWS','review'),('ISSUES OPENED','issues')]):
        x=28+i*238; b.append(f'<rect x="{x}" y="99" width="226" height="92" rx="12" fill="#24243a" stroke="#45465c"/>'); t(x+14,124,label,13,'#a7b8ba',600); t(x+14,169,counts[key],36,weight=700)
    t(28,225,'Public event activity / up to 30 days',18,weight=700); t(972,225,f'{sum(days.values())} events returned',14,'#b9b5ff',600,'end')
    peak=max(days.values(),default=1) or 1
    for i in range(30):
        day=start+dt.timedelta(days=i); n=days[day]; x=30+i*31.4; h=4+76*n/peak
        b.append(f'<rect x="{x:.1f}" y="{330-h:.1f}" width="22" height="{h:.1f}" rx="3" fill="{"#b9b5ff" if n else "#45465c"}"><title>{day}: {n} public events</title></rect>')
    t(28,350,start.isoformat(),12,'#a7b8ba'); t(972,350,today.isoformat(),12,'#a7b8ba',anchor='end'); t(28,377,f'{repos} public repositories / Updated {today}',13,'#a7b8ba'); t(972,377,'REST API • not full contribution totals',13,'#a7b8ba',anchor='end'); b.append('</svg>')
    return '\n'.join(b)

def render(user=None):
    ink='#f5f7f2'; muted='#a7b8ba'; blue='#b9b5ff'; border='#45465c'; panel='#24243a'
    b=['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="405" viewBox="0 0 1000 405" role="img" aria-label="GitHub contribution activity">']
    def rect(x,y,w,h,fill,stroke='none',r=12):
        b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>')
    def text(x,y,s,size=16,color=ink,weight=400,anchor='start',family='Arial,sans-serif'):
        b.append(f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{escape(str(s))}</text>')
    rect(1,1,998,403,'#151523',border,22)
    text(28,37,'06 / GITHUB ACTIVITY',13,blue,600,family='monospace'); text(28,76,'Progress, one commit at a time.',29,ink,700)
    text(972,36,'LAST 12 MONTHS',12,muted,400,'end','monospace')
    c=user['contributionsCollection'] if user else None
    keys=[('COMMITS','totalCommitContributions'),('PULL REQUESTS','totalPullRequestContributions'),('PR REVIEWS','totalPullRequestReviewContributions'),('ISSUES OPENED','totalIssueContributions')]
    for i,(label,key) in enumerate(keys):
        x=28+i*238; rect(x,99,226,92,panel,border); text(x+14,124,label,13,muted,600); text(x+14,169,f'{c[key]:,}' if c else '—',36,ink,700)
    cal=c['contributionCalendar'] if c else None
    text(28,225,'Contribution calendar',18,ink,700)
    text(972,225,(f"{cal['totalContributions']:,} total contributions" if cal else 'Awaiting first workflow run'),14,blue,600,'end')
    if cal:
        weeks=cal['weeks'][-53:]
        max_count=max((day['contributionCount'] for week in weeks for day in week['contributionDays']),default=0)
        colors=['#25253b','#403b74','#6055ae','#8a7fe0','#b9b5ff']
        for i,week in enumerate(weeks):
            for day in week['contributionDays']:
                dow=(dt.date.fromisoformat(day['date']).weekday()+1)%7
                n=day['contributionCount']; level=0 if not n else min(4,max(1,(n*4+max_count-1)//max_count))
                rect(32+i*17.65,242+dow*15,13,12,colors[level],r=3)
        text(28,376,f"{user['repositories']['totalCount']:,} public owned repositories  /  Updated {dt.datetime.now(dt.timezone.utc).date()}",13,muted)
        text(846,376,'Less',12,muted)
        for i,col in enumerate(colors): rect(880+i*14,366,11,11,col,r=2)
        text(970,376,'More',12,muted,anchor='end')
    else:
        rect(28,242,944,105,panel,border,12)
        text(500,291,'Run “Update PRISM activity” to load your GitHub data.',17,muted,500,'middle')
        text(500,317,'No sample or invented statistics are displayed.',13,muted,400,'middle')
        text(28,376,'Source: GitHub GraphQL API / visibility depends on token access',13,muted)
    b.append('</svg>')
    return '\n'.join(b)

if __name__=='__main__':
    OUT.parent.mkdir(parents=True,exist_ok=True)
    if '--placeholder' in sys.argv:
        OUT.write_text(render(),encoding='utf-8')
    else:
        # A failed request leaves the existing dashboard untouched.
        login, token = os.environ['PROFILE_USER'], os.environ.get('GH_TOKEN','')
        try:
            result = render(fetch(login,token))
        except (RuntimeError, HTTPError, URLError, TimeoutError, KeyError, ValueError) as exc:
            print('GraphQL unavailable; using public REST events.', file=sys.stderr)
            result = render_public(*fetch_public(login,token))
        OUT.write_text(result,encoding='utf-8')
