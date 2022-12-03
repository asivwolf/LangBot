from nonebot import on_command, CommandSession
import requests

#  on_command 装饰器将函数声明为一个命令处理器
# 这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」
@on_command('weather', aliases=('天气', '天气预报', '查天气'))
async def weather(session: CommandSession):
    # 取得消息的内容，并且去掉首尾的空白符
    city = session.current_arg_text.strip()
    # 如果除了命令的名字之外用户还提供了别的内容，即用户直接将城市名跟在命令名后面，
    # 则此时 city 不为空。例如用户可能发送了："天气 南京"，则此时 city == '南京'
    # 否则这代表用户仅发送了："天气" 二字，机器人将会向其发送一条消息并且等待其回复
    if not city:
        city = (await session.aget(prompt='你想查询哪个城市的天气呢？')).strip()
        # 如果用户只发送空白符，则继续询问
        while not city:
            city = (await session.aget(prompt='要查询的城市名称不能为空呢，请重新输入')).strip()
    # 获取城市的天气预报
    weather_report = await get_weather_of_city(city)
    # 向用户发送天气预报
    await session.send(weather_report)

def get_json(url):
    r = requests.get(url)
    json_data = r.json()
    return json_data

async def get_weather_of_city(city: str) -> str:
    # 这里简单返回一个字符串
    # 实际应用中，这里应该调用返回真实数据的天气 API，并拼接成天气预报内容
    #高德地图API
    url = 'https://restapi.amap.com/v3/weather/weatherInfo?city='+city+'&key=6a88d2ecfe07d33646486102d2a90dd6'
    #请求API
    print(url)
    weather_data = get_json(url)
    print(weather_data)
    if weather_data['status'] == '0' or weather_data['count'] == '0':
        return "查询失败,请重试o(╥﹏╥)o"
    elif weather_data['count'] == '1':
        #获取当日天气数据
        lives = weather_data['lives'][0]
        temperature = lives['temperature']
        weather = lives['weather']
        humidity = lives['humidity']
        reporttime = lives['reporttime']
        return city+'的天气为：'+weather+'，温度为：'+temperature+'，更新时间为：'+reporttime
    else:
        #str->int
        city_num = int(weather_data['count'])
        welcome="查询到"+str(city_num)+"个城市：\n"
        for i in range(city_num):
            #获取当日天气数据
            lives = weather_data['lives'][i]
            province = lives['province']
            city = lives['city']
            temperature = lives['temperature']
            weather = lives['weather']
            humidity = lives['humidity']
            welcome=welcome+province+city+'的天气为：'+weather+'，温度为：'+temperature+'，湿度为：'+humidity+'；\n'
        return welcome
    #return f'{city}的天气是……'