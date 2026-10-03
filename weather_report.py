# Weather Report Program
import requests
# Get the city name from the user
city = input("날씨를 확인할 지역을 입력하세요 (기본값: 서울): ").strip()

# Use Seoul as the default city
if not city:
    city = "서울"

print("\n========================================")
print("날씨 리포트")
print("========================================")

print(f"지역: {city}")
print("날씨 정보를 불러오는 중입니다...")
# Find the coordinates of the city
url = "https://geocoding-api.open-meteo.com/v1/search"
params = {
    "name": city,
    "count": 1,
    "language": "ko",
    "format": "json"
}

response = requests.get(url, params=params)
data = response.json()

if "results" in data:
    latitude = data["results"][0]["latitude"]
    longitude = data["results"][0]["longitude"]

    print(f"위도: {latitude}")
    print(f"경도: {longitude}")
else:
    print("지역을 찾을 수 없습니다.")