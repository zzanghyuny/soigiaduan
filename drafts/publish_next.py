#!/usr/bin/env python3
"""Publish queued 'Thông tin dự án' posts on a fixed schedule: 09:00 and 20:00 Vietnam time (ICT, UTC+7).
usage: python3 publish_next.py <main_repo_dir> <drafts_dir>
Each queued post is assigned the next free slot (09:00 / 20:00 ICT). A post's files are written to main up to
LOOKAHEAD_H hours before its slot, with `publishAt` set; the site hides it until that time (feed.js).
Safe to run often (hourly): it only writes what is due. Env PUBLISH_NOW=ISO8601 overrides the clock (tests)."""
import sys,os,json,re,shutil,datetime as dt
main,dr=sys.argv[1],sys.argv[2]
ICT=dt.timezone(dt.timedelta(hours=7)); LOOKAHEAD_H=12; HOURS=(9,20)
now=dt.datetime.fromisoformat(os.environ['PUBLISH_NOW']) if os.environ.get('PUBLISH_NOW') else dt.datetime.now(dt.timezone.utc)
now=now.astimezone(ICT)
q=json.load(open(f'{dr}/queue.json'))
data=open(f'{main}/du-an-data.js',encoding='utf8').read()
arr=json.loads(re.search(r'var DUAN = (\[.*\]);',data,re.S).group(1))
done={p['id'] for p in arr}
pend=[p['publishAt'] for p in arr if p.get('publishAt')]
last=max(dt.datetime.fromisoformat(x) for x in pend) if pend else None
def next_slot(after):
    d=after.date()
    for add in range(0,3):
        for h in HOURS:
            s=dt.datetime(d.year,d.month,d.day,h,0,tzinfo=ICT)+dt.timedelta(days=add)
            if s>after: return s
start=max(now,last) if last else now
todo=[x for x in q['queue'] if x['slug'] not in done]
if now.date().isoformat()<q.get('not_before','2000-01-01'): print('before start date'); sys.exit(0)
published=[]; cur=start
for x in todo:
    slot=next_slot(cur)
    if slot>now+dt.timedelta(hours=LOOKAHEAD_H): break
    s=x['slug']; h=open(f"{dr}/bai-viet/{s}.html",encoding='utf8').read()
    lab=slot.strftime('%d/%m/%Y')
    h=re.sub(r'Cập nhật \d\d/\d\d/\d{4}',f'Cập nhật {lab}',h,count=1)
    open(f"{main}/bai-viet/{s}.html",'w',encoding='utf8').write(h)
    dst=f"{main}/bai-viet/images/{x['folder']}"
    if os.path.exists(dst): shutil.rmtree(dst)
    shutil.copytree(f"{dr}/bai-viet/images/{x['folder']}",dst)
    arr.append(dict(id=s,region=x['region'],tag=x['tag'],title=x['title'],date=slot.date().isoformat(),dateLabel=lab,url=f'bai-viet/{s}.html',preview=x['preview'],publishAt=slot.isoformat()))
    sm=open(f'{main}/sitemap.xml',encoding='utf8').read(); u=f'https://soigiaduan.com/bai-viet/{s}.html'
    if u not in sm: open(f'{main}/sitemap.xml','w',encoding='utf8').write(sm.replace('</urlset>',f'<url><loc>{u}</loc></url></urlset>'))
    published.append((s,slot.isoformat())); cur=slot
if published:
    new=re.sub(r'var DUAN = \[.*\];',lambda m:'var DUAN = '+json.dumps(arr,ensure_ascii=False,indent=1)+';',data,flags=re.S)
    open(f'{main}/du-an-data.js','w',encoding='utf8').write(new)
    print('scheduled',published)
else: print('nothing due; next slot',next_slot(start).isoformat(),'pending',len(todo))
