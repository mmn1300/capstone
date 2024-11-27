import pymysql

# 데이터베이스 연결
connect = pymysql.connect(host='localhost',user='root',password='0000',db='convenienceDB',charset='utf8')
cursor = connect.cursor()

# inventory 테이블이 존재하면 삭제하는 SQL문 정의
dropSQL = "drop table if exists inventory;"
cursor.execute(dropSQL)

# inventory테이블을 생성하는 SQL문 정의
createSQL = '''create table inventory(
            code tinyint unsigned not null,
            mcode tinyint unsigned not null,
            category varchar(4) not null,
            cname varchar(5) not null,
            name varchar(10) not null,
            quantity smallint unsigned,
            price int unsigned
         )default charset=utf8;'''
# categoryCode tinyint unsigned not null,

# inventory테이블 생성하는 SQL문 사용
if connect:
    cursor.execute(createSQL)

# 생성된 inventory테이블에 데이터를 삽입하는 SQL문을 정의
insertSQL=[
    "insert into inventory values(1, 1, '음료', '생수', '아이시스', 3000, 1000)",
    "insert into inventory values(2, 1, '식품', '아이스크림', '메로나', 3000, 1000)",
    "insert into inventory values(3, 1, '음료', '맥주', '카스', 3000, 1000)",
    "insert into inventory values(4, 1, '음료', '탄산음료', '밀키스', 3000, 1000)",
    "insert into inventory values(5, 1, '음료', '생수', '삼다수', 3000, 1000)",
    "insert into inventory values(6, 1, '음료', '탄산음료', '코카콜라', 3000, 1000)",
    "insert into inventory values(7, 1, '음료', '맥주', '테라', 3000, 1000)",
    "insert into inventory values(8, 1, '음료', '탄산음료', '환타', 3000, 1000)",
    "insert into inventory values(9, 1, '식품', '과자', '오레오', 3000, 1000)",
    "insert into inventory values(10, 1, '음료', '탄산음료', '펩시', 3000, 1000)",
    "insert into inventory values(11, 1, '식품', '라면', '신라면', 3000, 1000)",
    "insert into inventory values(12, 1, '식품', '라면', '삼양라면', 3000, 1000)",
    "insert into inventory values(13, 1, '식품', '과자', '꼬깔콘', 3000, 1000)",
    "insert into inventory values(14, 1, '기타', '우산', '검정색우산', 3000, 1000)",
    "insert into inventory values(15, 1, '기타', '우산', '청색접이식우산', 3000, 1000)",
    "insert into inventory values(16, 1, '위생용품', '마스크', 'KF94마스크', 3000, 1000)",
    "insert into inventory values(17, 1, '식품', '라면', '진라면매운맛', 3000, 1000)",
    "insert into inventory values(18, 1, '식품', '라면', '육개장컵', 3000, 1000)",
    "insert into inventory values(19, 1, '식품', '라면', '진라면순한맛', 3000, 1000)",
    "insert into inventory values(20, 1, '식품', '과자', '다이제초코', 3000, 1000)",
    "insert into inventory values(21, 1, '식품', '과자', '꿀꽈배기', 3000, 1000)",
    "insert into inventory values(22, 1, '음료', '탄산음료', '핫식스', 3000, 1000)"
]

# inventory테이블에 데이터를 삽입하는 SQL문 사용
if connect:
    for sql in insertSQL:
        cursor.execute(sql)

    # 데이터베이스 데이터 변경 사항 적용
    connect.commit()

insertSQL2=[
    "insert into inventory values(1, 2, '음료', '생수', '아이시스', 2000, 1000)",
    "insert into inventory values(2, 2, '식품', '아이스크림', '메로나', 2000, 1000)",
    "insert into inventory values(3, 2, '음료', '맥주', '카스', 2000, 1000)",
    "insert into inventory values(4, 2, '음료', '탄산음료', '밀키스', 2000, 1000)",
    "insert into inventory values(5, 2, '음료', '생수', '삼다수', 2000, 1000)",
    "insert into inventory values(6, 2, '음료', '탄산음료', '코카콜라', 2000, 1000)",
    "insert into inventory values(7, 2, '음료', '맥주', '테라', 2000, 1000)",
    "insert into inventory values(8, 2, '음료', '탄산음료', '환타', 2000, 1000)",
    "insert into inventory values(9, 2, '식품', '과자', '오레오', 2000, 1000)",
    "insert into inventory values(10, 2, '음료', '탄산음료', '펩시', 2000, 1000)",
    "insert into inventory values(11, 2, '식품', '라면', '신라면', 2000, 1000)",
    "insert into inventory values(12, 2, '식품', '라면', '삼양라면', 2000, 1000)",
    "insert into inventory values(13, 2, '식품', '과자', '꼬깔콘', 2000, 1000)",
    "insert into inventory values(14, 2, '기타', '우산', '검정색우산', 2000, 1000)",
    "insert into inventory values(15, 2, '기타', '우산', '청색접이식우산', 2000, 1000)",
    "insert into inventory values(16, 2, '기타', '우산', '청색접이식우산', 2000, 1000)",
    "insert into inventory values(17, 2, '위생용품', '마스크', 'KF94마스크', 2000, 1000)",
    "insert into inventory values(18, 2, '식품', '라면', '진라면매운맛', 2000, 1000)",
    "insert into inventory values(19, 2, '식품', '라면', '진라면순한맛', 2000, 1000)",
    "insert into inventory values(20, 2, '식품', '과자', '다이제초코', 2000, 1000)",
    "insert into inventory values(21, 2, '식품', '과자', '꿀꽈배기', 2000, 1000)",
    "insert into inventory values(22, 2, '음료', '탄산음료', '핫식스', 2000, 1000)"
]

# inventory테이블에 데이터를 삽입하는 SQL문 사용
if connect:
    for sql in insertSQL2:
        cursor.execute(sql)

    # 데이터베이스 데이터 변경 사항 적용
    connect.commit()


# 데이터베이스 연결 종료
connect.close()
cursor.close()