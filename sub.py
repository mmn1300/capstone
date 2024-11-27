import define.constant_data as constant
import define.init_def as init
import define.database_def as database
import define.weather_def as weather
import define.etc_def as etc


############### /define/constant_data.py ###############

jsonDatapath = constant.jsonDatapath

todayFormattedDate = constant.todayFormattedDate
yesterdayFormattedDate = constant.yesterdayFormattedDate
approvalCode = constant.approvalCode

categoryCode = constant.categoryCode
categoryModelPath = constant.categoryModelPath
categoryForecastingResultPath = constant.categoryForecastingResultPath
categoryKoreanName = constant.categoryKoreanName
productTypeKorenName = constant.productTypeKorenName
categoryImagePath = constant.categoryImagePath

########################################################



############### /define/init_def.py ###############

def getJSON(path):
    return init.getJSON(path)

def setJSON(data, path):
    return init.setJSON(data, path)

def deleteJSON(path):
    return init.deleteJSON(path)

def variablesInit():
    return init.variablesInit()

def getUserDataPath(mcode):
    return init.getUserDataPath(mcode)

def userVariablesInit(mcode):
    return init.userVariablesInit(mcode)

def getDroidCamURL(ip):
    return init.getDroidCamURL(ip)

def setModelInputData():
    return init.setModelInputData()

def getDateCount(date):
    return init.getDateCount(date)

##########################################################



############### /define/database_def.py ###############

def getSelectSQL(mcode, category=''):
    return database.getSelectSQL(mcode, category)

def getSelectAllSQL(mcode):
    return database.getSelectAllSQL(mcode)

def setTodaySalesRateTable(date=todayFormattedDate):
    return database.setTodaySalesRateTable(date)

def sellProduceFormInventory(items, nums, mcode):
    return database.sellProduceFormInventory(items, nums, mcode)

def addTodaySalesRate(items, nums, mcode):
    return database.addTodaySalesRate(items, nums, mcode)

def getSalesSQL(mcode, date=todayFormattedDate):
    return database.getSalesSQL(mcode, date)

def setSQL(texts, texts2, numbers, mcode):
    return database.setSQL(texts, texts2, numbers, mcode)
    
def setUpdateSQL(icList, qList, pList, mcode):
    return database.setUpdateSQL(icList, qList, pList, mcode)

def getSalesFit(mcode, date = todayFormattedDate):
    return database.getSalesFit(mcode, date)

def getAllCategory(mcode):
    return database.getAllCategory(mcode)

def getAllProductName(categoryList, mcode):
    return database.getAllProductName(categoryList, mcode)

def getCategory(name, mcode):
    return database.getCategory(name, mcode)

def getQuantity(name, mcode):
    return database.getQuantity(name, mcode)

def getAllNameAndPrice(mcode):
    return database.getAllNameAndPrice(mcode)

def getInventoryQuantity(mcode):
    return database.getInventoryQuantity(mcode)

def setYesterdaySalesRate(mcode, yesterdayFormattedDate=yesterdayFormattedDate, categoryCode=categoryCode):
    return database.setYesterdaySalesRate(mcode, yesterdayFormattedDate, categoryCode)

def getPriceSQL(itemName, mcode):
    return database.getPriceSQL(itemName, mcode)

def getTodaySalesRate(mcode):
    return database.getTodaySalesRate(mcode)

def getAddTodaySales(rows1, rows2):
    return database.getAddTodaySales(rows1, rows2)

def loginCheck(id,pw):
    return database.loginCheck(id,pw)

def getUserInfo(id,pw):
    return database.getUserInfo(id,pw)

def idCheck(id):
    return database.idCheck(id)

def nicknameCheck(name):
    return database.nicknameCheck(name)

def placeCheck(place):
    return database.placeCheck(place)

def createNewUserAccount(id,pw,name,place):
    return database.createNewUserAccount(id,pw,name,place)

def getMcode(place):
    return database.getMcode(place)

def getAllPlace():
    return database.getAllPlace()

def getSumOfCategoryQuantity(mcode):
    return database.getSumOfCategoryQuantity(mcode)

def deleteMember(id, mcode):
    return database.deleteMember(id, mcode)

def getAllMember():
    return database.getAllMember()

def deleteItem(code, name, mcode):
    return database.deleteItem(code, name, mcode)

###########################################################



############### /define/weather_def.py ###############
def setTodayWeather():
    return weather.setTodayWeather()

def setweatherInfo():
    return weather.setweatherInfo()

def getTodayWeatherData():
    return weather.getTodayWeatherData()

def getPastWeather(target_date):
    return weather.getPastWeather(target_date)

##################################################



############### /define/etc_def.py ###############

def createXlsx(info, cellData, remark):
    return etc.createXlsx(info, cellData, remark)

def getDistributedQuantity(qlist, total_items):
    return etc.getDistributedQuantity(qlist, total_items)

##################################################




























