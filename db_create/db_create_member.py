import pymysql

# 데이터베이스 연결
connect = pymysql.connect(host='localhost',user='root',password='0000',db='convenienceDB',charset='utf8')
cursor = connect.cursor()

# inventory 테이블이 존재하면 삭제하는 SQL문 정의
dropSQL = "drop table if exists member;"
cursor.execute(dropSQL)

# inventory테이블을 생성하는 SQL문 정의
createSQL = '''create table member(
            authority tinyint unsigned not null,
            mcode tinyint unsigned not null PRIMARY KEY,
            mid varchar(15) not null,
            mpw varchar(15) not null,
            mname varchar(10) not null,
            pname varchar(10) not null
         )default charset=utf8;'''
# categoryCode tinyint unsigned not null,

# inventory테이블 생성하는 SQL문 사용
if connect:
    cursor.execute(createSQL)

insertSQL=[
    "insert into member values(0, 0, 'rootroot', 'rootroot', '최고관리자', '')",
    "insert into member values(1, 1, '12345678', '12345678', '사용자1', 'xx공원')"
    ]

# inventory테이블에 데이터를 삽입하는 SQL문 사용
if connect:
    for sql in insertSQL:
        cursor.execute(sql)

    # 데이터베이스 데이터 변경 사항 적용
    connect.commit()

# 데이터베이스 연결 종료
connect.close()
cursor.close()