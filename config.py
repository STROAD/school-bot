import discord


# 토큰
TOKEN = ""  # 이곳에 자신의 디스코드 봇 토큰 넣기


# Discord Bot APPLICATION ID
APPLICATION_ID = int()  # 이곳에 자신의 디스코드 봇 APPLICATION ID 넣기


# 디스코드 봇 상태 설정
bot_status = discord.Status.online
bot_activity = discord.Activity(type=discord.ActivityType.listening, name="/도움말")


# 인증키
NIES_KEY = ""  # 이곳에 자신의 나이스 Open API 인증키 입력
OPEN_API_KEY = ""  # 이곳에 자신의 공공데이터포털 Open API 인증키 입력, 버스 및 날씨정보 API에 이용됨


# 시간표
schedule = """
```
ㅤ| 월요일 | 화요일 | 수요일 | 목요일 | 금요일 |
1 |ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|
2 |ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|
3 |ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|
4 |ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|
5 |ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|
6 |ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|
7 |ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|ㅤ과목ㅤ|
```
"""


# GitHub 주소
GITHUB = "https://github.com/STROAD/school-bot"
