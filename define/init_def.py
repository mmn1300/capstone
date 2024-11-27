####################################################
####################################################
##### 초기화 및 데이터 세팅 관련 함수 정의 파일 #####
####################################################
####################################################

import json
import os
from datetime import datetime, timedelta
import holidays


def getJSON(path):
    with open(path, 'r') as file:
        data = json.load(file)
        return data
    

def setJSON(data, path):
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)


def deleteJSON(fpath):
    if os.path.exists(fpath):
        os.remove(fpath)


def variablesInit():
    config = {
        "weatherLoad" : True,
        "todayWeatherInfo" : '',
        "inventoryQuantity" : {
            "snack" : 0,
            "ramen" : 0,
            "beer" : 0,
            "razor" : 0,
            "pad" : 0,
            "hangover_cure" : 0,
            "stockings" : 0,
            "icecream" : 0,
            "mask" : 0,
            "soda" : 0,
            "umbrella" : 0,
            "water" : 0
        },
        "threeDaysPredictedSales" : {
            "snack" : 0,
            "ramen" : 0,
            "beer" : 0,
            "razor" : 0,
            "pad" : 0,
            "hangover_cure" : 0,
            "stockings" : 0,
            "icecream" : 0,
            "mask" : 0,
            "soda" : 0,
            "umbrella" : 0,
            "water" : 0
        },
        "sevenDaysPredictedSales" : {
            "snack" : 0,
            "ramen" : 0,
            "beer" : 0,
            "razor" : 0,
            "pad" : 0,
            "hangover_cure" : 0,
            "stockings" : 0,
            "icecream" : 0,
            "mask" : 0,
            "soda" : 0,
            "umbrella" : 0,
            "water" : 0
        },
        "categoryGruModelOperationStatus" : {
            "beer" : True,
            "icecream" : True,
            "mask" : True,
            "soda" : True,
            "umbrella" : True,
            "water" : True,
            "snack" : True
        }
    }

    setJSON(config, 'data/data.json')


def getUserDataPath(mcode):
    return f'data/user_{mcode}_data.json'


def userVariablesInit(mcode):
    config = {
        "yesterdaySalesRate" : {
            "snack" : 0,
            "ramen" : 0,
            "beer" : 0,
            "razor" : 0,
            "pad" : 0,
            "hangover_cure" : 0,
            "stockings" : 0,
            "icecream" : 0,
            "mask" : 0,
            "soda" : 0,
            "umbrella" : 0,
            "water" : 0
        }
    }
    setJSON(config, getUserDataPath(mcode))


def getDroidCamURL(ip):
    return f'http://{ip}:4747/mjpegfeed'


# 모델의 입력값으로 사용할 파라미터들을 세팅해서 model_data_list.txt 파일에 저장해두는 함수
def setModelInputData():
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_of_week_encoded = {day: [0]*8 for day in days_of_week}
    day_of_week_list = []

    # 오늘 날짜부터 8일간의 날짜 리스트 생성
    dates = [datetime.today() + timedelta(days=i) for i in range(0, 8)]
    datesStrList = [date.strftime('%Y-%m-%d') for date in dates]

    # 공휴일 정보 가져오기
    kr_holidays = holidays.KR(years=2024)

    # 주말 및 공휴일 확인하여 public_holiday 추가
    publicHolidayList = [1 if date in kr_holidays or date.weekday() >= 5 else 0 for date in dates]

    # 요일 원핫인코딩
    for idx, date in enumerate(dates):
        day_name = date.strftime('%A')
        day_of_week_encoded[day_name][idx] = 1

    # 요일 이름 추가
    day_of_week_list = [date.strftime('%A') for date in dates]

    with open(r'data\_weather_info\model_data_list.txt', 'w', encoding='utf-8') as file:
        file.write(json.dumps(datesStrList))
        file.write('\n')
        file.write(json.dumps(publicHolidayList))
        file.write('\n')
        file.write(json.dumps(day_of_week_list))
        file.write('\n')
        file.write(json.dumps(day_of_week_encoded))
        file.write('\n')
        file.write(json.dumps(days_of_week))


# 2024-11-11 과 같은 날짜 정보를 받아 해당 날짜가 그 해의 몇번째 날짜인지 알려주는 함수
def getDateCount(date_str):
    # 입력 받은 날짜 문자열을 datetime 객체로 변환
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    # 해당 날짜가 연도 내 몇 번째 날인지 계산
    day_of_year = date_obj.timetuple().tm_yday
    
    return day_of_year
    
    

