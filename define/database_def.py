###################################################
###################################################
######### 데이터베이스 관련 함수 정의 파일 #########
###################################################
###################################################

import pymysql
from define.init_def import getJSON, setJSON, getUserDataPath
import define.constant_data as const


# 데이터베이스 연결과 커서를 생성하는 함수
def dbConnectSetting():
    # 데이터베이스 연결
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='0000',
        db='convenienceDB',
        charset='utf8'
    )
    #커서 생성
    cursor = connection.cursor()
    return connection, cursor


# inventory 테이블 질의 함수
def getSelectSQL(mcode, category):
    connect, cursor = dbConnectSetting()

    # SQL 쿼리 실행
    if category=='':
        cursor.execute(f"SELECT code,category,cname,name,quantity,price FROM inventory WHERE mcode={mcode}")
    else:
        cursor.execute(f"SELECT code,category,cname,name,quantity,price FROM inventory WHERE mcode={mcode} and category='{category}'")

    rows = cursor.fetchall()

    # 데이터베이스 연결 종료
    cursor.close()
    connect.close()
    return rows


# inventory 테이블에서 모든 재고들의 카테고리, 상품 유형, 상품 명을 알려주는 함수
def getSelectAllSQL(mcode):
    connect, cursor = dbConnectSetting()

    # SQL 쿼리 실행
    cursor.execute(f"SELECT category, cname, name FROM inventory WHERE mcode={mcode}")

    rows = cursor.fetchall()

    # 데이터베이스 연결 종료
    cursor.close()
    connect.close()
    return rows


# today_sales_rate 테이블을 초기화하는 함수
def setTodaySalesRateTable(date):
    connect, cursor = dbConnectSetting()

    cursor.execute(f"UPDATE today_sales_rate SET sales_rate = 0, date = '{date}'")

    # 데이터베이스 데이터 변경 사항 적용
    connect.commit()

    cursor.close()
    connect.close()


# inventory 테이블에서 판매량만큼 재고를 차감하는 함수
def sellProduceFormInventory(items, nums, mcode):
    connect, cursor = dbConnectSetting()


    for i in range(len(items)):
        # SQL 쿼리 실행
        cursor.execute(f"SELECT name, quantity FROM inventory WHERE mcode={mcode}")
        rows = cursor.fetchall()

        for r in rows:
            if r[0] == items[i]:
                cursor.execute(f"UPDATE inventory SET quantity = {int(r[1])-int(nums[i])} WHERE name = '{items[i]}' and mcode={mcode}")

    # 데이터베이스 데이터 변경 사항 적용
    connect.commit()

    # 데이터베이스 연결 종료
    cursor.close()
    connect.close()


# 판매된 상품을 카테고리별로 today_sales_rate 테이블에 기록해두는 함수
def addTodaySalesRate(items, nums, mcode):
    connect, cursor = dbConnectSetting()


    for i in range(len(items)):
        # SQL 쿼리 실행
        cursor.execute(f"SELECT category, sales_rate FROM today_sales_rate WHERE mcode={mcode}")
        rows = cursor.fetchall()

        for r in rows:
            if r[0] == items[i]:
                # SQL 쿼리 실행
                cursor.execute(f"UPDATE today_sales_rate SET sales_rate = {int(r[1])+int(nums[i])} WHERE category = '{items[i]}' and mcode={mcode}")

    # 데이터베이스 데이터 변경 사항 적용
    connect.commit()

    # 데이터베이스 연결 종료
    cursor.close()
    connect.close()


# sales_history 테이블 질의
def getSalesSQL(mcode, date):
    connect, cursor = dbConnectSetting()

    # SQL 쿼리 실행
    cursor.execute(f"SELECT date,code,category,cname,sales_rate FROM sales_history WHERE date = '{date}' and mcode={mcode} order by code")

    rows = cursor.fetchall()

    # 데이터베이스 연결 종료
    cursor.close()
    connect.close()
    return rows


# 데이터를 받아 데이터베이스에 입력하고 그 결과를 반환하는 함수
def setSQL(texts, texts2, numbers, mcode):
    itemCategory = {
        "과자":"식품",
        "라면":"식품",
        "마스크":"위생용품",
        "맥주":"음료",
        "면도기":"위생용품",
        "생리대":"위생용품",
        "생수":"음료",
        "숙취해소제":"식품",
        "스타킹":"기타",
        "아이스크림":"식품",
        "우산":"기타",
        "탄산음료":"음료"
    }

    try:
        connection, cursor = dbConnectSetting()

        if texts and texts2 and numbers:
            try:
                # 데이터베이스에서 현재 데이터를 가져옴
                cursor.execute(f"SELECT 1 FROM inventory WHERE mcode={mcode}")
                rows = cursor.fetchall()
                cnt = len(rows)+1

                # 업데이트 작업
                for i in range(len(texts)):
                    cname = texts[i]
                    name = texts2[i]
                    number = int(numbers[i])

                    if name != '':
                        cursor.execute(f"SELECT quantity FROM inventory WHERE cname='{cname}' and name='{name}' and mcode={mcode}")
                        result = cursor.fetchone()

                        if result:
                            current_quantity = result[0]
                            new_quantity = current_quantity + number
                            cursor.execute(f"UPDATE inventory SET quantity = {new_quantity} WHERE name = '{name}' and mcode={mcode}")
                        else:
                            cursor.execute(f"INSERT INTO inventory VALUES ({cnt},{mcode},'{itemCategory[cname]}','{cname}', '{name}', {number}, 0)")
                            cnt+=1


                connection.commit()

                cursor.execute(f"SELECT code,category,cname,name,quantity,price FROM inventory WHERE mcode={mcode}")
                rows = cursor.fetchall()
                message = "good"

            # 예외 발생 시 abort 트랜잭션 처리
            except Exception as e:
                connection.rollback()
                message = f"오류가 발생했습니다: {str(e)}"
        else:
            message = "유효하지 않은 요청입니다."

    finally:
        # 데이터베이스 연결 종료
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        return message, rows
    

# 특정 상품을 삭제하는 함수
def deleteItem(code, name, mcode):
    connection, cursor = dbConnectSetting()
    length = 0
    
    try:
        if connection:
            cursor.execute(f"SELECT 1 FROM inventory WHERE mcode={mcode}")
            rows = cursor.fetchall()
            length = len(rows)

            cursor.execute(f"SELECT 1 FROM inventory WHERE code={code} and name='{name}' and mcode={mcode}")
            result = cursor.fetchall()
            if result:
                cursor.execute(f"DELETE FROM inventory WHERE code={code} and name='{name}' and mcode={mcode}")
                if code != length:
                    for i in range(code+1, length+1):
                        cursor.execute(f"UPDATE inventory SET code={i-1} WHERE code={i}")
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
    
    except:
        return False


# 데이터를 받아 재고 테이블에 입력하고 그 결과를 반환하는 함수
def setUpdateSQL(icList, qList, pList, mcode):
    try:
        connection, cursor = dbConnectSetting()

        if icList and qList and pList:
            try:
                # 업데이트 작업
                for i in range(len(icList)):
                    code = int(icList[i])
                    quantity = int(qList[i])
                    price = int(pList[i])

                    # 수량과 가격 정보를 데이터베이스에 반영시킴.
                    cursor.execute(f"UPDATE inventory SET quantity = {quantity} WHERE code = {code} and mcode={mcode}")
                    cursor.execute(f"UPDATE inventory SET price = {price} WHERE code = {code} and mcode={mcode}")


                connection.commit()

                cursor.execute(f"SELECT code,category,cname,name,quantity,price FROM inventory WHERE mcode={mcode}")
                rows = cursor.fetchall()
                message = "good"

            # 예외 발생 시 abort 트랜잭션 처리
            except Exception as e:
                connection.rollback()
                message = f"오류가 발생했습니다: {str(e)}"
        else:
            message = "유효하지 않은 요청입니다."

    finally:
        # 데이터베이스 연결 종료
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        return message, rows
    

# getSalesSQL() 함수를 개선한 함수. 질의 결과 중 없는 데이터를 판매량 0으로 추가해주는 코드
def getSalesFit(mcode, date): # 디폴트 값은 어제 날짜
    connect, cursor = dbConnectSetting()

    # SQL 쿼리 실행
    cursor.execute(f"SELECT date,code,category,cname,sales_rate FROM sales_history WHERE date = '{date}' and mcode={mcode} order by code")

    rows = cursor.fetchall()


    # tuple 타입으로 정의되어 있는 row의 내용을 변경하기 위해 일시적으로 list로 변경
    rows = list(rows)

    data = [
        (),
        (date,1,'식품','과자',0),
        (date,2,'식품','라면',0),
        (date,3,'위생용품','마스크',0),
        (date,4,'음료','맥주',0),
        (date,5,'위생용품','면도기',0),
        (date,6,'위생용품','생리대',0),
        (date,7,'음료','생수',0),
        (date,8,'식품','숙취해소제',0),
        (date,9,'기타','스타킹',0),
        (date,10,'식품','아이스크림',0),
        (date,11,'기타','우산',0),
        (date,12,'음료','탄산음료',0)
    ]

    newrows = []

    for i in range(len(rows)):
        rows[i] = list(rows[i])
        rows[i][0] = date
        rows[i] = tuple(rows[i])
        

    # 판매되지 않아 판매 목록에 없는 품목을 찾기
    for i in range(1,13):
        f=0
        for j in range(len(rows)):
            if rows[j][1]==i:
                f=1
        if(f==0):
            newrows.append(data[i])

    # 찾은 품목을 판매량 0으로 데이터에 포함(DB에 저장하지는 않음) 
    for i in newrows:
        rows.insert(i[1]-1,i)

    rows = tuple(rows)

    # 데이터베이스 연결 종료
    cursor.close()
    connect.close()

    return rows


# 모든 상품의 상품유형-카테고리 형태로 반환하는 함수
def getAllCategory(mcode):
    connect, cursor = dbConnectSetting()

    ProductTypeTocategory = {}

    categoryList = ['식품', '음료', '위생용품', '기타']
    for c in categoryList:
        cursor.execute(f"SELECT distinct cname FROM inventory WHERE category='{c}' and mcode={mcode} order by cname")
        rows = cursor.fetchall()
        cname = []
        for i in rows:
            cname.append(i[0])
        ProductTypeTocategory[c] = cname

    cursor.close()
    connect.close()

    return ProductTypeTocategory


# 모든 상품의 상품명을 카테고리명-[상품명] 형태로 반환하는 함수
def getAllProductName(categoryList, mcode):
    connect, cursor = dbConnectSetting()

    categoryToProductName = {}

    for c in categoryList:
        cursor.execute(f"SELECT distinct name FROM inventory WHERE cname='{c}' and mcode={mcode} order by name")
        rows = cursor.fetchall()
        cname = []
        for i in rows:
            cname.append(i[0])
        categoryToProductName[c] = cname

    cursor.close()
    connect.close()

    return categoryToProductName


# 상품의 카테고리를 반환하는 함수
def getCategory(name, mcode):
    connect, cursor = dbConnectSetting()
    cursor.execute(f"SELECT distinct cname FROM inventory WHERE name='{name}' and mcode={mcode}")
    rows = cursor.fetchall()
    cursor.close()
    connect.close()

    if rows:
        return rows[0][0]
    else:
        return ''

# 해당 상품의 수량을 반환하는 함수
def getQuantity(name, mcode):
    connect, cursor = dbConnectSetting()
    cursor.execute(f"SELECT quantity FROM inventory WHERE name='{name}' and mcode={mcode}")
    rows = cursor.fetchall()
    cursor.close()
    connect.close()
    return int(rows[0][0])

# 모든 상품의 가격을 상품-가격 형태로 반환하는 함수
def getAllNameAndPrice(mcode):
    connect, cursor = dbConnectSetting()

    productNameToPrice = {}

    cursor.execute(f"SELECT distinct name, code, price FROM inventory WHERE mcode={mcode} order by price")
    rows = cursor.fetchall()

    cursor.close()
    connect.close()

    for row in rows:
        productNameToPrice[row[0]] = [row[1], int(row[2])]

    return productNameToPrice


# inventory 테이블에서 입력 카테고리에 해당하는 재고가 몇개 있는지 반환하는 함수
def getInventoryQuantity(mcode):
    connect, cursor = dbConnectSetting()

    # SQL 쿼리 실행
    cursor.execute(f"SELECT cname, quantity FROM inventory WHERE mcode={mcode}")

    rows = cursor.fetchall()

    # 데이터베이스 연결 종료
    cursor.close()
    connect.close()

    data = getJSON(const.jsonDatapath)

    for key in const.categoryKoreanName.keys():
        data["inventoryQuantity"][key] = 0

    for i in range(len(rows)):
        for key in const.categoryKoreanName.keys():
            if const.categoryKoreanName[key] == rows[i][0]:
                data["inventoryQuantity"][key] += rows[i][1]

    setJSON(data, const.jsonDatapath)


# 어제 날짜의 각 카테고리 판매량들을 읽어 yesterdaySalesRate 딕셔너리에 값들을 저장하는 함수
def setYesterdaySalesRate(mcode, formatted_yesterday, categoryCode):
    connect, cursor = dbConnectSetting()

    # SQL 쿼리 실행
    cursor.execute(f"SELECT code, sales_rate FROM sales_history WHERE date='{formatted_yesterday}' and mcode={mcode} order by code")

    rows = cursor.fetchall()

    # 데이터베이스 연결 종료
    cursor.close()
    connect.close()

    data = getJSON(getUserDataPath(mcode))
    for i in range(len(rows)):
        data["yesterdaySalesRate"][categoryCode[rows[i][0]]] = rows[i][1]
    setJSON(data, getUserDataPath(mcode))


# 해당 상품의 가격 정보를 가져오는 함수
def getPriceSQL(itemName, mcode):
    connect, cursor = dbConnectSetting()

    # SQL 쿼리 실행
    cursor.execute(f"SELECT price FROM inventory WHERE name='{itemName}' and mcode={mcode}")

    rows = cursor.fetchall()

    # 데이터베이스 연결 종료
    cursor.close()
    connect.close()
    
    return int(rows[0][0])


# today_sales_rate 테이블에 있는 데이터를 질의해서 반환하는 함수
def getTodaySalesRate(mcode):
    connect, cursor = dbConnectSetting()

    # SQL 쿼리 실행
    cursor.execute(f"SELECT category, sales_rate FROM today_sales_rate WHERE mcode={mcode}")

    rows = cursor.fetchall()

    # 데이터베이스 연결 종료
    cursor.close()
    connect.close()
    
    return rows


# sales_history 테이블의 오늘 날짜 데이터와 today_sales_rate 테이블의 데이터를 받아 더해 반환하는 함수
def getAddTodaySales(rows1, rows2):
    addData = list()
    for row1 in rows1:
        addData.append(list(row1))

    for row2 in rows2:
        for addRow1 in addData:
            if row2[0]==addRow1[3]:
                addRow1[4]=int(row2[1])+int(addRow1[4])
    return addData


# 아이디를 입력받아 해당 아이디가 이미 존재하는지 알려주는 함수
def idCheck(id):
    connect, cursor = dbConnectSetting()

    if connect:
        # SQL 쿼리 실행
        cursor.execute(f"SELECT mid FROM member")
        rows = cursor.fetchall()

    # 데이터베이스 연결 종료
    cursor.close()
    connect.close()

    idList=[]
    for row in rows:
        for i in row:
            if i != '':
                idList.append(i)

    if id in idList:
        return True
    else:
        return False
        
    

# 닉네임을 입력받아 해당 닉네임이 이미 존재하는지 알려주는 함수
def nicknameCheck(name):
    connect, cursor = dbConnectSetting()

    if connect:
        # SQL 쿼리 실행
        cursor.execute(f"SELECT mname FROM member")
        rows = cursor.fetchall()

    # 데이터베이스 연결 종료
    cursor.close()
    connect.close()

    nnList=[]
    for row in rows:
        for nn in row:
            if nn != '':
                nnList.append(nn)

    if name in nnList:
        return True
    else:
        return False
        
    
# 지점명을 입력받아 해당 지점이 이미 존재하는지 알려주는 함수
def placeCheck(place):
    connect, cursor = dbConnectSetting()

    if connect:
        # SQL 쿼리 실행
        cursor.execute(f"SELECT pname FROM member")
        rows = cursor.fetchall()

    # 데이터베이스 연결 종료
    cursor.close()
    connect.close()

    pList=[]
    for row in rows:
        for p in row:
            if p != '':
                pList.append(p)

    if place in pList:
        return True
    else:
        return False
    

# 새 계정의 회원정보를 member 테이블에 생성하는 함수
def createNewUserData(connect, cursor, id, pw, name, place):
    if connect:
        cursor.execute(f"SELECT mcode FROM member")
        rows = cursor.fetchall()

        cursor.execute(f"INSERT INTO member VALUES(1,{len(rows)},'{id}','{pw}','{name}','{place}')")


# 새 계정의 오늘 판매량 정보를 TSR 테이블에 생성하는 함수
def createNewUserTSR(connect, cursor):
    if connect:

        cursor.execute(f"SELECT distinct mcode FROM today_sales_rate WHERE mcode>0")
        rows = cursor.fetchall()
        length = len(rows)+1

        insertSQL = [
            f"INSERT INTO today_sales_rate VALUES({length}, '{const.todayFormattedDate}', '라면', 0)",
            f"INSERT INTO today_sales_rate VALUES({length}, '{const.todayFormattedDate}', '과자', 0)",
            f"INSERT INTO today_sales_rate VALUES({length}, '{const.todayFormattedDate}', '마스크', 0)",
            f"INSERT INTO today_sales_rate VALUES({length}, '{const.todayFormattedDate}', '면도기', 0)",
            f"INSERT INTO today_sales_rate VALUES({length}, '{const.todayFormattedDate}', '맥주', 0)",
            f"INSERT INTO today_sales_rate VALUES({length}, '{const.todayFormattedDate}', '생리대', 0)",
            f"INSERT INTO today_sales_rate VALUES({length}, '{const.todayFormattedDate}', '생수', 0)",
            f"INSERT INTO today_sales_rate VALUES({length}, '{const.todayFormattedDate}', '숙취해소제', 0)",
            f"INSERT INTO today_sales_rate VALUES({length}, '{const.todayFormattedDate}', '스타킹', 0)",
            f"INSERT INTO today_sales_rate VALUES({length}, '{const.todayFormattedDate}', '우산', 0)",
            f"INSERT INTO today_sales_rate VALUES({length}, '{const.todayFormattedDate}', '아이스크림', 0)",
            f"INSERT INTO today_sales_rate VALUES({length}, '{const.todayFormattedDate}', '탄산음료', 0)"
        ]

        for sql in insertSQL:
            cursor.execute(sql)


# 새 사용자 정보를 데이터베이스에 등록하는 함수
def createNewUserAccount(id,pw,name,place):
    try:
        connect, cursor = dbConnectSetting()
        createNewUserTSR(connect, cursor)
        createNewUserData(connect, cursor, id, pw, name, place)
        
        connect.commit()
        # 데이터베이스 연결 종료
        cursor.close()
        connect.close()
        return True

    except:
        return False


# 아이디와 비밀번호가 매칭되는지 알려주는 함수
def loginCheck(id,pw):
    connect, cursor = dbConnectSetting()

    result = False

    try:
        if connect:
            cursor.execute(f"SELECT mpw FROM member WHERE mid='{id}'")
            rows = cursor.fetchall()

            if pw == rows[0][0]:
                result = True
        
        # 데이터베이스 연결 종료
        cursor.close()
        connect.close()

    except:
        return False

    return result


# 아이디와 비밀번호를 통해 유저코드, 닉네임, 지점명을 반환하는 함수
def getUserInfo(id,pw):
    connect, cursor = dbConnectSetting()

    if connect:
        cursor.execute(f"SELECT mcode,mname,pname FROM member WHERE mid='{id}' and mpw='{pw}'")
        rows = cursor.fetchall()

    # 데이터베이스 연결 종료
    cursor.close()
    connect.close()

    return rows[0]


# 지점명을 통해 코드를 알아내는 함수
def getMcode(place):
    connect, cursor = dbConnectSetting()

    if connect:
        cursor.execute(f"SELECT mcode FROM member WHERE pname='{place}'")
        rows = cursor.fetchall()

    # 데이터베이스 연결 종료
    cursor.close()
    connect.close()
    return int(rows[0][0])

    
# 회원가입되어있는 모든 지점의 지점명을 조회하는 함수
def getAllPlace():
    connect, cursor = dbConnectSetting()

    if connect:
        cursor.execute(f"SELECT pname FROM member")
        rows = cursor.fetchall()

    # 데이터베이스 연결 종료
    cursor.close()
    connect.close()

    pList=[]
    for row in rows:
        for p in row:
            if p != '':
                pList.append(p)
    
    return pList


# 각 카테고리별 총 재고 수량을 조회하는 함수
def getSumOfCategoryQuantity(mcode):
    connect, cursor = dbConnectSetting()

    if connect:
        cursor.execute(f"SELECT cname, sum(quantity) FROM inventory WHERE mcode={mcode} group by cname")
        rows = cursor.fetchall()
    
    # 데이터베이스 연결 종료
    cursor.close()
    connect.close()

    rows = list(rows)
    rowDict = {}
    for row in rows:
        row = list(row)
        rowDict[row[0]] = int(row[1])

    return rowDict


# 아이디와 유저코드를 통해 해당 회원 정보와 관련 테이블의 정보를 삭제하는 함수
def deleteMember(id, mcode):
    connect, cursor = dbConnectSetting()
    memberCount = 0

    if mcode == 0:
        return False

    if connect:
        cursor.execute(f"SELECT mid FROM member")
        rows = cursor.fetchall()
        memberCount = len(rows)
        
        cursor.execute(f"SELECT 1 FROM member WHERE mcode={mcode} and mid='{id}'")
        rows = cursor.fetchall()

    if rows:
        if deleteMemberInfo(connect, cursor, mcode, memberCount):
            if deleteMemberTSR(connect, cursor, mcode, memberCount):
                if deleteMemberInventory(connect, cursor, mcode, memberCount):
                    if deleteMemberSH(connect, cursor, mcode, memberCount):
                        # 데이터베이스 변경사항 저장
                        connect.commit()
                        # 데이터베이스 연결 종료
                        cursor.close()
                        connect.close()
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

# member 테이블에서 해당 회원의 데이터 행을 삭제하는 함수
def deleteMemberInfo(connect, cursor, mcode, memberCount):
    if connect:
        cursor.execute(f"DELETE FROM member WHERE mcode={mcode}")
        for i in range(mcode+1, memberCount):
            cursor.execute(f"UPDATE member SET mcode={i-1} WHERE mcode={i}")
        return True


# today_sales_rate 테이블에서 해당 회원의 데이터 행을 삭제하는 함수
def deleteMemberTSR(connect, cursor, mcode, memberCount):
    if connect:
        try:
            cursor.execute(f"DELETE FROM today_sales_rate WHERE mcode={mcode}")
            for i in range(mcode+1, memberCount):
                cursor.execute(f"UPDATE today_sales_rate SET mcode={i-1} WHERE mcode={i}")
            return True
        except:
            return False


# inventory 테이블에서 해당 회원의 데이터 행을 삭제하는 함수
def deleteMemberInventory(connect, cursor, mcode, memberCount):
    if connect:
        try:
            cursor.execute(f"DELETE FROM inventory WHERE mcode={mcode}")
            for i in range(mcode+1, memberCount):
                cursor.execute(f"UPDATE inventory SET mcode={i-1} WHERE mcode={i}")
            return True
        except:
            return False


# sales_history 테이블에서 해당 회원의 데이터 행을 삭제하는 함수
def deleteMemberSH(connect, cursor, mcode, memberCount):
    if connect:
        try:
            cursor.execute(f"DELETE FROM sales_history WHERE mcode={mcode}")
            for i in range(mcode+1, memberCount):
                cursor.execute(f"UPDATE sales_history SET mcode={i-1} WHERE mcode={i}")
            return True
        except:
            return False


# 회원정보를 출력하는 함수
def getAllMember():
    connect, cursor = dbConnectSetting()

    if connect:
        cursor.execute("SELECT authority, mcode, mid, mname, pname FROM member")
        rows = cursor.fetchall()

    # 데이터베이스 연결 종료
    cursor.close()
    connect.close()
    return rows