import nextcord
import requests
import xml.etree.ElementTree as ET
from config import open_API_KEY


# 버스 API URL
Bus_URL = "http://openapi.tago.go.kr/openapi/service/\
ArvlInfoInqireService/getSttnAcctoSpcifyRouteBusArvlPrearngeInfoList"


# 버스정보 가져오기
async def bus_parser(Bus_params):
    global minute, second, cnt, nodenm

    # 버스 정보 XML로 받아오기
    response = requests.get(Bus_URL, params=Bus_params)
    bus_xml = ET.fromstring(response.content)

    # 도착 예정 시간
    arrtime = int(bus_xml.findtext(".//arrtime"))
    # 남은 정거장 수
    cnt = f"(남은 정거장 수 : {bus_xml.findtext('.//arrprevstationcnt')})"
    # 정거장 이름
    nodenm = bus_xml.findtext(".//nodenm")

    # 도착 예정 시간 초를 분,초로 변환
    second = arrtime % 60
    minute = int(arrtime / 60 % 60)


# 집버스
async def bus_home(ctx):
    # 버스 파라미터
    Bus_params = {
        "serviceKey": open_API_KEY,
        "cityCode": "#수정하기#",
        "nodeId": "#수정하기#",
        "routeId": "#수정하기#",
    }

    await bus_parser(Bus_params)

    embed = nextcord.Embed(
        title="***버스 도착 정보***", description="\u200B", colour=0x2196F3
    )
    embed.add_field(name="**버스 정보**", value="#수정하기#", inline=False)
    embed.add_field(name="**정거장 정보**", value=nodenm, inline=False)
    embed.add_field(
        name="**버스 도착 예정 시간**", value=(f"{minute}분 {second}초 {cnt}"), inline=False
    )

    await ctx.send(embed=embed, reference=ctx.message, mention_author=False)


# 학교 버스
async def bus_school(ctx):
    # 버스 파라미터
    Bus_params = {
        "serviceKey": open_API_KEY,
        "cityCode": "#수정하기#",
        "nodeId": "#수정하기#",
        "routeId": "#수정하기#",
    }

    await bus_parser(Bus_params)

    embed = nextcord.Embed(
        title="***버스 도착 정보***", description="\u200B", colour=0x2196F3
    )
    embed.add_field(name="**버스 정보**", value="#수정하기#", inline=False)
    embed.add_field(name="**정거장 정보**", value=nodenm, inline=False)
    embed.add_field(
        name="**버스 도착 예정 시간**", value=(f"{minute}분 {second}초 {cnt}"), inline=False
    )

    await ctx.send(embed=embed, reference=ctx.message, mention_author=False)
