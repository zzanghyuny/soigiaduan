# Soi Giá Dự Án - 배포 안내

## 파일 배치
- 정적 사이트 파일은 저장소 루트에 둡니다.
- Palm River 글은 bai-viet/palm-river-gia-hop-ly.html 위치에 둡니다. 홈페이지·사이트맵의 경로 및 글의 ../style.css 참조와 일치하도록 정리했습니다.
- UUID가 붙은 중복 글 파일과 첨부 이미지(image.png)는 사이트 파일이 아니므로 제외했습니다.

## Vercel 배포
1. 이 폴더의 내용을 새 GitHub 저장소 루트에 올립니다.
2. Vercel에서 해당 저장소를 Import합니다. Framework Preset은 Other, Build Command는 비우고 Output Directory는 . 또는 기본값으로 둡니다.
3. 배포 후 홈페이지와 /bai-viet/palm-river-gia-hop-ly.html, 정책 페이지, /robots.txt, /sitemap.xml을 확인합니다.
4. soigiaduan.com 도메인을 실제 등록한 뒤 Vercel 프로젝트에 연결하세요. 등록 여부는 아직 확인되지 않았습니다. 실제 사용할 도메인이 다르면 sitemap.xml과 robots.txt의 도메인을 먼저 수정하세요.
5. ads.txt는 AdSense 승인 후 발급된 publisher ID로 바꿉니다. 현재는 안내 주석만 있어 광고 인증 파일로는 작동하지 않습니다.

## Git 명령
 git add -A
 git commit -m "Initial site: Palm River analysis"
 git push -u origin main

주의: Palm River 글은 임시 가격 분석입니다. 게시 전 베트남어 표현과 데이터·법률 출처를 확인하세요.
