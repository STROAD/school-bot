from discord import Embed
from datetime import datetime
import requests
from config import open_API_KEY


# 날씨 API URL
weather_URL = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"


# 날씨
async def weather(ctx):
    # 날짜, 시간 구하기
    now_date = int(datetime.now().strftime("%Y%m%d"))
    yes_date = int(datetime.now().strftime("%Y%m%d")) - 1
    now_hour = int(datetime.now().strftime("%H"))
    now_min = int(datetime.now().strftime("%M"))

    # API 제공 시간에 맞춰 가장 최신의 정보를 받을 수 있는 시간을 설정
    if now_hour < 2 or (now_hour == 2 and now_min <= 10):
        base_date = yes_date
        base_time = "2300"
    elif now_hour < 5 or (now_hour == 5 and now_min <= 10):
        base_date = now_date
        base_time = "0200"
    elif now_hour < 8 or (now_hour == 8 and now_min <= 10):
        base_date = now_date
        base_time = "0500"
    elif now_hour < 11 or (now_hour == 11 and now_min <= 10):
        base_date = now_date
        base_time = "0800"
    elif now_hour < 14 or (now_hour == 14 and now_min <= 10):
        base_date = now_date
        base_time = "1100"
    elif now_hour < 17 or (now_hour == 17 and now_min <= 10):
        base_date = now_date
        base_time = "1400"
    elif now_hour < 20 or (now_hour == 20 and now_min <= 10):
        base_date = now_date
        base_time = "1700"
    elif now_hour < 23 or (now_hour == 23 and now_min <= 10):
        base_date = now_date
        base_time = "2000"
    else:
        base_date = now_date
        base_time = "2300"

    # 날씨 파라미터
    weather_params = {
        "ServiceKey": open_API_KEY,
        "pageNo": "1",
        "numOfRows": "12",
        "dataType": "JSON",
        "base_date": base_date,
        "base_time": base_time,
        "nx": "#수정하기#",
        "ny": "#수정하기#",
    }

    # 날씨정보 JSON으로 받아오기
    response = requests.get(weather_URL, params=weather_params).json()
    # 호출결과 코드
    resultCode = response["response"]["header"]["resultCode"]

    # 정상적으로 호출되었을 경우
    if resultCode == "00":
        # 날씨정보
        weather_data = response.get("response").get("body").get("items")

        # 날씨정보 추출
        for item in weather_data["item"]:
            # 1시간 기온
            if item["category"] == "TMP":
                tmp = item["fcstValue"]

            # 하늘상태
            if item["category"] == "SKY":
                sky_code = item["fcstValue"]

                if sky_code == "1":
                    sky = "맑음"
                elif sky_code == "3":
                    sky = "구름많음"
                elif sky_code == "4":
                    sky = "흐림"
                else:
                    sky = "정보없음"

            # 강수형태
            if item["category"] == "PTY":
                pty_code = item["fcstValue"]

                if pty_code == "0":
                    pty = "강수없음"
                elif pty_code == "1":
                    pty = "비"
                elif pty_code == "2":
                    pty = "비/눈"
                elif pty_code == "3":
                    pty = "눈"
                elif pty_code == "4":
                    pty = "소나기"
                else:
                    pty = "정보없음"

            # 강수확률
            if item["category"] == "POP":
                pop = item["fcstValue"]

            # 1시간 강수량
            if item["category"] == "PCP":
                pcp = item["fcstValue"]

            # 습도
            if item["category"] == "REH":
                reh = item["fcstValue"]

            # 1시간 신적설
            if item["category"] == "SNO":
                sno = item["fcstValue"]

    # 정상적으로 호출되지 못했을 경우
    else:
        embed = Embed(title="오류!", description="잠시후 다시 시도해주시기 바랍니다.")

        await ctx.send(embed=embed, reference=ctx.message, mention_author=False)

    embed = Embed(title="***날씨 정보***", description="#수정하기#동", colour=0x2196F3)
    embed.add_field(name="***기온***", value=f"{tmp}°C")
    embed.add_field(name="***습도***", value=f"{reh}%")
    embed.add_field(name="***하늘***", value=f"{sky}")
    embed.add_field(name="***강수확률***", value=f"{pop}%")
    # 강수형태가 있을 경우에만 임베드 추가
    if pty_code != "0":
        embed.add_field(name="**강수형태**", value=f"{pty}")
    # 강수량이 있을 경우에만 임베드 추가
    if pcp != "강수없음":
        embed.add_field(name="**강수량**", value=f"{pcp}")
    # 적설이 있을 경우에만 임베드 추가
    if sno != "적설없음":
        embed.add_field(name="**적설량**", value=f"{sno}")

    await ctx.send(embed=embed, reference=ctx.message, mention_author=False)
