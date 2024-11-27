import pymysql
from datetime import datetime

# 데이터베이스 연결
connect = pymysql.connect(host='localhost',user='root',password='0000',db='convenienceDB',charset='utf8')
cursor = connect.cursor()

# today_sales_rate 테이블이 존재하면 삭제하는 SQL문 정의
dropSQL = "drop table if exists today_sales_rate;"
cursor.execute(dropSQL)

# today_sales_rate 테이블 생성하는 SQL문 정의
createSQL = '''create table today_sales_rate(
            mcode tinyint unsigned not null,
            date date,
            category varchar(6) not null,
            sales_rate smallint unsigned
            )default charset=utf8;'''


# 현재 날짜.
today = datetime.now()

# 오늘 날짜 'yyyy-mm-dd' 형식.
todayFormattedDate = today.strftime('%Y-%m-%d')

# today_sales_rate 테이블 생성하는 SQL문 사용
if connect:
    cursor.execute(createSQL)

    insertSQL = [
        f"INSERT INTO today_sales_rate VALUES(1, '{todayFormattedDate}', '라면', 0)",
        f"INSERT INTO today_sales_rate VALUES(1, '{todayFormattedDate}', '과자', 0)",
        f"INSERT INTO today_sales_rate VALUES(1, '{todayFormattedDate}', '마스크', 0)",
        f"INSERT INTO today_sales_rate VALUES(1, '{todayFormattedDate}', '면도기', 0)",
        f"INSERT INTO today_sales_rate VALUES(1, '{todayFormattedDate}', '맥주', 0)",
        f"INSERT INTO today_sales_rate VALUES(1, '{todayFormattedDate}', '생리대', 0)",
        f"INSERT INTO today_sales_rate VALUES(1, '{todayFormattedDate}', '생수', 0)",
        f"INSERT INTO today_sales_rate VALUES(1, '{todayFormattedDate}', '숙취해소제', 0)",
        f"INSERT INTO today_sales_rate VALUES(1, '{todayFormattedDate}', '스타킹', 0)",
        f"INSERT INTO today_sales_rate VALUES(1, '{todayFormattedDate}', '우산', 0)",
        f"INSERT INTO today_sales_rate VALUES(1, '{todayFormattedDate}', '아이스크림', 0)",
        f"INSERT INTO today_sales_rate VALUES(1, '{todayFormattedDate}', '탄산음료', 0)"
    ]

    for sql in insertSQL:
        cursor.execute(sql)

    # 데이터베이스 데이터 변경 사항 적용
    connect.commit()


# 데이터베이스 연결 종료
connect.close()
cursor.close()