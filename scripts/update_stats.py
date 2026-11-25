"""Generate a self-contained SVG from live GitHub GraphQL data."""
import json, os, urllib.request
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

query = '''query($login:String!){user(login:$login){repositories(privacy:PUBLIC,ownerAffiliations:[OWNER],first:1){totalCount} followers{totalCount} contributionsCollection{contributionCalendar{totalContributions}}}}'''

def render(values=None):
    labels = ('Public repositories', 'Visible contributions / 1 year', 'Followers')
    data = values or ('—', '—', '—')
    note = 'Awaiting first successful GitHub Actions run' if values is None else 'Updated ' + datetime.now(timezone.utc).strftime('%Y-%m-%d UTC') + ' / GitHub API'
    cards = ''
    for i, (label, val) in enumerate(zip(labels, data)):
        x = 25 + i * 320
        cards += f'<rect x="{x}" y="61" width="310" height="97" rx="12" fill="#0d1728" stroke="#233a51"/><text x="{x+16}" y="90" font-size="15" fill="#92a8c2">{escape(label)}</text><text x="{x+16}" y="133" font-size="34" font-weight="700" fill="#5bf0e0">{escape(str(val))}</text>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="205" viewBox="0 0 1000 205" role="img" aria-label="GitHub statistics"><rect x="1" y="1" width="998" height="203" rx="22" fill="#0a1423" stroke="#233a51" stroke-width="2"/><g font-family="Arial,sans-serif"><text x="25" y="33" font-size="17" font-weight="700" fill="#ecf4fd">GITHUB / ACTIVITY</text><text x="975" y="32" text-anchor="end" font-size="12" fill="#92a8c2">LIVE DATA</text>{cards}<text x="25" y="185" font-size="12" fill="#92a8c2">{escape(note)}</text></g></svg>'''

def main():
    req = urllib.request.Request('https://api.github.com/graphql', data=json.dumps({'query':query,'variables':{'login':os.environ['PROFILE_USER']}}).encode(), headers={'Authorization':'Bearer '+os.environ['GITHUB_TOKEN'],'Content-Type':'application/json','User-Agent':'profile-activity-workflow'})
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.load(response)
    if result.get('errors') or not result.get('data',{}).get('user'):
        raise RuntimeError('GitHub GraphQL did not return complete user data: '+str(result.get('errors','user not found')))
    u = result['data']['user']
    values = (u['repositories']['totalCount'],u['contributionsCollection']['contributionCalendar']['totalContributions'],u['followers']['totalCount'])
    Path('assets/stats.svg').write_text(render(values),encoding='utf-8')

if __name__ == '__main__':
    main()
