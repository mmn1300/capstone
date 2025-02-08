import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import catboost as cb

# 저장된 모델 로드
model_path = r'gru_model\mask\catboost_mask.cbm'
loaded_model = cb.CatBoostRegressor()
loaded_model.load_model(model_path)

# 새로운 데이터 로드
new_data_path = r'gru_model\mask\mask2.csv'
new_data = pd.read_csv(new_data_path, encoding='cp949', nrows=7+0)

# 기존에 사용한 features 정의
features = ['day_of_week', 'city_name', 'public_holiday',
            'PM10_max','PM10_min','PM10_avg','PM25_max','PM25_min','PM25_avg']
cat_features = ['day_of_week', 'city_name', 'public_holiday']

# 새로운 데이터에 대한 전처리
X_new = new_data[features]

# 연속형 변수 정규화 (훈련 데이터의 스케일러 사용)
num_features = [col for col in features if col not in cat_features]
scaler = StandardScaler()
X_new[num_features] = scaler.fit_transform(X_new[num_features])

# 예측 수행
y_pred_new = loaded_model.predict(X_new)

# 예측 결과를 새로운 데이터프레임에 추가
new_data['predicted_sales_rate'] = y_pred_new

prediction_list = list(new_data['predicted_sales_rate'].values)
f = open(r'data\mask\mask_forecasting.txt', 'w')
for d in prediction_list[:-1]:
    f.write(str(round(d,2)))
    f.write('\n')
f.write(str(round(prediction_list[-1], 2)))
f.close()