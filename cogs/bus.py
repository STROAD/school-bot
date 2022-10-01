import discord
from requests import get
from xml.etree.ElementTree import fromstring
from config import OPEN_API_KEY


# 버스 API URL
Bus_URL = "http://apis.data.go.kr/1613000/ArvlInfoInqireService/getSttnAcctoSpcifyRouteBusArvlPrearngeInfoList"


# 버스정보 가져오기
async def bus_parser(nodeid, routeid):
    # 버스 파라미터
    Bus_params = {
        "serviceKey": OPEN_API_KEY,
        "cityCode": "#수정하기#",
        "nodeId": nodeid,
        "routeId": routeid,
    }

    # 버스 정보 XML로 받아오기
    response = get(Bus_URL, params=Bus_params)
    bus_xml = fromstring(response.content)

    # 호출결과 코드 찾기
    result_code = bus_xml.findtext(".//resultCode")

    # 버스 정보가 존재하는지 확인
    # 버스 정보가 있을경우
    if result_code == "00":
        bus_xml = bus_xml.find("body/items")

        # item element가 1개 아닐경우
        if len(bus_xml.findall("item")) != 1:
            # 항상 가장 먼저 도착하는 버스 정보를 받아오도록 함
            if int(bus_xml[0][1].text) < int(bus_xml[1][1].text):
                n = 0
            else:
                n = 1
        else:
            n = 0

        # 도착 예정 시간
        arrtime = int(bus_xml[n].findtext("./arrtime"))
        # 남은 정거장 수
        cnt = f'(남은 정거장 수 : {bus_xml[n].findtext("./arrprevstationcnt")})'
        # 정거장 이름
        nodenm = bus_xml[n].findtext("./nodenm")

        # 도착 예정 시간 초를 분,초로 변환
        second = arrtime % 60
        minute = int(arrtime / 60 % 60)

        bus_chk = True

    # 버스 정보가 없을경우
    else:
        cnt = None
        nodenm = None
        second = None
        minute = None
        bus_chk = False

    return cnt, nodenm, second, minute, bus_chk


# 집버스
async def bus_home(ctx):
    nodeid = "#수정하기#"
    routeid = "#수정하기#"

    cnt, nodenm, second, minute, bus_chk = await bus_parser(nodeid, routeid)

    if bus_chk == True:
        embed = discord.Embed(
            title="🚍 ***버스 도착 정보***  🚍", description="\u200B", colour=0x81C784
        )
        embed.add_field(name="**버스 정보**", value="#수정하기#", inline=False)
        embed.add_field(name="**정거장 정보**", value=nodenm, inline=False)
        embed.add_field(
            name="**버스 도착 예정 시간**", value=(f"{minute}분 {second}초 {cnt}"), inline=False
        )

    elif bus_chk == False:
        embed = discord.Embed(
            title="오류가 발생했습니다.", description="잠시 후 다시 시도해주세요.", colour=0xFF1744
        )

    await ctx.send(embed=embed, reference=ctx.message, mention_author=False)


# 학교 버스
async def bus_school(ctx):
    nodeid = "#수정하기#"
    routeid = "#수정하기#"

    cnt, nodenm, second, minute, bus_chk = await bus_parser(nodeid, routeid)

    if bus_chk == True:
        embed = discord.Embed(
            title="🚍 ***버스 도착 정보***  🚍", description="\u200B", colour=0x81C784
        )
        embed.add_field(name="**버스 정보**", value="#수정하기#", inline=False)
        embed.add_field(name="**정거장 정보**", value=nodenm, inline=False)
        embed.add_field(
            name="**버스 도착 예정 시간**", value=(f"{minute}분 {second}초 {cnt}"), inline=False
        )

    elif bus_chk == False:
        embed = discord.Embed(
            title="오류가 발생했습니다.", description="잠시 후 다시 시도해주세요.", colour=0xFF1744
        )

    await ctx.send(embed=embed, reference=ctx.message, mention_author=False)
