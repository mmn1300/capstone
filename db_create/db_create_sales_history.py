import pymysql
import csv

# csv에 존재하는 데이터는 상품명, 판매량, 날짜 이므로
# 결과에 출력할 카테고리와 상품코드를 상품명을 이용해 매칭. 딕셔너리에 정의
cdic = {
    '과자' : ['식품',1],
    '라면' : ['식품',2],
    '마스크' : ['위생용품',3],
    '맥주' : ['음료',4],
    '면도기' : ['위생용품',5],
    '생리대' : ['위생용품',6],
    '생수' : ['음료',7],
    '숙취해소제' : ['식품',8],
    '스타킹' : ['기타',9],
    '아이스크림' : ['식품',10],
    '우산' : ['기타',11],
    '탄산음료' : ['음료',12]
}

# 데이터베이스 연결
connect = pymysql.connect(host='localhost',user='root',password='0000',db='convenienceDB',charset='utf8')
cursor = connect.cursor()

# sales_history 테이블이 존재하면 삭제하는 SQL문 정의
dropSQL = "drop table if exists sales_history;"
cursor.execute(dropSQL)

# sales_history테이블을 생성하는 SQL문 정의
createSQL = '''create table sales_history(
            mcode tinyint unsigned,
            date date,
            code tinyint unsigned,
            category varchar(4),
            cname varchar(5) not null,
            sales_rate smallint unsigned
         )default charset=utf8;'''

# 정의해둔 생성 SQL문을 사용
cursor.execute(createSQL)
 
# data폴더 아래 Sales history.csv 파일 읽기
f = [
    open('data/_SalesHistory/Sales history.csv','r',encoding="utf-8"),
    ]

for i in range(len(f)):
    rdr = csv.reader(f[i])

    # 연산에 사용할 변수 초기화
    cnt = 1
    data = []
    category = ''
    code = 0

    # csv파일에 존재하는 데이터를 한줄씩 읽어 딕셔너리에 정의된 정보와 매칭시켜 리스트 형태로 하나씩 data리스트에 삽입
    for r in rdr:
        if cnt >1:
            data.append([r[1],cdic[r[2]][1],cdic[r[2]][0],r[2],int(r[3])])
        cnt+=1

    # 임시로 만들어둔 csv파일에 날짜가 2016년으로 되어있어 이를 2024년으로 바꿈
    for line in data:
        # 문자열은 내부 내용 변경이 불가능하므로 리스트로 바꾼뒤 내용을 변경하고, 이를 다시 문자열로 되돌림
        date = list(line[0])
        date[2] = '2'
        date[3] = '4'
        line[0] = (''.join(date))

        # sales_history테이블에 삽입할 데이터를 한줄씩 SQL문으로 정의
        insertSQL = f"insert into sales_history values({i+1},'{line[0]}',{line[1]},'{line[2]}','{line[3]}',{line[4]})"

        # sales_history테이블에 데이터 삽입 SQL문 사용
        cursor.execute(insertSQL)

    # 데이터베이스내 데이터 변경사항 적용
    connect.commit()

# 데이터베이스 연결 종료
connect.close()
cursor.close()