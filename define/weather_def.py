###################################################
###################################################
############ 날씨 데이터 함수 정의 파일 ############
###################################################
###################################################

import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from define.init_def import getJSON, setJSON
from define.constant_data import jsonDatapath



# 아큐웨더 사이트에 있는 오늘의 날씨 정보를 스크래핑하여 반환해주는 함수
def setTodayWeather():
    url = "https://www.accuweather.com/ko/kr/jongno-1234-ilisamsa-ga-dong/3429990/weather-forecast/3429990" 
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"} 
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser') 
    weatherInfo = soup.find("p",attrs={"class":"no-wrap"})
    data = getJSON(jsonDatapath)
    data["todayWeatherInfo"] = weatherInfo.get_text()
    setJSON(data, jsonDatapath)


# 날씨 데이터를 가져오는 함수
def get_weather_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup


# 기온 데이터를 추출하는 함수
def extract_temperature(soup):
    temp_high = soup.find_all("span", attrs={"class": "temp-hi"})
    temp_low = soup.find_all("span", attrs={"class": "temp-lo"})
    try:
        temp_high_list = [int(th.get_text()[:-1]) for th in temp_high[1:8]]  # 첫 번째 데이터 포함
        temp_low_list = [int(tl.get_text()[:-1]) for tl in temp_low[1:8]]  # 첫 번째 데이터 포함
        temp_avg_list = [(temp_high_list[i] + temp_low_list[i]) / 2 for i in range(len(temp_high_list))]
    except:
        return False, False, False
    
    return temp_high_list, temp_low_list, temp_avg_list



# 강수량 데이터를 추출하는 함수
def extract_rainfall(soup):
    rainfall = soup.find_all("span", attrs={"class": "value"})
    try:
        rainfall_data = rainfall[5].get_text()
    except:
        return False

    return rainfall_data


# 습도 데이터를 추출하는 함수
def get_humidity_data(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')
    hum = soup.find_all("span", attrs={"data-testid": "PercentageValue", "class": "DetailsTable--value--pWEVz"})
    # <span data-testid="PercentageValue" class="DetailsTable--value--pWEVz">62%</span>

    try:
        # 오늘의 습도
        today_humidity = int(hum[0].get_text()[:-1])
        
        # 평균 습도 계산
        hList = [int(h.get_text()[:-1]) for h in hum[1:15]]
        humidity = [(hList[i] + hList[i+1]) / 2 for i in range(0, 14, 2)]
        
        # 오늘의 습도와 평균 습도를 포함한 리스트 생성
        humidity_list = [today_humidity] + humidity
    except:
        return False

    return humidity_list[1:]


# 날씨 정보를 스크래핑해서 그 값들을 data\_weather_info\newnewnewnew.csv 파일에 저장하는 함수
def setweatherInfo():
    # 베이스 URL
    base_url = "https://www.accuweather.com/ko/kr/jongno-1234-ilisamsa-ga-dong/3429990/weather-forecast/3429990"
    soup = get_weather_data(base_url)
    temp_high_list, temp_low_list, temp_avg_list = extract_temperature(soup)
    if temp_high_list and temp_low_list and temp_avg_list == False:
        return "temperature data loading error"

    # 습도 데이터 URL
    humidity_url = "https://weather.com/weather/tenday/l/4fb90f40a74b7f010fee7ce7a51958b93c8b701c089c340c92711b88eac7c663"
    humidity_list = get_humidity_data(humidity_url)
    if humidity_list == False:
        return "humidity data loading error"

    rainfall_list = []

    for day in range(2, 9):  # 내일부터 7일치 데이터를 가져옴
        url = f"https://www.accuweather.com/ko/kr/jongno-1234-ilisamsa-ga-dong/3429990/daily-weather-forecast/3429990?day={day}"
        soup = get_weather_data(url)
        returnData = extract_rainfall(soup)
        rainfall_list.append(returnData)
        if returnData == False:
            return "rainfall data loading error"

    rainfallList = []
    try:
        for data in rainfall_list:
            rainfallList.append(float(data[:-2]))
    except:
        return "rainfall data loading error2"

    file_path = [r'data\_weather_info\weekends_only.csv', r'data\umbrella\umbrella.csv']

    # 현재 날짜.
    today = datetime.now()

    # 오늘 날짜 'yyyy-mm-dd' 형식.
    target_date_str = today.strftime('%Y-%m-%d')

    # 날짜 문자열을 datetime 객체로 변환
    target_date = datetime.strptime(target_date_str, '%Y-%m-%d')
    
    i=0

    for fp in file_path:
        # 원본 CSV 파일 읽기
        df = pd.read_csv(fp)

        # measurementdate 열을 datetime 형식으로 변환
        df['measurementdate'] = pd.to_datetime(df['measurementdate'], format='%Y-%m-%d')

        # 'filtered_data' DataFrame에서 기준일(내일)부터 7일후까지의 행에 대입
        df.loc[df['measurementdate'].between(target_date + timedelta(days=1), target_date + timedelta(days=7)), 'temperature_max'] = temp_high_list
        df.loc[df['measurementdate'].between(target_date + timedelta(days=1), target_date + timedelta(days=7)), 'temperature_min'] = temp_low_list
        df.loc[df['measurementdate'].between(target_date + timedelta(days=1), target_date + timedelta(days=7)), 'temperature_avg'] = temp_avg_list
        df.loc[df['measurementdate'].between(target_date + timedelta(days=1), target_date + timedelta(days=7)), 'humidity'] = humidity_list
        df.loc[df['measurementdate'].between(target_date + timedelta(days=1), target_date + timedelta(days=7)), 'precipitation'] = rainfallList

        # 결과를 파일에 저장
        df.to_csv(fp, index=False)


# 특정 날짜의 날씨 정보를 읽어 반환하는 함수
def getPastWeather(target_date):
    # CSV 파일 읽기
    df = pd.read_csv(r'data\_weather_info\newnewnewnew.csv')

    # 날짜 열을 datetime 형식으로 변환 (yyyy-dd-mm 형식에 맞게)
    df['measurementdate'] = pd.to_datetime(df['measurementdate'], format='%Y-%m-%d')

    # 문자열을 datetime 형식으로 변환
    target_date = pd.to_datetime(target_date, format='%Y-%m-%d')

    # 특정 날짜에 해당하는 행 필터링
    filtered_row = df[df['measurementdate'] == target_date]

    # 결과 출력 (원하는 열 값만 출력)
    if not filtered_row.empty:
        # 예를 들어 'value'라는 열에서 값을 출력하려면
        weatherData = []
        weatherData.append(filtered_row['temperature_avg'].values[0])
        weatherData.append(filtered_row['windspeed_avg'].values[0])
        weatherData.append(filtered_row['humidity'].values[0])
        weatherData.append(filtered_row['precipitation'].values[0])

        for i in range(len(weatherData)):
            if weatherData[i].is_integer():
                weatherData[i] = int(weatherData[i])

        return weatherData
    else:
        return False




# 오늘의 날씨 정보를 가져와 today_weather_data.txt 파일에 저장해두는 함수
def getTodayWeatherData():
    headers = {
        'Content-Type': 'application/json'
    }

    # 현재 시간 가져오기
    now = datetime.now()

    # 분을 버리고 과거의 정각으로 설정
    tm_str = now.strftime('%Y%m%d%H') + "00"

    # print(f"측정한 시각: {tm_str}")

    # URL 생성
    url = f"https://apihub.kma.go.kr/api/typ01/url/kma_sfctm2.php?tm={tm_str}&"+"본인의 기상청 API키 입력"

    try:
        # GET 요청
        response = requests.get(url, headers=headers)

        # 응답 텍스트를 줄 단위로 분리
        lines = response.text.splitlines()

        # 데이터를 저장할 딕셔너리 초기화
        weather_data = {}

        # 날씨 데이터 라인 추출
        for line in lines:
            if line.startswith(tm_str):  # 날짜와 시간을 기준으로 필요한 데이터 라인 찾기
                fields = line.split()
                
                # 각 값이 특정 기준 이하(예: -9.0)인 경우 "Measured Unavailable"을 출력
                wind_speed = fields[3]  
                temperature = fields[11]  
                humidity = fields[13]  
                rainfall = fields[15]  

                weather_data['Wind Speed'] = wind_speed if float(wind_speed) > -9.0 else "Measured Unavailable"
                weather_data['Temperature'] = temperature if float(temperature) > -9.0 else "Measured Unavailable"
                weather_data['Humidity'] = humidity if float(humidity) > -9.0 else "Measured Unavailable"
                weather_data['precipitation'] = rainfall if float(rainfall) > -9.0 else "Measured Unavailable"
                
                break  

        with open(r'data\_weather_info\today_weather_data.txt', 'w', encoding='utf-8') as file:
                file.write(weather_data['Temperature'])
                file.write('\n')
                file.write(weather_data['Wind Speed'])
                file.write('\n')
                file.write(weather_data['Humidity'])
                file.write('\n')
                file.write(weather_data['precipitation'])
    except:
        return "기상청API 날씨 로딩 오류"


