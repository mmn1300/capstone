from flask import Flask, render_template, request , url_for, jsonify, Response, send_file, session
import sub
import subprocess
import os
from math import ceil
import web_cam.POS as p
from flask_session import Session

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = '/tmp/flask_session'
app.config['SESSION_FILE_THRESHOLD'] = 100  # 최대 파일 수 (옵션)
app.config['SESSION_USE_SIGNER'] = True  # 세션 데이터 서명 (옵션)
app.secret_key = 'aaaaaaaaaaaa'
Session(app)  # Flask-Session 초기화


# 서버 시작시 사용할 변수 파일 및 테이블, 각 모델 예측값 파일을 초기화
sub.variablesInit()
sub.setTodaySalesRateTable()
sub.setTodayWeather()
for text_file_path in list(sub.categoryForecastingResultPath.values()):
    if os.path.exists(text_file_path):
        with open(text_file_path, "w") as file:
            file.write("0\n0\n0\n0\n0\n0\n0")


# 생성되어있던 발주서 전부 제거
target_directory = 'purchase_order'
if os.path.exists(target_directory):
        for filename in os.listdir(target_directory):
            file_path = os.path.join(target_directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"파일 삭제 중 오류 발생: {e}")


# 시작화면
@app.route('/')
def index():
    if session.get('user_place'):
        session.pop('user_place', None)
    if session.get('IP-URL'):
        session.pop('IP-URL', None)
    username = session.get('username')
    place = session.get('place')
    return render_template('index_page.html', username=username or '', place=place or '')


# 시작화면 -> 지점 선택
@app.route('/place')
def select_place():
    return render_template('place_select.html', placeList=sub.getAllPlace())


@app.route('/create_user_session', methods=['POST'])
def create_user_session():
    data = request.get_json()
    place = data.get('place')
    IPtoURL = data.get('IP-URL')
    session['user_place'] = place
    session['IP-URL'] = IPtoURL
    return jsonify({"message" : True})



# 시작화면 -> 지점선택 -> 판매 메뉴
@app.route('/user_page')
def user_page():
    return render_template('user_page.html')


# 시작화면 -> 판매 메뉴 -> 홈
@app.route('/user_page/logout')
def user_logout():
    session.pop('user_place', None)
    session.pop('IP-URL', None)
    username = session.get('username')
    place = session.get('place')
    return render_template('index_page.html', username=username or '', place=place or '')


# 시작화면 -> 판매 메뉴 -> 관리자
@app.route('/user_page/admin_page')
def user_admin_page():
    session.pop('user_place', None)
    session.pop('IP-URL', None)
    username = session.get('username')
    place = session.get('place')
    if(username == '최고관리자'):
        return render_template('member_management.html')
    elif(username):
        return render_template('admin_page.html', username=username, place=place)
    else:
        return render_template('login_form.html')
    

# 시작화면 -> 판매 메뉴(상품 결제 처리)
@app.route('/user_page/payment', methods=['PUT'])
def payment_page():
    data = request.get_json()

    placeInfo = session.get('user_place')
    textArray = data.get('texts', [])
    numberArray = data.get('numbers', [])
    categoryArray = []

    
    # POS.py의 classKoreanName 딕셔너리에서 값을 통해 키를 알아내는 코드. 얻은 키는 상품 형태로 변환
    for item in textArray:
        for key, value in p.classKoreanName.items():
            if item == value:
                categoryArray.append(p.category[key])
                break

    mcode = sub.getMcode(placeInfo)
    sub.sellProduceFormInventory(textArray,numberArray,mcode)
    sub.addTodaySalesRate(categoryArray,numberArray,mcode)

    return jsonify({'result': 'good'})


@app.route('/video_feed')
def video_feed():
    return Response(p.generate_frames(sub.getDroidCamURL(session.get('IP-URL'))), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture_image', methods=['POST'])
def capture_image():
    if p.current_frame is not None:
        # 이미지 예측
        predicted_class = p.predict_image(p.current_frame)
        koreanName = p.classKoreanName[predicted_class]
        return jsonify({
            'itemName': koreanName,
            'category' : p.category[predicted_class],
            'price' : sub.getPriceSQL(koreanName, sub.getMcode(session.get('user_place'))),
            'imagePath' : p.itemImagePath[koreanName]
            })
    return jsonify({'result': 'No image captured'})


# 시작화면 -> 관리자 메뉴
@app.route('/admin_page')
def admin_page():
    username = session.get('username')
    place = session.get('place')
    if(username == '최고관리자'):
        rows = sub.getAllMember()
        return render_template('member_management.html', rows=rows)
    elif(username):
        return render_template('admin_page.html', username=username, place=place)
    else:
        return render_template('login_form.html')


# 시작화면 -> 최고 관리자 메뉴 -> 회원 삭제
@app.route('/member/delete', methods=['DELETE'])
def member_delete():
    data = request.get_json()
    id = data.get('id')
    mcode = data.get('code')
    result = sub.deleteMember(id, mcode)
    return jsonify({'result': result})


# 시작화면 -> 관리자 메뉴 -> 재고 물품 등록 및 정보
@app.route('/admin_page/inventory_info')
def inventory_info():
    data = sub.getJSON(sub.jsonDatapath)
    start_line = sub.getDateCount(sub.todayFormattedDate)
    for key, path in sub.categoryForecastingResultPath.items():
        SumOfThreePredictedSales = 0
        SumOfSevenPredictedSales = 0
        with open(path, 'r') as file:
            lines = file.readlines()
            end_line = start_line + 6
            predictData = lines[start_line - 1:end_line]
            predictData = [float(item.strip()) for item in predictData if item.strip().replace('.', '', 1).isdigit()]
        
        for i in range(len(predictData)):
            if isinstance(predictData[i], str):  # 문자열인지 확인
                if i < 3:
                    SumOfThreePredictedSales += float(predictData[i].strip())
                SumOfSevenPredictedSales += float(predictData[i].strip())
            else:
                if i < 3:
                    SumOfThreePredictedSales += predictData[i]
                SumOfSevenPredictedSales += predictData[i]
        data["threeDaysPredictedSales"][key] = round(SumOfThreePredictedSales, 2)
        data["sevenDaysPredictedSales"][key] = round(SumOfSevenPredictedSales, 2)
    
    sub.setJSON(data, sub.jsonDatapath)

    return render_template('inventory_info.html', username=session.get('username'), place=session.get('place'))


# 시작화면 -> 관리자 메뉴 -> 판매 내역
@app.route('/admin_page/sales_history')
def sales_history():
    mcode = session.get('mcode')
    # sales_history테이블에 존재하는 오늘 날짜의 데이터를 받아옴. 없는 항목은 판매량 0으로 받아옴. 판매된 수량 더함
    rows = sub.getAddTodaySales(sub.getSalesFit(mcode), sub.getTodaySalesRate(mcode))
    #오늘의 날씨 정보를 받음
    data = sub.getJSON(sub.jsonDatapath)
    weatherInfo = data["todayWeatherInfo"]
    return render_template('sales_history.html', rows=rows, place=session.get('place'), weatherInfo=weatherInfo)


# 시작화면 -> 관리자 메뉴 -> 판매 내역(날짜 별)
@app.route('/admin_page/sales_history/select_date', methods=["GET"])
def day_sales_history():
    date = request.args.get('date', type=str)
    # sales_history테이블에 존재하는 date일자의 데이터를 받아옴. 없는 항목은 판매량 0으로 받아옴
    rows=()
    mcode = session.get('mcode')
    if date == sub.todayFormattedDate:
        rows = sub.getAddTodaySales(sub.getSalesFit(mcode), sub.getTodaySalesRate(mcode))
    else:
        rows = sub.getSalesFit(mcode, date)

    return jsonify(rows)


# 시작화면 -> 관리자 메뉴 -> 재고 물품 등록 및 정보 -> 재고 등록
@app.route('/admin_page/inventory_info/inventory_warehousing')
def inventory_warehousing():
    rows = sub.getSelectAllSQL(session.get('mcode'))
    return render_template('inventory_warehousing.html', rows=rows)


# 시작화면 -> 관리자 메뉴 -> 재고 물품 등록 및 정보 -> 재고 등록 -> DB 재고 등록(백엔드 처리)
@app.route('/admin_page/inventory_info/inventory_warehousing/db_insert', methods=['POST'])
def db_insert():
    message = "에러가 발생했습니다."

    # inventory_warehousing.html에서 POST방식으로 넘어온 데이터
    texts = request.form.getlist('texts')
    texts2 = request.form.getlist('texts2')
    numbers = request.form.getlist('numbers')
    
    # 데이터를 받아 데이터베이스에 입력하고 입력 후 결과를 받음
    message, rows = sub.setSQL(texts, texts2, numbers, session.get('mcode'))

    # 정상, 비정상 실행시에 따른 렌더링
    if message == 'good':
        sumOfThreeDaysPredictSales = {sub.categoryKoreanName[key]: data["threeDaysPredictedSales"][key] for key in data["threeDaysPredictedSales"]}
        sumOfSevenDaysPredictSales = {sub.categoryKoreanName[key]: data["sevenDaysPredictedSales"][key] for key in data["sevenDaysPredictedSales"]}
        data = sub.getJSON(sub.jsonDatapath)
        return render_template('query_result.html',
                        rows=rows,
                        category='all',
                        sumOfCategoryQuantity = sub.getSumOfCategoryQuantity(session.get('mcode')),
                        sumOfThreeDaysPredictSales=sumOfThreeDaysPredictSales,
                        sumOfSevenDaysPredictSales=sumOfSevenDaysPredictSales)
    else:
        return render_template('result.html', message=message, error="유효하지 않은 요청")


# 시작화면 -> 관리자 메뉴 -> 재고 물품 등록 및 정보 -> 재고 정보 출력
@app.route('/admin_page/inventory_info/products')
def db_query_category():
    category = request.args.get('category', type=str)
    if category != 'all':
        rows = sub.getSelectSQL(session.get('mcode'), sub.productTypeKorenName[category])
    else:
        rows = sub.getSelectSQL(session.get('mcode'))
    data = sub.getJSON(sub.jsonDatapath)
    sumOfThreeDaysPredictSales = {sub.categoryKoreanName[key]: data["threeDaysPredictedSales"][key] for key in data["threeDaysPredictedSales"]}
    sumOfSevenDaysPredictSales = {sub.categoryKoreanName[key]: data["sevenDaysPredictedSales"][key] for key in data["sevenDaysPredictedSales"]}
    return render_template('query_result.html',
                           rows=rows,
                           category=category,
                           sumOfCategoryQuantity = sub.getSumOfCategoryQuantity(session.get('mcode')),
                           sumOfThreeDaysPredictSales=sumOfThreeDaysPredictSales,
                           sumOfSevenDaysPredictSales=sumOfSevenDaysPredictSales)


# 시작화면 -> 관리자 메뉴 -> 재고 물품 등록 및 정보 -> 재고 정보 출력 -> 재고량, 가격 변경(백엔드 처리)
@app.route('/admin_page/inventory_info_update', methods=['PUT'])
def inventory_info_update():
    try:
        data = request.get_json()
        itemCodeArray = data.get('productCodes')
        quantityArray = data.get('quantitys')
        priceArray = data.get('prices')

        sub.setUpdateSQL(itemCodeArray, quantityArray, priceArray, session.get('mcode'))
        data = sub.getJSON(sub.jsonDatapath)
        return jsonify({"data" : "good"})

    except Exception as e:
        return jsonify({"error" : str(e)}), 500
    

# 시작화면 -> 관리자 페이지 -> 재고 물품 등록 및 정보 -> 재고 정보 출력 -> 상품 삭제
@app.route('/admin_page/product/delete', methods=['DELETE'])
def inventory_item_delete():
    try:
        data = request.get_json()
        itemCode = int(data.get('code'))
        itemName = data.get('name')
        result = sub.deleteItem(itemCode, itemName, session.get('mcode'))
        return jsonify({"result" : result})

    except Exception as e:
        return jsonify({"result" : False, "error" : str(e)})
    

# 시작화면 -> 관리자 메뉴 -> 수요 예측전 모델 동작에 필요한 것들을 셋팅
@app.route('/admin_page/predict_model_load')
def predict_model_load():
    sub.setYesterdaySalesRate(session.get('mcode'))
    data = sub.getJSON(sub.jsonDatapath)
    if data["weatherLoad"] == True:
        sub.setModelInputData()
        returnData = sub.setweatherInfo()
        if returnData is not None:
            return render_template('result.html', message="모델을 불러오는 도중 에러가 발생했습니다.", error=returnData)
        
        data["weatherLoad"] = False
        sub.setJSON(data, sub.jsonDatapath)

    # 아래 코드는 시간 단위마다 데이터가 갱신되므로 일회성 동작 처리 불가
    returnData = sub.getTodayWeatherData()
    if returnData is not None:
            return render_template('result.html', message="모델을 불러오는 도중 에러가 발생했습니다.", error=returnData)
    
    return render_template('predict_model_load.html')


# 시작화면 -> 관리자 메뉴 -> 수요 예측 -> 카테고리별 수요 예측
@app.route('/admin_page/demand_forecasting')
def forecasting():
    category = request.args.get('category', type=str)
    def run_script_and_get_output(script_name):
        # subprocess.run()을 사용하여 다른 스크립트를 실행하고 결과를 받아옴
        result = subprocess.run(
            ['python', script_name],  # 실행할 명령어
            capture_output=True,      # 표준 출력과 표준 오류를 캡처
            text=True                 # 출력 결과를 텍스트로 처리
        )
        return result.stdout
    
    sub.getInventoryQuantity(session.get('mcode'))
    data = sub.getJSON(sub.jsonDatapath)
    userData = sub.getJSON(sub.getUserDataPath(session.get('mcode')))

    # gru_model폴더 밑에 있는 예측모델을 실행함.
    if data["categoryGruModelOperationStatus"][category]:
        run_script_and_get_output(sub.categoryModelPath[category])
        data["categoryGruModelOperationStatus"][category] = False
        sub.setJSON(data, sub.jsonDatapath)

    weatherData=[]
    
    with open(r'data\_weather_info\today_weather_data.txt', 'r', encoding='utf-8') as file:
        for l in file:
            if l == 'Measured Unavailable':
                weatherData.append('측정되지 않음')
            else:
                weatherData.append(float(l))
    
    start_line = sub.getDateCount(sub.todayFormattedDate)
    with open(sub.categoryForecastingResultPath[category], 'r') as file:
        # 파일의 모든 행을 읽음
        lines = file.readlines()
        
        # 특정 행부터 7번째 행까지 읽어옴
        end_line = start_line + 7
        predictData = lines[start_line - 1:end_line]
        predictData = [float(item.strip()) for item in predictData if item.strip().replace('.', '', 1).isdigit()]

    return render_template('predict_result.html',
                           categoryName=category,
                           categoryQuantity=data["inventoryQuantity"][category],
                           imgPath=sub.categoryImagePath[category],
                           weatherTextData=data["todayWeatherInfo"],
                           weatherNumberData=weatherData,
                           yesterdaySalesRate=userData["yesterdaySalesRate"][category],
                           predictData=predictData
                           )


# 시작화면 -> 관리자 페이지 -> 수요 예측 -> 카테고리별 수요 예측 -> 특정 날짜 수요예측
@app.route('/admin_page/demand_forecasting/date', methods=['GET'])
def date_demand_predict():
    category = request.args.get('category', type=str)
    date = request.args.get('date', type=str)
    start_line = sub.getDateCount(date)
    with open(sub.categoryForecastingResultPath[category], 'r') as file:
        # 파일의 모든 행을 읽음
        lines = file.readlines()
        
        # 특정 행부터 8번째 행까지 읽어옴
        end_line = start_line + 7
        predictData = lines[start_line - 1:end_line]
        predictData = [float(item.strip()) for item in predictData if item.strip().replace('.', '', 1).isdigit()]
        weatherData = sub.getPastWeather(date)

    return jsonify({
        "newPredictData" : predictData,
        "weatherData": weatherData})


# 시작화면 -> 관리자 메뉴 -> 발주서 작성
@app.route('/admin_page/order_page')
def order_page():
    categoryList = sub.getAllCategory(session.get('mcode'))
    cl = []
    for pt in categoryList.values():
        for c in pt:
            cl.append(c)
    return render_template('order_page.html',
                           productTypeToCategory=categoryList,
                           categoryToProductName=sub.getAllProductName(cl, session.get('mcode')),
                           productNameToCodeAndPrice=sub.getAllNameAndPrice(session.get('mcode')),
                           place = session.get('place')
                           )


# 시작화면 -> 관리자 메뉴 -> 발주서 작성 -> AI 추천
@app.route('/admin_page/order_page/predict', methods=['POST'])
def ai_recommendation():
    mcode = session.get('mcode')
    data = request.get_json()
    day = int(data.get('day'))
    items = data.get('items', [])

    key_dict = dict.fromkeys(sub.categoryForecastingResultPath.keys(), 0)
    start_line = sub.getDateCount(sub.todayFormattedDate)
    for category, modelResultPath in sub.categoryForecastingResultPath.items():
        with open(modelResultPath, 'r') as file:
            lines = file.readlines()
            cnt=1
            end_line = start_line + 6
            predictData = lines[start_line - 1:end_line]
            predictData = [float(item.strip()) for item in predictData if item.strip().replace('.', '', 1).isdigit()]
            for data in predictData:
                if cnt<=day:
                    key_dict[category] += float(data)
                cnt+=1

    for k, v in key_dict.items():
        key_dict[k] = ceil(v)
    
    categoryKoreanNameDict = {}
    for category, data in key_dict.items():
        categoryKoreanNameDict[sub.categoryKoreanName[category]] = data

    quantityOfCategory = sub.getSumOfCategoryQuantity(mcode)
    requireQuantity = {}
    for key, value in categoryKoreanNameDict.items():
        for k, v in quantityOfCategory.items():
            if key == k:
                if (value - v)>0:
                    requireQuantity[key] = value - v
                else:
                    requireQuantity[key] = 0

    key_array = list(sub.categoryForecastingResultPath.keys())
    new_dict_name = {sub.categoryKoreanName[key]: [] for key in key_array}
    for item in items:
        category = sub.getCategory(item, mcode)
        if category in list(new_dict_name.keys()):
            new_dict_name[category].append(item)

    new_dict = {sub.categoryKoreanName[key]: [] for key in key_array}
    for item in items:
        category = sub.getCategory(item, mcode)
        if category in list(new_dict.keys()):
            new_dict[category].append(sub.getQuantity(item, mcode))

    distributedQuantityDict = {}
    for key, value in new_dict.items():
        dql = sub.getDistributedQuantity(value, requireQuantity[key])
        for innerKey, innerValue in new_dict_name.items():
            if key == innerKey:
                for i in range(len(innerValue)):
                    distributedQuantityDict[innerValue[i]] = dql[i]

    return jsonify({
        "distributedQuantityDict" : distributedQuantityDict
    })



# 시작화면 -> 관리자 메뉴 -> 발주서 작성 -> 발주서 생성
@app.route('/admin_page/order_page/create_xlsx', methods=["POST"])
def create_xlsx():
    orderInfoList = request.form.getlist('info')
    orderDataList = request.form.getlist('item_info')
    remarkString = request.form.get('remark')

    fileName = sub.createXlsx(orderInfoList, orderDataList, remarkString)
    return render_template('xlsx_download.html', fileName=fileName)


# 시작화면 -> 관리자 메뉴 -> 발주서 작성 -> 발주서 다운로드
@app.route('/admin_page/order_page/create_xlsx/download/<string:fileName>', methods=['GET'])
def download_file(fileName):
    file_path = 'purchase_order/'+fileName  # 서버의 파일 경로

    try:
        return send_file(
            file_path,
            mimetype='text/xlsx',
            as_attachment=True,
            download_name=fileName
        )
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
        

# 로그인 페이지
@app.route('/login_form')
def login_form():
    return render_template('login_form.html')

# 로그인 아이디 확인
@app.route('/login/id', methods=['POST'])
def login_id():
    data = request.get_json()
    id = data.get('id')

    if(sub.idCheck(id)):
        return jsonify({"message": 'exists'})
    else:
        return jsonify({"message": 'not exists'})

# 로그인 비밀번호 확인
@app.route('/login/pw', methods=['POST'])
def login_pw():
    data = request.get_json()
    id = data.get('id')
    pw = data.get('pw')

    if(sub.loginCheck(id,pw)):
        return jsonify({"message": 'exists'})
    else:
        return jsonify({"message": 'not exists'})


# 로그인 (세션 생성, 사용자 데이터 파일 생성)
@app.route('/login', methods=['POST'])
def login():
    id = request.form.get('id')
    pw = request.form.get('pw')

    mcode,nickname,place = sub.getUserInfo(id,pw)
    session['mcode'] = mcode
    session['username'] = nickname
    session['place'] = place


    if nickname=='최고관리자':
        rows = sub.getAllMember()
        return render_template('member_management.html', rows=rows)
    else:
        sub.userVariablesInit(mcode)
        return render_template('admin_page.html', username=nickname, place=place)


# 로그아웃 (세션 삭제, 사용자 데이터 파일 삭제)
@app.route('/logout')
def logout():
    mcode = session.get('mcode')
    session.pop('mcode', None)
    session.pop('username', None)
    session.pop('place', None)
    sub.deleteJSON(sub.getUserDataPath(mcode))
    return render_template('index_page.html', username='', place='')


# 회원가입 페이지
@app.route('/account_form')
def account_form():
    return render_template('create_account.html')

# 회원가입 -> 아이디 체크 (입력한 아이디가 이미 존재하는지 확인)
@app.route('/account/id', methods=['POST'])
def account_id():
    data = request.get_json()
    id = data.get('id')

    if(sub.idCheck(id)==False):
        return jsonify({"idCheck": True})
    else:
        return jsonify({"idCheck": False})
        
# 회원가입 -> 닉네임 체크 (입력한 닉네임이 이미 존재하는지 확인)
@app.route('/account/nickname', methods=['POST'])
def account_name():
    data = request.get_json()
    nickname = data.get('nickname')

    if(sub.nicknameCheck(nickname)==False):
        return jsonify({"nicknameCheck": True})
    else:
        return jsonify({"nicknameCheck": False})

# 회원가입 -> 지점명 체크 (입력한 지점의 계정이 이미 존재하는지 확인)
@app.route('/account/place', methods=['POST'])
def account_place():
    data = request.get_json()
    place = data.get('place')

    if(sub.placeCheck(place)==False):
        return jsonify({"placeCheck": True})
    else:
        return jsonify({"placeCheck": False})

# 회원가입 -> 승인 코드 체크 (입력한 승인 코드가 일치하는지 확인)
@app.route('/account/code', methods=['POST'])
def account_code():
    data = request.get_json()
    code = data.get('code')

    if(sub.approvalCode==int(code)):
        return jsonify({"codeCheck": True})
    else:
        return jsonify({"codeCheck": False})

# 회원가입 (새 계정 생성 및 데이터베이스 등록)
@app.route('/account/create', methods=['POST'])
def create_account():
    data = request.get_json()
    id = data.get('id')
    pw = data.get('pw')
    name = data.get('name')
    place = data.get('place')
    if(sub.createNewUserAccount(id,pw,name,place)):
        return jsonify({"message": 'good'})
    else:
        return jsonify({"message" : 'bad'})


@app.errorhandler(404)
def page_not_found(error):
    return f"페이지가 없습니다. 에러원인 : {error}", 404

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(debug=True)

