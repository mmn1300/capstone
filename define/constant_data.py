####################################################
####################################################
###### 서버에서 상수로 사용할 데이터 정의 파일 ######
####################################################
####################################################

from datetime import datetime, timedelta

jsonDatapath = r'data/data.json'

# 현재 날짜.
today = datetime.now()

# 오늘 날짜 'yyyy-mm-dd' 형식.
todayFormattedDate = today.strftime('%Y-%m-%d')

# 어제 날짜 계산
yesterday = today - timedelta(days=1)

# 어제 날짜 'yyyy-mm-dd' 형식.
yesterdayFormattedDate = yesterday.strftime('%Y-%m-%d')

# 회원가입 승인 코드
approvalCode = 9999


categoryCode = {
    1 : "snack",
    2 : "ramen",
    3 : "mask",
    4 : "beer",
    5 : "razor",
    6 : "pad",
    7 : "water",
    8 : "hangover_cure",
    9 : "stockings",
    10 : "icecream",
    11 : "umbrella",
    12 : "soda"
}

categoryModelPath = {
    "beer" : r'model\beer\gru_model_with_arima_beer.py', #
    "icecream" : r'model\icecream\gru_model_with_arima_icecream.py',#
    "mask" : r'model\mask\catboost_model_mask.py', # 미구현
    "soda" : r'model\soda\gru_model_with_arima_soda.py', #
    "umbrella" : r'model\umbrella\catboost_model_umbrella.py', #
    "water" : r'model\water\gru_model_with_arima_water.py', #
    "snack" : r'model\snack\gru_model_with_arima_snack.py' #
}

categoryForecastingResultPath = {
    "beer" : r'data\beer\beer_forecasting.txt',
    "icecream" : r'data\icecream\icecream_forecasting.txt',
    "soda" : r'data\soda\soda_forecasting.txt',
    "umbrella" : r'data\umbrella\umbrella_forecasting.txt',
    "water" : r'data\water\water_forecasting.txt',
    "snack" : r'data\snack\snack_forecasting.txt'
}

productTypeKorenName = {
    "food" : "식품",
    "drink" : "음료",
    "sanitary_products" : "위생용품",
    "etc" : "기타"
}

categoryKoreanName = {
    "beer" : "맥주",
    "icecream" : "아이스크림",
    "mask" : "마스크",
    "soda" : "탄산음료",
    "umbrella" : "우산",
    "water" : "생수",
    "snack" : "과자",
    "ramen" : "라면",
    "razor" : "면도기",
    "hangover_cure" : "숙취해소제",
    "pad" : "생리대",
    "stockings" : "스타킹"
}

categoryImagePath = {
    "beer" : r'img/beer_img.png',
    "icecream" : r'img/icecream_img2.png',
    "mask" : r'img/mask_img.png',
    "soda" : r'img/soda_img.png',
    "umbrella" : r'img/umbrella_img.png',
    "water" : r'img/water_img.png',
    "snack" : r'img/snack_img.png'
}