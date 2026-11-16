#!/usr/bin/env python3
"""Create a self-hosted public GitHub activity card. No external stats service."""
import datetime as dt
import json
import os
import sys
import urllib.request
import urllib.parse
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
  repositories(ownerAffiliations:OWNER, privacy:PUBLIC, isFork:false) { totalCount }
} }'''

def fetch(login, token):
    headers = {'Authorization': 'Bearer '+token, 'Accept':'application/vnd.github+json', 'User-Agent':'prism-profile', 'Content-Type':'application/json'}
    req = urllib.request.Request('https://api.github.com/graphql', data=json.dumps({'query':QUERY,'variables':{'login':login}}).encode(), headers=headers)
    with urllib.request.urlopen(req, timeout=45) as r:
        response=json.load(r)
    if response.get('errors') or not (response.get('data') or {}).get('user'):
        raise RuntimeError('GitHub contribution data is not available to this token.')
    return response['data']['user']

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
        data=fetch(os.environ['PROFILE_USER'],os.environ['GH_TOKEN'])
        OUT.write_text(render(data),encoding='utf-8')
