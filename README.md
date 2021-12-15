# school-bot

school bot은 [Python](https://www.python.org) 3.9.7에서 [discord.py](https://github.com/Rapptz/discord.py) 라이브러리를 사용하여 만들어진 디스코드 봇 입니다.  
(사용한 Open API : [급식식단정보](https://open.neis.go.kr/portal/data/service/selectServicePage.do?page=1&rows=10&sortColumn=&sortDirection=&infId=OPEN17320190722180924242823&infSeq=2), [국토교통부_버스도착정보](https://www.data.go.kr/data/15000757/openapi.do))


 오늘의 급식, 내일의 급식, 버스 도착 예정 시간 확인 등이 가능합니다.


## 주요기능
* 오늘 날짜의 급식(중식) 보기
* 버스 도착시간 보기

## 명령어
`!도움말`로 모든 명령어를 확인할 수 있습니다.

## 설치
1. [Python](https://www.python.org)(3.9.7 이상) 설치  
    (3.9.7 이외의 버전에서는 작동이 안될 수 있습니다.)

2. Repository clone  
    이 레포지트리를 clone합니다.  
    `$ git colne https://github.com/STROAD/school-bot.git`

3. 봇 구동에 필요한 라이브러리 설치
    ```
    pip install discord  
    pip install requests
    ```

4. 파일 수정  
    config.py 파일에 자신의 봇 토큰, 인증키 등을 입력하여 주세요.  
    bot.py 파일에서 `#수정하기#`를 삭제후 해당하는값을 넣어주세요.  
    (통합버전(bot_integrated.py)을 사용하는 경우 bot_integrated.py파일만 수정하면 됨)

5. 봇 실행  
    bot.py(혹은 bot_integrated.py) 파일을 실행해주세요.

## 라이선스
이 프로젝트는 MIT License를 사용합니다.  
자세한 내용은 [LICENSE.md](LICENSE) 파일을 참고해 주세요.
