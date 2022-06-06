# school-bot


<p align="center">
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/python-3.10.4-3776AB?style=flat&logo=python&logoColor=yellow">
  </a>
  <a href="https://github.com/Rapptz/discord.py/">
     <img src="https://img.shields.io/badge/discord-py-blue.svg" alt="discord.py">
  </a>
  <a href="https://github.com/psf/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code Style: Black">
  </a>
  <a href="https://github.com/STROAD/school-bot/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/STROAD/school-bot" alt="license: MIT">
  </a>
  <a href="https://github.com/STROAD/school-bot/releases">
    <img src="https://img.shields.io/github/v/release/STROAD/school-bot" alt="release">
  </a>
</p>


school bot은 [Python](https://www.python.org) 3.10.4에서 [discord.py](https://github.com/Rapptz/discord.py) 라이브러리를 사용하여 만들어진 디스코드 봇 입니다.  
(사용한 Open API : [급식식단정보](https://open.neis.go.kr/portal/data/service/selectServicePage.do?page=1&rows=10&sortColumn=&sortDirection=&infId=OPEN17320190722180924242823&infSeq=2), [학사일정](https://open.neis.go.kr/portal/data/service/selectServicePage.do?page=1&rows=10&sortColumn=&sortDirection=&infId=OPEN17220190722175038389180&infSeq=1), [국토교통부_(TAGO)_버스도착정보](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15098530), [기상청_단기예보 ((구)_동네예보) 조회서비스](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15084084))


급식, 버스 도착 예정 시간, 날씨정보와 학사일정 확인 등이 가능합니다.


## 주요기능
* 급식(중식, 석식) 보기
* 버스 도착시간 보기
* 날씨정보 확인
* 학사일정 확인


## 명령어
`!도움말` 또는 `!help`로 모든 명령어를 확인할 수 있습니다.


## 설치
1. [Python](https://www.python.org)(3.10.4) 설치  
    (3.10.4 이외의 버전에서는 작동이 안될 수 있습니다.)

2. Repository clone  
    이 레포지트리를 clone합니다.  
    `$ git colne https://github.com/STROAD/school-bot.git`

3. 봇 구동에 필요한 라이브러리 설치
    ```
    pip install discord.py  
    pip install requests
    pip install pandas
    pip install python-dateutil
    ```

4. 파일 수정  
    1. config.py 파일에 자신의 봇 토큰, 인증키 등을 입력하여 주세요.  
    2. bot.py, meal.py, bus.py, weather.py, schedule.py 파일에서 `#수정하기#`를 삭제후 해당하는값을 넣어주세요.

5. 봇 실행  
    bot.py 파일을 실행해주세요.


## 라이선스
이 프로젝트는 MIT License를 사용합니다.  
자세한 내용은 [LICENSE.md](LICENSE) 파일을 참고해 주세요.
