import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import catboost as cb
import matplotlib.pyplot as plt
from catboost import CatBoostRegressor, Pool
import pandas as pd
import matplotlib.pyplot as plt

# 1. 저장된 모델 가중치 불러오기
model = CatBoostRegressor()
model.load_model(r'model\umbrella\catboost_model.cbm')  # 저장된 모델 파일 경로

# 2. 새로운 데이터 불러오기 및 전처리
new_data = pd.read_csv(r'data\umbrella\umbrella.csv')

# 학습에 사용하지 않는 열 제거
X_new = new_data.drop(columns=['measurementdate', 'sales_rate'])  # 'measurementdate'와 'sales_rate' 열 제거

# 3. 카테고리형 변수 설정 (기존 학습 데이터와 동일하게 설정)
categorical_features = ['day_of_week', 'public_holiday', 'city_name']

# 새로운 데이터에 대한 Pool 생성
new_data_pool = Pool(X_new, cat_features=categorical_features)

# 4. 예측 수행
new_predictions = model.predict(new_data_pool)

# 5. 예측 결과를 DataFrame으로 변환하여 날짜와 함께 표시
new_data['predicted_sales_rate'] = new_predictions  # 예측 결과를 'predicted_sales_rate' 열로 추가

# 날짜와 예측된 판매율을 함께 출력
predictions_with_dates = new_data[['measurementdate', 'predicted_sales_rate']]
predictions_with_dates['measurementdate'] = pd.to_datetime(predictions_with_dates['measurementdate'])  # 날짜 형식으로 변환

# pandas 출력 설정 변경 (모든 데이터를 표시하도록 설정)
pd.set_option('display.max_rows', None)  # 모든 행을 표시
pd.set_option('display.max_columns', None)  # 모든 열을 표시
pd.set_option('display.width', None)  # 가로 폭에 맞게 출력
pd.set_option('display.max_colwidth', None)  # 열 너비 제한 제거

# 예측 결과 출력
print("Predictions with dates:")

filtered_data = predictions_with_dates['predicted_sales_rate']

filtered_data = filtered_data.values

i=0
with open(r'data\umbrella\umbrella_forecasting.txt', 'w') as f:
    for data in (np.round(filtered_data, 2)):
        f.write(str(data))
        if i!=len(filtered_data)-1:
            f.write('\n')
        i+=1