# 웨일 일러스트 배경테마 공모전 통계 크롤러
## 개발배경
2022년 7월에 진행된 [웨일 일러스트 배경테마 공모전](https://store.whale.naver.com/event/wallpaper-contest)에 참여한 친구가 본인의 작품 투표 순위를 확인하는 것을 도와주기 위해 개발하였습니다.
## 라이브러리
- [selenium](https://www.selenium.dev/documentation/webdriver/) with [chromedriver](https://chromedriver.chromium.org/home)   
공모전 홈페이지에서 작품 정보를 가져올 때 이용했습니다.
- [yattag](https://www.yattag.org/)   
가져온 정보를 HTML 형식의 보고서로 내보내기 위해 이용했습니다.
## 설명
1. 공모전 홈페이지에서 작품 전체 리스트를 가져옵니다.
2. 각 작품의 페이지에 접속하여 정보(제목, 작가명, 투표수 등)를 가져옵니다.
3. 수집된 작품별 정보 리스트를 투표수 기준으로 내림차순 정렬하고 순위와 퍼센트를 리스트의 앞에 추가시킵니다.
4. 가공된 리스트를 바탕으로 HTML 형식의 보고서를 작성합니다.
## 회고
800개가 넘는 작품 페이지에 일일이 접속하여 정보를 가져오는 것이 무척이나 오래 걸립니다. 이 때문에 멀티프로세싱([multiprocessing](https://docs.python.org/ko/3/library/multiprocessing.html))을 이용하여 여러 창을 띄워 작업을 나눠보려 했지만 별다른 속도 향상이 없었습니다.   
selenium 대신 [requests](https://requests.readthedocs.io/en/latest/) 라이브러리를 이용하면 더 빠른 속도를 기대할 수 있었습니다. 하지만 공모전 홈페이지는 페이지 틀이 로드된 이후에 내용물이 이어서 로드됩니다. 그래서 페이지 틀 이후에 로드되는 정보를 가져올 수 없었습니다.