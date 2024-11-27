from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from starlette.middleware.sessions import SessionMiddleware
from math import ceil
import sub
import subprocess
import web_cam.POS as p
import os

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="aaaaaaaaaaaa")

# 정적 파일 제공 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

# 템플릿 설정
templates = Jinja2Templates(directory="templates")

# 서버 시작시 사용할 변수 파일 및 테이블, 각 모델 예측값 파일을 초기화
sub.variablesInit()
sub.setTodaySalesRateTable()
sub.setTodayWeather()
for text_file_path in list(sub.categoryForecastingResultPath.values()):
    if os.path.exists(text_file_path):
        with open(text_file_path, "w") as file:
            file.write("0")

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
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    if request.session.get('user_place'):
        request.session.pop('user_place', None)
    if request.session.get('IP-URL'):
        request.session.pop('IP-URL', None)

    username = request.session.get('username','')
    place = request.session.get('place','')
    
    return templates.TemplateResponse("index_page.html", {
        "request": request,
        "username": username,
        "place": place})


# 시작화면 -> 지점 선택
@app.get('/place', response_class=HTMLResponse)
async def select_place(request: Request):
    return templates.TemplateResponse('place_select.html', {
        "request": request,
        "placeList":sub.getAllPlace()})


@app.post('/create_user_session')
async def create_user_session(request: Request):
    data = await request.json()
    place = data.get('place')
    ipToURL = data.get('IP-URL')
    request.session['user_place'] = place
    request.session['IP-URL'] = ipToURL
    return JSONResponse(content={"message" : True})


# 시작화면 -> 유저 페이지
@app.get('/user_page', response_class=HTMLResponse)
async def user_page(request: Request):
    return templates.TemplateResponse('user_page.html', {"request": request})


# 시작화면 -> 유저 페이지 -> 홈
@app.get('/user_page/logout')
async def user_logout(request: Request):
    request.session.pop('user_place', None)
    request.session.pop('IP-URL', None)
    username = request.session.get('username')
    place = request.session.get('place')
    return templates.TemplateResponse('index_page.html', {
        "request": request,
        "username": username,
        "place": place})


# 시작화면 -> 유저 페이지 -> 관리자
@app.get('/user_page/admin_page')
async def user_admin_page(request: Request):
    request.session.pop('user_place', None)
    request.session.pop('IP-URL', None)
    username = request.session.get('username')
    place = request.session.get('place')
    if(username == '최고관리자'):
        return templates.TemplateResponse('member_management.html', {"request": request})
    elif(username):
        return templates.TemplateResponse('admin_page.html', {
        "request": request,
        "username": username,
        "place": place})
    else:
        return templates.TemplateResponse('login_form.html', {"request": request})


# 유저 페이지 (상품 결제 처리)
@app.put("/user_page/payment")
async def payment_page(request: Request):
    data = await request.json()

    placeInfo = request.session.get('user_place')
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

    return JSONResponse(content={'result': 'good'})


@app.get("/video_feed")
async def video_feed(request: Request):
    return StreamingResponse(p.generate_frames(sub.getDroidCamURL(request.session.get('IP-URL'))), media_type='multipart/x-mixed-replace; boundary=frame')

@app.post("/capture_image")
async def capture_image(request: Request):
    if p.current_frame is not None:
        # 이미지 예측
        predicted_class = p.predict_image(p.current_frame)
        korean_name = p.classKoreanName[predicted_class]
        
        # JSON 응답 생성
        return JSONResponse(content={
            'itemName': korean_name,
            'category': p.category[predicted_class],
            'price': sub.getPriceSQL(korean_name, sub.getMcode(request.session.get('user_place'))),
            'imagePath': p.itemImagePath[korean_name]
        })

    return JSONResponse(content={'result': 'No image captured'})


# 시작화면 -> 관리자 페이지 (일반 -> 관리자 메뉴, 최고관리자 -> 회원 관리)
@app.get('/admin_page', response_class=HTMLResponse)
async def admin_page(request: Request):
    username = request.session.get('username')
    mcode = request.session.get('mcode')
    place = request.session.get('place')
    if(mcode == 0):
        rows = sub.getAllMember()
        return templates.TemplateResponse('member_management.html', {
            "request": request,
            "rows": rows})
    elif(mcode):
        return templates.TemplateResponse('admin_page.html', {
            "request": request,
            "username": username,
            "place": place})
    else:
        return templates.TemplateResponse('login_form.html', {"request": request})
    

# 시작화면 -> 최고 관리자 페이지 -> 회원 삭제
@app.delete('/member/delete')
async def member_delete(request: Request):
    data = await request.json()
    id = data.get('id')
    mcode = data.get('mcode')
    result = sub.deleteMember(id, int(mcode))
    return JSONResponse(content={'result': result})
    


# 관리자 페이지 -> 재고 물품 등록 및 정보
@app.get("/admin_page/inventory_info", response_class=HTMLResponse)
async def inventory_info(request: Request):
    data = sub.getJSON(sub.jsonDatapath)
    
    start_line = sub.getDateCount(sub.todayFormattedDate)
    for key, path in sub.categoryForecastingResultPath.items():
        sum_of_three_predicted_sales = 0
        sum_of_seven_predicted_sales = 0
        
        with open(path, 'r') as file:
            lines = file.readlines()
            end_line = start_line + 6
            predictData = lines[start_line - 1:end_line]
            predictData = [float(item.strip()) for item in predictData if item.strip().replace('.', '', 1).isdigit()]
        
        for i in range(len(predictData)):
            if isinstance(predictData[i], str):  # 문자열인지 확인
                if i < 3:
                    sum_of_three_predicted_sales += float(predictData[i].strip())
                sum_of_seven_predicted_sales += float(predictData[i].strip())
            else:
                if i < 3:
                    sum_of_three_predicted_sales += predictData[i]
                sum_of_seven_predicted_sales += predictData[i]
        
        data["threeDaysPredictedSales"][key] = round(sum_of_three_predicted_sales, 2)
        data["sevenDaysPredictedSales"][key] = round(sum_of_seven_predicted_sales, 2)
    
    sub.setJSON(data, sub.jsonDatapath)
    
    return templates.TemplateResponse("inventory_info.html", {
        "request": request,
        "username":request.session.get('username'),
        "place":request.session.get('place')})


# 관리자 페이지 -> 판매 내역
@app.get("/admin_page/sales_history", response_class=HTMLResponse)
async def sales_history(request: Request):
    mcode = request.session.get('mcode')
    # sales_history 테이블에 오늘 날짜의 데이터를 받아옴
    rows = sub.getAddTodaySales(sub.getSalesFit(mcode), sub.getTodaySalesRate(mcode))
    
    # 오늘의 날씨 정보를 받음
    data = sub.getJSON(sub.jsonDatapath)
    weather_info = data["todayWeatherInfo"]
    
    return templates.TemplateResponse("sales_history.html", {
        "request": request,
        "rows": rows,
        "place":request.session.get('place'),
        "weatherInfo": weather_info})


# 관리자 페이지 -> 판매 내역 (날짜 별)
@app.get("/admin_page/sales_history/select_date")
async def day_sales_history(request: Request, date: str):
    # sales_history 테이블에 존재하는 date일자의 데이터를 받아옴
    rows=()
    mcode = request.session.get('mcode')
    if date == sub.todayFormattedDate:
        rows = sub.getAddTodaySales(sub.getSalesFit(mcode), sub.getTodaySalesRate(mcode))
    else:
        rows = sub.getSalesFit(mcode, date)
    return JSONResponse(content=rows)


# 시작화면 -> 관리자 페이지 -> 수요 예측전 모델 동작에 필요한 것들을 셋팅
@app.get('/admin_page/predict_model_load', response_class=HTMLResponse)
async def predict_model_load(request: Request):
    sub.setYesterdaySalesRate(request.session.get('mcode'))
    data = sub.getJSON(sub.jsonDatapath)
    if data["weatherLoad"] == True:
        sub.setModelInputData()
        returnData = sub.setweatherInfo()
        if returnData is not None:
            responseData = {
                "request": request,
                "message":"모델을 불러오는 도중 에러가 발생했습니다.",
                "error":returnData
                }
            return templates.TemplateResponse('result.html', responseData)
        
        data["weatherLoad"] = False
        sub.setJSON(data, sub.jsonDatapath)

    # 아래 코드는 시간 단위마다 데이터가 갱신되므로 일회성 동작 처리 불가
    returnData = sub.getTodayWeatherData()
    if returnData is not None:
            responseData = {
                "request": request,
                "message":"모델을 불러오는 도중 에러가 발생했습니다.",
                "error":returnData
                }
            return templates.TemplateResponse('result.html', responseData)
    
    return templates.TemplateResponse('predict_model_load.html', {"request":request})


# 시작화면 -> 관리자 페이지 -> 재고 물품 등록 및 정보 -> 재고 등록
@app.get('/admin_page/inventory_info/inventory_warehousing', response_class=HTMLResponse)
async def inventory_warehousing(request: Request):
    rows = sub.getSelectAllSQL(request.session.get('mcode'))
    return templates.TemplateResponse('inventory_warehousing.html', {"request": request, "rows":rows})


# 관리자 페이지 -> 재고 물품 등록 -> DB 재고 등록 (백엔드 처리)
@app.post("/admin_page/inventory_info/inventory_warehousing/db_insert", response_class=HTMLResponse)
async def db_insert(request: Request, texts: list[str] = Form(...), texts2: list[str] = Form(...), numbers: list[str] = Form(...)):
    message = "에러가 발생했습니다."

    # 데이터를 받아 데이터베이스에 입력하고 결과를 받음
    message, rows = sub.setSQL(texts, texts2, numbers, request.session.get('mcode'))

    sumOfThreeDaysPredictSales = {sub.categoryKoreanName[key]: data["threeDaysPredictedSales"][key] for key in data["threeDaysPredictedSales"]}
    sumOfSevenDaysPredictSales = {sub.categoryKoreanName[key]: data["sevenDaysPredictedSales"][key] for key in data["sevenDaysPredictedSales"]}

    # 정상, 비정상 실행 시에 따른 렌더링
    if message == 'good':
        data = sub.getJSON(sub.jsonDatapath)
        responseData = {
            "request": request,
            "rows": rows,
            "category": "all",
            "sumOfCategoryQuantity": sub.getSumOfCategoryQuantity(request.session.get('mcode')),
            "sumOfThreeDaysPredictSales": sumOfThreeDaysPredictSales,
            "sumOfSevenDaysPredictSales": sumOfSevenDaysPredictSales
        }
        return templates.TemplateResponse("query_result.html", responseData)
    else:
        responseData = {
            "request": request,
            "message": message,
            "error": "유효하지 않은 요청"
        }
        return templates.TemplateResponse("result.html", responseData)


# 시작화면 -> 관리자 페이지 -> 재고 물품 등록 및 정보 -> 재고 정보 출력
@app.get('/admin_page/inventory_info/products', response_class=HTMLResponse)
async def db_query_category(request: Request, category: str):
    if category != 'all':
        rows = sub.getSelectSQL(request.session.get('mcode'), sub.productTypeKorenName[category])
    else:
        rows = sub.getSelectSQL(request.session.get('mcode'))
    data = sub.getJSON(sub.jsonDatapath)
    sumOfThreeDaysPredictSales = {sub.categoryKoreanName[key]: data["threeDaysPredictedSales"][key] for key in data["threeDaysPredictedSales"]}
    sumOfSevenDaysPredictSales = {sub.categoryKoreanName[key]: data["sevenDaysPredictedSales"][key] for key in data["sevenDaysPredictedSales"]}
    responseData = {
            "request": request,
            "rows": rows,
            "category" : category,
            "sumOfCategoryQuantity": sub.getSumOfCategoryQuantity(request.session.get('mcode')),
            "sumOfThreeDaysPredictSales": sumOfThreeDaysPredictSales,
            "sumOfSevenDaysPredictSales": sumOfSevenDaysPredictSales
        }
    return templates.TemplateResponse('query_result.html', responseData)


# 시작화면 -> 관리자 페이지 -> 재고 물품 등록 및 정보 -> 재고 정보 출력 -> 재고량, 가격 변경(백엔드 처리)
@app.put('/admin_page/inventory_info_update')
async def inventory_item_update(request: Request):
    try:
        data = await request.json()
        itemCodeArray = data.get('productCodes')
        quantityArray = data.get('quantitys')
        priceArray = data.get('prices')

        sub.setUpdateSQL(itemCodeArray, quantityArray, priceArray, request.session.get('mcode'))
        return JSONResponse(content={"data" : "good"})

    except Exception as e:
        return JSONResponse(content={"error" : str(e)})
    

# 시작화면 -> 관리자 페이지 -> 재고 물품 등록 및 정보 -> 재고 정보 출력 -> 상품 삭제
@app.delete('/admin_page/product/delete')
async def inventory_item_delete(request: Request):
    try:
        data = await request.json()
        itemCode = int(data.get('code'))
        itemName = data.get('name')
        result = sub.deleteItem(itemCode, itemName, request.session.get('mcode'))
        return JSONResponse(content={"result" : result})

    except Exception as e:
        return JSONResponse(content={"result" : False, "error" : str(e)})
    

# 시작화면 -> 관리자 페이지 -> 수요 예측 -> 카테고리별 수요 예측
@app.get('/admin_page/demand_forecasting', response_class=HTMLResponse)
async def forecasting(request: Request, category: str):
    def run_script_and_get_output(script_name):
        # subprocess.run()을 사용하여 다른 스크립트를 실행하고 결과를 받아옴
        result = subprocess.run(
            ['python', script_name],  # 실행할 명령어
            capture_output=True,      # 표준 출력과 표준 오류를 캡처
            text=True                 # 출력 결과를 텍스트로 처리
        )
        return result.stdout
    
    sub.getInventoryQuantity(request.session.get('mcode'))
    data = sub.getJSON(sub.jsonDatapath)
    userData = sub.getJSON(sub.getUserDataPath(request.session.get('mcode')))

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
    
    # 필요한 기간만큼 수요 예측 정보를 읽음
    start_line = sub.getDateCount(sub.todayFormattedDate)
    with open(sub.categoryForecastingResultPath[category], 'r') as file:
        lines = file.readlines()
        
        # 특정 행부터 8번째 행까지 읽어옴
        end_line = start_line + 7
        predictData = lines[start_line - 1:end_line]
        predictData = [float(item.strip()) for item in predictData if item.strip().replace('.', '', 1).isdigit()]

    responseData={
        "request": request,
        "categoryName": category,
        "categoryQuantity": data["inventoryQuantity"][category],
        "imgPath": sub.categoryImagePath[category],
        "weatherTextData": data["todayWeatherInfo"],
        "weatherNumberData": weatherData,
        "yesterdaySalesRate": userData["yesterdaySalesRate"][category],
        "predictData": predictData
    }

    return templates.TemplateResponse('predict_result.html', responseData)


# 시작화면 -> 관리자 페이지 -> 수요 예측 -> 카테고리별 수요 예측 -> 특정 날짜 수요예측
@app.get('/admin_page/demand_forecasting/date', response_class=HTMLResponse)
async def date_demand_predict(request: Request, category: str, date: str):
    start_line = sub.getDateCount(date)
    with open(sub.categoryForecastingResultPath[category], 'r') as file:
        # 파일의 모든 행을 읽음
        lines = file.readlines()
        
        # 특정 행부터 8번째 행까지 읽어옴
        end_line = start_line + 7
        predictData = lines[start_line - 1:end_line]
        predictData = [float(item.strip()) for item in predictData if item.strip().replace('.', '', 1).isdigit()]
        weatherData = sub.getPastWeather(date)

    return JSONResponse(content={
        "newPredictData" : predictData,
        "weatherData": weatherData})


# 시작화면 -> 관리자 페이지 -> 발주서 작성
@app.get('/admin_page/order_page', response_class=HTMLResponse)
def order_page(request: Request):
    categoryList = sub.getAllCategory(request.session.get('mcode'))
    cl = []
    for pt in categoryList.values():
        for c in pt:
            cl.append(c)
    responseData = {
            "request": request,
            "productTypeToCategory": categoryList,
            "categoryToProductName": sub.getAllProductName(cl, request.session.get('mcode')), 
            "productNameToCodeAndPrice": sub.getAllNameAndPrice(request.session.get('mcode')),
            "place": request.session.get('place')
            }
    return templates.TemplateResponse('order_page.html', responseData)


# 시작화면 -> 관리자 페이지 -> 발주서 작성 -> AI 추천
@app.post('/admin_page/order_page/predict')
async def ai_recommendation(request: Request):
    mcode = request.session.get('mcode')
    data = await request.json()
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

    return JSONResponse(content={
        "distributedQuantityDict" : distributedQuantityDict # {category:[value1, value2, ...]}
    })


# 관리자 페이지 -> 발주서 작성 -> 발주서 생성
@app.post("/admin_page/order_page/create_xlsx", response_class=HTMLResponse)
async def create_xlsx(request : Request, info: list[str] = Form(...), item_info: list[str] = Form(...), remark: str = Form(...)):
    try:
        file_name = sub.createXlsx(info, item_info, remark)
        return templates.TemplateResponse("xlsx_download.html", {"request": request, "fileName": file_name})
    except:
        responseData = {
            "request": request,
            "message": "파일 생성에 오류가 발생했습니다.",
            "error": "유효하지 않은 요청"
        }
        return templates.TemplateResponse("result.html", responseData)


# 시작화면 -> 관리자 페이지 -> 발주서 작성 -> 발주서 다운로드
@app.get("/admin_page/order_page/create_xlsx/download/{fileName}")
async def download_file(fileName: str):
    file_path = f'purchase_order/{fileName}'  # 서버의 파일 경로

    # 파일이 존재하는지 확인
    try:
        return FileResponse(
            file_path,
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # 엑셀 파일 MIME 타입
            filename=fileName
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")


# 로그인 페이지
@app.get('/login_form', response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse('login_form.html', {"request": request})

# 로그인 아이디 확인
@app.post("/login/id")
async def login_id(request: Request):
    data = await request.json()
    if sub.idCheck(data.get('id')):
        return JSONResponse(content={"message": "exists"})
    else:
        return JSONResponse(content={"message": "not exists"})

# 로그인 비밀번호 확인
@app.post("/login/pw")
async def login_pw(request: Request):
    data = await request.json()
    if sub.loginCheck(data.get('id'), data.get('pw')):
        return JSONResponse(content={"message": "exists"})
    else:
        return JSONResponse(content={"message": "not exists"})

# 로그인 (세션 생성)
@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, id: str = Form(...), pw: str = Form(...)):
    mcode, nickname, place = sub.getUserInfo(id, pw)
    request.session['mcode'] = mcode
    request.session['username'] = nickname
    request.session['place'] = place

    if mcode == 0:
        rows = sub.getAllMember()
        return templates.TemplateResponse("member_management.html", {
            "request": request,
            "rows": rows})
    else:
        sub.userVariablesInit(mcode)
        return templates.TemplateResponse("admin_page.html", {
            "request": request,
            "username": nickname,
            "place": place})

# 로그 아웃
@app.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    mcode = request.session.get('mcode')
    request.session.pop('mcode', None)
    request.session.pop('username', None)
    request.session.pop('place', None)
    sub.deleteJSON(sub.getUserDataPath(mcode))

    return templates.TemplateResponse("index_page.html", {
        "request": request,
        "username": "",
        "place": ""})


# 회원가입 페이지
@app.get('/account_form', response_class=HTMLResponse)
async def account_form(request: Request):
    return templates.TemplateResponse('create_account.html', {"request": request})

# 회원가입 -> 아이디 체크 (입력한 아이디가 이미 존재하는지 확인)
@app.post('/account/id')
async def account_id(request: Request):
    data = await request.json()
    id = data.get('id')

    if(sub.idCheck(id)==False):
        return JSONResponse(content={"idCheck": True})
    else:
        return JSONResponse(content={"idCheck": False})
        
# 회원가입 -> 닉네임 체크 (입력한 닉네임이 이미 존재하는지 확인)
@app.post('/account/nickname')
async def account_name(request: Request):
    data = await request.json()
    nickname = data.get('nickname')

    if(sub.nicknameCheck(nickname)==False):
        return JSONResponse(content={"nicknameCheck": True})
    else:
        return JSONResponse(content={"nicknameCheck": False})

# 회원가입 -> 지점명 체크 (입력한 지점의 계정이 이미 존재하는지 확인)
@app.post('/account/place')
async def account_place(request: Request):
    data = await request.json()
    place = data.get('place')

    if(sub.placeCheck(place)==False):
        return JSONResponse(content={"placeCheck": True})
    else:
        return JSONResponse(content={"placeCheck": False})

# 회원가입 -> 승인 코드 체크 (입력한 승인 코드가 일치하는지 확인)
@app.post('/account/code')
async def account_code(request: Request):
    data = await request.json()
    code = data.get('code')

    if(sub.approvalCode==int(code)):
        return JSONResponse(content={"codeCheck": True})
    else:
        return JSONResponse(content={"codeCheck": False})

# 회원가입 (새 계정 생성 및 데이터베이스 등록)
@app.post('/account/create')
async def create_account(request: Request):
    data = await request.json()
    id = data.get('id')
    pw = data.get('pw')
    name = data.get('name')
    place = data.get('place')
    if(sub.createNewUserAccount(id,pw,name,place)):
        return JSONResponse(content={"message": 'good'})
    else:
        return JSONResponse(content={"message" : 'bad'})




# 로컬호스트 ->  터미널에 uvicorn app2:app --reload 를 입력하여 실행함

# 사설네트워크 -> 터미널에 uvicorn app2:app --host 0.0.0.0 --port 8000 를 입력하여 실행함





























