# GRU기반 날씨 예측을 활용한 수요예측 및 재고관리, 이미지 분류 판매 프로그램

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
  
  설치에 필요한 install 명령어는 다음과 같습니다.

  ---

  ---

  서버는 flask와 fastapi 두가지를 구축하였으니 원하는 프레임워크를 install하여 사용하시면 됩니다.

  성능이 좋지 않은 호스트에서 fastapi서버가 원할하게 동작함을 확인하였으니 참고 바랍니다.

---

## 사용 방법

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
     
  9. 


---

## 참고 및 출처

---

## 기타
