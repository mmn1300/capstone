import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import pandas as pd
import pickle
from sklearn.preprocessing import MinMaxScaler
from statsmodels.tsa.arima.model import ARIMA

# 학습 데이터 경로와 모델 파일 경로 설정
train_data_path = r'data\snack\snack.csv'  # 학습 데이터 파일 경로
new_data_path = r'data\_weather_info\weekends_only.csv'  # 예측에 사용할 새로운 데이터 파일 경로
model_save_path =r'model\snack\new_gru_snack.pth'  # 학습된 GRU 모델 가중치 파일 경로
arima_model_save_path = r'model\beer\new_arima_model_snack.pkl'  # 학습된 ARIMA 모델 파일 경로


# 학습 데이터 불러오기 및 스케일러 설정
train_data = pd.read_csv(train_data_path)#, encoding='cp949')

# 학습 데이터에서 예측에 사용할 피처와 목표 변수 선택
features_train = train_data.drop(columns=['measurementdate', 'sales_rate','windspeed_max','windspeed_avg'])
target_train = train_data['sales_rate']

# 학습 데이터로 스케일러 피팅
scaler_features = MinMaxScaler()
scaler_target = MinMaxScaler()

features_scaled_train = scaler_features.fit_transform(features_train)  # 피처 스케일러 설정 및 변환
target_scaled_train = scaler_target.fit_transform(target_train.values.reshape(-1, 1))  # 목표 변수 스케일러 설정 및 변환

# 새로운 데이터 불러오기
new_data = pd.read_csv(new_data_path)# , encoding='cp949'

# 새로운 데이터의 피처 선택 및 스케일링 (학습 데이터로 설정된 스케일러 사용)
features_new = new_data.drop(columns=['measurementdate', 'sales_rate','windspeed_max','windspeed_avg'])
features_scaled_new = scaler_features.transform(features_new)  # 학습한 스케일러로 새로운 데이터 변환

# 시퀀스 생성 함수 재정의
def create_sequences_with_future_weather(features, seq_length=8):
    xs = []
    for i in range(len(features) - seq_length):
        x = features[i:i + seq_length - 1]  # 과거 7일치 데이터를 가져옴
        future_day_weather = features[i + seq_length - 1].reshape(1, -1)  # 예측일의 기상 데이터
        x = np.concatenate([x, future_day_weather], axis=0)
        xs.append(x)
    return np.array(xs)

# 시퀀스 생성
X_new = create_sequences_with_future_weather(features_scaled_new)

# PyTorch 텐서로 변환
X_new = torch.tensor(X_new, dtype=torch.float32)

# GRU 모델 정의 (이전과 동일한 구조로)
class GRU(nn.Module):
    def __init__(self, input_size, hidden_layer_size=50, num_layers=1, output_size=1, dropout_prob=0.5):
        super(GRU, self).__init__()
        self.hidden_layer_size = hidden_layer_size
        self.num_layers = num_layers
        self.gru = nn.GRU(input_size, hidden_layer_size, num_layers, batch_first=True, dropout=dropout_prob)
        self.linear = nn.Linear(hidden_layer_size, output_size)
        self.relu = nn.ReLU()

    def forward(self, input_seq):
        gru_out, _ = self.gru(input_seq)
        gru_out = gru_out[:, -1]  # 마지막 타임스텝의 출력
        out = self.relu(gru_out)
        predictions = self.linear(out)
        return predictions

# 디바이스 설정
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 모델 초기화 및 가중치 불러오기
model = GRU(input_size=X_new.shape[2], dropout_prob=0.5).to(device)
model.load_state_dict(torch.load(model_save_path, map_location=device))
model.eval()

# GRU 모델 예측
gru_predictions = []
with torch.no_grad():
    for seq in X_new:
        seq = seq.unsqueeze(0).to(device)  # 배치 차원을 추가
        y_pred = model(seq)
        gru_predictions.extend(y_pred.cpu().numpy())

# 예측된 GRU 결과를 원래 스케일로 복원
gru_predictions_rescaled = scaler_target.inverse_transform(np.array(gru_predictions).reshape(-1, 1))

# ARIMA 모델 불러오기 (모델이 존재할 경우 불러오고, 없으면 새로 학습 후 저장)
try:
    with open(arima_model_save_path, 'rb') as f:
        arima_model_fit = pickle.load(f)
except FileNotFoundError:
    arima_model = ARIMA(gru_predictions_rescaled, order=(1, 1, 1))  # (p, d, q) 파라미터 조정 가능
    arima_model_fit = arima_model.fit()
    with open(arima_model_save_path, 'wb') as f:
        pickle.dump(arima_model_fit, f)

# ARIMA 잔차 예측
arima_predictions = arima_model_fit.predict(start=0, end=len(gru_predictions_rescaled) - 1)

# 최종 예측값 (GRU 예측값 + ARIMA 예측값)
final_predictions = gru_predictions_rescaled + arima_predictions.reshape(-1, 1)

with open(r'data\snack\snack_forecasting.txt', 'w') as f:
    for i in range(len(final_predictions)):
        f.write(str(round(final_predictions[i][0],2)))
        if i!=len(final_predictions)-1:
            f.write('\n')