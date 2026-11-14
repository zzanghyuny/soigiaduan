#!/usr/bin/env python3
"""Publish next N queued 'Thông tin dự án' posts into main working tree.
usage: python3 publish_next.py <main_repo_dir> <drafts_dir>
Skips posts already listed in main's du-an-data.js. Does nothing before queue.not_before (ICT date)."""
import sys,os,json,re,shutil,datetime
main,dr=sys.argv[1],sys.argv[2]
q=json.load(open(f'{dr}/queue.json'))
today=(datetime.datetime.utcnow()+datetime.timedelta(hours=7)).date()
if today.isoformat()<q['not_before']: print('before start date',today); sys.exit(0)
data=open(f'{main}/du-an-data.js',encoding='utf8').read()
done=set(re.findall(r'"id": "([^"]+)"',data))
todo=[x for x in q['queue'] if x['slug'] not in done][:q['per_run']]
if not todo: print('queue empty'); sys.exit(0)
lab=today.strftime('%d/%m/%Y')
for x in todo:
    s=x['slug']; h=open(f"{dr}/bai-viet/{s}.html",encoding='utf8').read()
    h=re.sub(r'Cập nhật \d\d/\d\d/\d{4}',f'Cập nhật {lab}',h,count=1)
    open(f"{main}/bai-viet/{s}.html",'w',encoding='utf8').write(h)
    dst=f"{main}/bai-viet/images/{x['folder']}"
    if os.path.exists(dst): shutil.rmtree(dst)
    shutil.copytree(f"{dr}/bai-viet/images/{x['folder']}",dst)
    # add to du-an-data.js
    arr=json.loads(re.search(r'var DUAN = (\[.*\]);',data,re.S).group(1))
    arr.append(dict(id=s,region=x['region'],tag=x['tag'],title=x['title'],date=today.isoformat(),dateLabel=lab,url=f'bai-viet/{s}.html',preview=x['preview']))
    data=re.sub(r'var DUAN = \[.*\];','var DUAN = '+json.dumps(arr,ensure_ascii=False,indent=1).replace('\\','\\\\')+';',data,flags=re.S)
    sm=open(f'{main}/sitemap.xml',encoding='utf8').read(); u=f'https://soigiaduan.com/bai-viet/{s}.html'
    if u not in sm: open(f'{main}/sitemap.xml','w',encoding='utf8').write(sm.replace('</urlset>',f'<url><loc>{u}</loc></url></urlset>'))
open(f'{main}/du-an-data.js','w',encoding='utf8').write(data)
print('published',[x['slug'] for x in todo])
