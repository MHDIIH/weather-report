import requests

# Weather Report Program

city = input("날씨를 확인할 지역을 입력하세요 (기본값: 서울): ").strip()

if not city:
    city = "서울"

print("\n========================================")
print("날씨 리포트")
print("========================================")

print(f"지역: {city}")
print("날씨 정보를 불러오는 중입니다...")


# 지역 이름으로 위도와 경도 찾기
geo_url = "https://geocoding-api.open-meteo.com/v1/search"

geo_params = {
    "name": city,
    "count": 1,
    "language": "ko",
    "format": "json"
}

geo_response = requests.get(geo_url, params=geo_params)
geo_data = geo_response.json()

if "results" not in geo_data:
    print("지역을 찾을 수 없습니다.")
    exit()

latitude = geo_data["results"][0]["latitude"]
longitude = geo_data["results"][0]["longitude"]

print(f"위도: {latitude}")
print(f"경도: {longitude}")


# 3일간 날씨 정보 가져오기
weather_url = "https://api.open-meteo.com/v1/forecast"

weather_params = {
    "latitude": latitude,
    "longitude": longitude,
    "hourly": [
        "temperature_2m",
        "precipitation_probability",
        "relative_humidity_2m",
        "wind_speed_10m",
        "weather_code"
    ],
    "daily": [
        "temperature_2m_max",
        "temperature_2m_min"
    ],
    "forecast_days": 3,
    "timezone": "Asia/Seoul",
    "wind_speed_unit": "ms"
}

weather_response = requests.get(weather_url, params=weather_params)
weather_data = weather_response.json()


# 날씨 코드 → 한글 날씨
def get_weather_text(code):
    if code == 0:
        return "맑음"
    elif code in [1, 2]:
        return "대체로 맑음"
    elif code == 3:
        return "흐림"
    elif code in [45, 48]:
        return "안개"
    elif code in [51, 53, 55]:
        return "이슬비"
    elif code in [61, 63, 65]:
        return "비"
    elif code in [71, 73, 75]:
        return "눈"
    elif code in [80, 81, 82]:
        return "소나기"
    elif code in [95, 96, 99]:
        return "뇌우"
    else:
        return "알 수 없음"


# 시간별 날씨 정보
times = weather_data["hourly"]["time"]
temperatures = weather_data["hourly"]["temperature_2m"]
rain_probabilities = weather_data["hourly"]["precipitation_probability"]
humidities = weather_data["hourly"]["relative_humidity_2m"]
wind_speeds = weather_data["hourly"]["wind_speed_10m"]
weather_codes = weather_data["hourly"]["weather_code"]


# 일별 날씨 정보
daily_times = weather_data["daily"]["time"]
daily_max = weather_data["daily"]["temperature_2m_max"]
daily_min = weather_data["daily"]["temperature_2m_min"]


# 시간으로 날씨 데이터 찾기
time_index = {}

for i in range(len(times)):
    time_index[times[i]] = i


# 날씨 리포트 출력
print("\n========================================")
print("☁️ 날씨 리포트 (Open-Meteo API)")
print("========================================")


# 3일간의 날씨 출력
for day in range(3):

    date = daily_times[day]
    month_day = date[5:].replace("-", ".")

    if day == 0:
        day_name = "오늘"
    elif day == 1:
        day_name = "내일"
    else:
        day_name = "모레"

    print(f"\n📅 {day_name} ({month_day}.)")
    print("----------------------------------------")

    # 오전 6시
    morning_time = date + "T06:00"
    morning_index = time_index[morning_time]

    print("🌅 오전 06:00")
    print(f"날씨: {get_weather_text(weather_codes[morning_index])}")
    print(f"기온: {temperatures[morning_index]} °C")
    print(f"강수확률: {rain_probabilities[morning_index]} %")
    print(f"습도: {humidities[morning_index]} %")
    print(f"풍속: {wind_speeds[morning_index]} m/s")

    # 오후 3시
    afternoon_time = date + "T15:00"
    afternoon_index = time_index[afternoon_time]

    print("\n🌇 오후 15:00")
    print(f"날씨: {get_weather_text(weather_codes[afternoon_index])}")
    print(f"기온: {temperatures[afternoon_index]} °C")
    print(f"강수확률: {rain_probabilities[afternoon_index]} %")
    print(f"습도: {humidities[afternoon_index]} %")
    print(f"풍속: {wind_speeds[afternoon_index]} m/s")

    # 일일 최저 / 최고 기온
    print(
        f"\n🌡️ 일일 기온: 최저 {daily_min[day]} °C / 최고 {daily_max[day]} °C"
    )

    print("----------------------------------------")