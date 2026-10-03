# Weather Report Program

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