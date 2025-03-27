# GRU기반 날씨 예측을 활용한 수요예측 및 재고관리, 이미지 분류 판매 프로그램

---

<h4 align="center">기술 스택</h4>
<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=Python&logoColor=white"/>&nbsp
  <img src="https://img.shields.io/badge/Flask-000000?style=flat-square&logo=Flask&logoColor=white"/>&nbsp
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=FastAPI&logoColor=white"/>&nbsp
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=MySQL&logoColor=white"/>&nbsp
  <img src="https://img.shields.io/badge/Pytorch-EE4C2C?style=flat-square&logo=Pytorch&logoColor=white"/>&nbsp
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=OpenCV&logoColor=white"/>&nbsp
  <img src="https://img.shields.io/badge/DroidCam-3DDC84?style=flat-square"/>&nbsp
  <img src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white"/>&nbsp
  <img src="https://img.shields.io/badge/BeautifulSoop4-000000?style=flat-square"/>&nbsp
</div>
<div align="center">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=HTML5&logoColor=white"/>&nbsp
  <img src="https://img.shields.io/badge/CSS-663399?style=flat-square&logo=CSS&logoColor=white"/>&nbsp
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=JavaScript&logoColor=white"/>&nbsp
  <img src="https://img.shields.io/badge/ChartJS-FF6384?style=flat-square&logo=ChartdotJS&logoColor=white"/>&nbsp
  <img src="https://img.shields.io/badge/VScode-000000?style=flat-square"/>&nbsp
  <img src="https://img.shields.io/badge/Jupyter-F37626?style=flat-square&logo=Jupyter&logoColor=white"/>&nbsp
  <img src="https://img.shields.io/badge/Anaconda-44A833?style=flat-square&logo=Anaconda&logoColor=white"/>&nbsp
  <img src="https://img.shields.io/badge/Postman-FF6C37?style=flat-square&logo=Postman&logoColor=white"/>&nbsp
</div>

---

## 기능 요약
+ 주요 기능
  1. 수요예측
     ![수요예측](https://github.com/mmn1300/capstone/blob/main/img1.png)
  2. 재고관리
     ![재고조회](https://github.com/mmn1300/capstone/blob/main/img2.png)
     ![재고등록](https://github.com/mmn1300/capstone/blob/main/img8.png)
     ![판매내역](https://github.com/mmn1300/capstone/blob/main/img5.png)
     ![발주서](https://github.com/mmn1300/capstone/blob/main/img4.png)
  4. 이미지 분류 판매
     ![이미지분류](https://github.com/mmn1300/capstone/blob/main/img3.png)

---

+그외 기능
  1. 로그인
     ![로그인](https://github.com/mmn1300/capstone/blob/main/img6.png)
     ![회원가입](https://github.com/mmn1300/capstone/blob/main/img7.png)
  2. 회원 관리
    ![회원관리](https://github.com/mmn1300/capstone/blob/main/img9.png)

---

## 설치 방법
  본 프로젝트를 로컬 환경에서 동작하려면 mySQL, pytorch를 필수적으로 설치해야합니다.
  (본 프로젝트는 VSCode를 사용하여 구현하였으니 참고 바랍니다.)

  ---


  서버는 flask와 fastapi 두가지를 구축하였으니 원하는 프레임워크를 install하여 사용하시면 됩니다.

  성능이 좋지 않은 호스트에서 fastapi서버가 원할하게 동작함을 확인하였으니 참고 바랍니다.

---

  기상청 API는 다음 링크에서 발급받으실 수 있습니다.


## 사용 방법
  
  1. /db_create/ 경로의 파이썬 소스코드들을 전부 한번씩 실행하여 데이터베이스의 테이블을 생성하십시오. (중복실행하셔도 문제가 일어나지 않으니 동일 소스코드를 여러번 실행하셔도 됩니다.)
     
  2. app.py 또는 app2.py 파일 중 원하는 것을 선택해 주십시오. 각각 flask 서버, fastapi 서버입니다.
     
  3. 서버를 동작시켜주십시오. 실행 방법은 터미널에 코드를 입력하는 것입니다. (코드는 각 서버 소스코드의 최하단에 주석으로 작성해두었습니다.)
     
  4. 서버 동작시 출력되는 링크를 통해 접속하십시오.
     
  5. 계정은 일반 계정과 최고관리자 계정으로 나뉩니다. 기본적으로 제공되는 계정이 있으나 새롭게 사용하고 싶으시면 회원가입 기능을 통해 새로 계정을 생성하십시오.
      
     5-1. 기본적으로 제공되는 계정은 mysql의 member 테이블속 데이터를 참고해주십시오.
---

## 주의 사항

  1. 업로드 된 파일과 디렉토리에서 img1-img9를 제외(설명 용 이미지)한 나머지를 디렉토리를 새로 만들어 이동시키십시오.
     
  2. 파이썬 인터프리터는 pytorch가 설치된 버전을 사용하십시오.
     
  3. 사용하시기 전 convenienceDB라는 이름의 데이터베이스가 생성되어있는지 점검하십시오.
     
     또한, 데이터베이스의 테이블 생성 및 초기화 코드(db_create 디렉토리 및 모든 파이썬 파일)를 한번씩 실행하십시오.
    
  4. 데이터베이스의 비밀번호는 0000으로 통일하였으니 참고하십시오.
     
     4-1. 혹시라도 mySQL을 이미 설치하여 다른 비밀번호로 설정하셨다면 /define/database_def.py 경로의 dbConnectSetting() 함수 내부에 비밀번호를 설정하신것으로 변경해주십시오.

     4-2. 가끔씩 mariaDB를 사용하는 경우 포트번호가 중복되어 데이터베이스 이용에 문제가 발생할 수 있습니다. 이 경우 dbConnectSetting() 함수내부에 알맞는 포트번호로 변경해주십시오.
    
  5. 수요예측 기능은 날씨 데이터 정보를 필요로 합니다. 이를 위해 기상청 API 코드가 필요한데, 이는 설치 방법에 작성해두었으니 참고하십시오.
      
  6. 날씨데이터의 일부는 아큐웨더의 날씨 예보를 스크래핑하여 사용하고 있습니다. 가끔씩 아큐웨더 사이트가 변경됨에 따라 데이터가 제대로 스크래핑되지 않는 경우가 발생합니다.
     만약 이와 같은 현상이 발생한다면 /define/weather_def.py 경로에 있는 setweatherInfo() 함수 및 호출하는 하위 함수들을 수정해야합니다.

  7. 수요예측은 2024년동안만 사용이 가능합니다. 만약 2025년 이후로 동작하시려면 /data/_weather_info/ 경로의 newnewnewnew.csv 파일과 weekends_only.csv 파일을 해당 연도에 맞게 변경해야 합니다.
      
     7-1. 위 두 파일에서 의미 있는 열은 날짜와 요일, 공휴일 입니다. 그외 다른 열은 아무 데이터로 채워두셔도 좋습니다.
      
  8. 판매 메뉴는 같은 사설 네트워크를 사용하고 있는 스마트폰에서만 동작합니다. 메뉴 이용중 문제가 발생하신다면 서버와 스마트폰이 같은 사설 네트워크를 사용하고 있는지 확인하여 주십시오.
      
     8-1. 판매 메뉴를 이용중 다른 페이지를 사용하실때 Droidcam의 연결을 해제하여 주십시오. 판매 메뉴는 항상 연결이 해제되어 있는 스마트폰에서만 정상 동작합니다.

  9. 판매메뉴의 이미지 인식 기능의 CNN 가중치 파일은 용량 문제로 업로드 할 수 없습니다. 실행시 cnn5.pth파일이 없어 오류가 발생할 것이니 참고해주십시오.


---

## 참고 및 출처

[파이토치 설치] 윈도우 파이토치(Pytorch) 설치

[윈도우 파이토치 설치](https://lonaru-burnout.tistory.com/18)

---

[관리자 메뉴 -> 판매 내역] 달력 만들기

[Javascript 캘린더 만들기](https://velog.io/@eungbi/Javascript-%EC%BA%98%EB%A6%B0%EB%8D%94-%EB%A7%8C%EB%93%A4%EA%B8%B0-1)

---

[기상청 API 인증키] 인증키 발급 방법

---

[이미지 인식 모델] GS25 편의점 포스기 구현 소개 영상

[GS25 편의점 포스기 구현 소개 영상](https://www.youtube.com/watch?v=7tRORFXjcRc)

---

## 기타

  깃허브 업로드는 저작권 컨텐츠와 보안 인증키 사용으로 인해 해당 부분을 제거한 내용만을 수작업으로 업로드 하고 있습니다.
