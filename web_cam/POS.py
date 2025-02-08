import cv2
import torch
import torchvision.transforms as transforms
from PIL import Image
import torch.nn as nn
import torch.nn.functional as F
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# Net 클래스 정의
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, 3, padding=1)  # 첫 번째 Convolution Layer
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)  # 두 번째 Convolution Layer
        self.conv3 = nn.Conv2d(64, 128, 3, padding=1)  # 세 번째 Convolution Layer
        self.pool = nn.MaxPool2d(2, 2)  # Max Pooling Layer
        self.fc1 = nn.Linear(128 * 28 * 28, 512)  # 첫 번째 Fully Connected Layer
        self.fc2 = nn.Linear(512, 256)  # 두 번째 Fully Connected Layer
        self.fc3 = nn.Linear(256, 6)  # 출력 Layer

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))  # 첫 번째 Convolution + ReLU + Pooling
        x = self.pool(F.relu(self.conv2(x)))  # 두 번째 Convolution + ReLU + Pooling
        x = self.pool(F.relu(self.conv3(x)))  # 세 번째 Convolution + ReLU + Pooling
        x = torch.flatten(x, 1)  # 평탄화 (Flatten)
        x = F.relu(self.fc1(x))  # 첫 번째 Fully Connected + ReLU
        x = F.relu(self.fc2(x))  # 두 번째 Fully Connected + ReLU
        x = self.fc3(x)  # 출력 Layer
        return x

# 모델 로드
net = Net()
net.load_state_dict(torch.load('web_cam/cnn5.pth', map_location=torch.device('cpu')))
net.eval()

# 클래스 정의
classes = ('cass', 'cokacola', 'fanta', 'icis', 'samdasu', 'tera')

category = {
    'cass' : '맥주',
    'cokacola' : '탄산음료',
    'icis' : '생수',
    'merona' : '아이스크림',
    'milkis' : '탄산음료',
    'samdasu' : '생수',
    'fanta' : '탄산음료',
    'tera' : '맥주'
}

classKoreanName = {
    'cass' : '카스',
    'cokacola' : '코카콜라',
    'icis' : '아이시스',
    'merona' : '메로나',
    'milkis' : '밀키스',
    'samdasu' : '삼다수',
    'tera' : '테라',
    'fanta' : '환타'
}

itemImagePath = {
    '카스' : '/static/item_img/cass.jpg',
    '코카콜라' : '/static/item_img/cokacola.jpg',
    '아이시스' : '/static/item_img/icis.jpg',
    '메로나' : '/static/item_img/merona.jpg',
    '밀키스' : '/static/item_img/milkis.jpg',
    '삼다수' : '/static/item_img/samdasu.jpg',
    '테라' : '/static/item_img/tera.jpg',
    '환타' : '/static/item_img/fanta.jpg'
}

# 이미지 전처리
transform = transforms.Compose([
    transforms.Resize((224, 224)),  # 이미지 크기 조정
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

# 전역 변수
current_frame = None


# 새로운 이미지 예측 함수
def predict_image(image):
    image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))  # OpenCV 이미지를 PIL 이미지로 변환
    image = transform(image).unsqueeze(0)  # 배치 차원 추가

    with torch.no_grad():
        outputs = net(image)
        _, predicted = torch.max(outputs, 1)
    
    return classes[predicted.item()]


def generate_frames(url):
    global current_frame
    cap = cv2.VideoCapture(url)  # 카메라 인덱스 설정 (0은 기본 카메라)
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        global current_frame
        current_frame = frame.copy()  # 현재 프레임 저장

        # 비디오 프레임을 JPEG로 인코딩
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        # 프레임을 HTTP 응답으로 반환
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')