#####################################################
#####################################################
##### 그 외 유틸성 라이브러리 관련 함수 정의 파일 #####
#####################################################
#####################################################

import xlsxwriter
from datetime import datetime
import torch



def createXlsx(info, cellData, remark):
    now = datetime.now()
    formatted_time = now.strftime("%Y%m%d_%I%M%p").lower()  # YYYYMMDD_HHmmam/pm 형식으로 시간 포맷팅

    # 엑셀 파일 이름 생성
    file_name = f'purchase_order/발주서_{formatted_time}.xlsx'

    # 발주서 데이터를 코드에서 작성
    order_info = {
        "발주 번호": info[0],
        "스타일 번호": info[1],
        "발주일": info[2],
        "납품일": info[3],
        "발주처": info[4],
        "납품처": info[5]
    }

    # 품목 정보 (10개의 항목), 열 이름
    items = []

    for i in range(0,len(cellData),5):
        items.append({"상품 코드": cellData[i], "상품 명": cellData[i+1], "수량": cellData[i+2], "개당 단가": cellData[i+3]})

    # 엑셀 파일 생성
    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet('발주서')

    # 서식 정의
    formats = {
        "title": workbook.add_format({'align': 'center', 'valign': 'vcenter', 'bold': True, 'font_size': 16, 'border': 1}),
        "header": workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1, 'bg_color': '#E6E6FA', 'bold': True}),  # 연한 보라색
        "cell": workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter'}),
        "merge_header": workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1, 'bold': True, 'bg_color': '#d9e1f2'}),
        "note": workbook.add_format({'border': 1, 'align': 'left', 'valign': 'top'})
    }

    # 열 너비 설정
    worksheet.set_column('A:A', 15)  # 상품 코드
    worksheet.set_column('B:C', 20)  # 상품 명 (두 칸 사용)
    worksheet.set_column('D:F', 15)  # 수량, 개당 단가, 총 금액

    # 발주서 제목 추가
    worksheet.merge_range('A1:F1', '발 주 서', formats["title"])

    # 발주서 정보 부분 입력
    headers = ['발주 번호', '스타일 번호', '발주일', '납품일', '발주처', '납품처']
    values = [order_info['발주 번호'], order_info['스타일 번호'], order_info['발주일'], order_info['납품일'], order_info['발주처'], order_info['납품처']]

    for i in range(3):  # 정보는 3행까지 있음
        worksheet.merge_range(f'A{i+2}:B{i+2}', headers[i*2], formats["merge_header"])
        worksheet.write(f'C{i+2}', values[i*2], formats["cell"])
        worksheet.merge_range(f'D{i+2}:E{i+2}', headers[i*2+1], formats["merge_header"])
        worksheet.write(f'F{i+2}', values[i*2+1], formats["cell"])

    # 품목 정보 테이블 헤더 입력 (연한 보라색 배경)
    worksheet.write('A6', '상품 코드', formats["header"])
    worksheet.merge_range('B6:C6', '상품 명', formats["header"])  # 상품 명 두 칸 사용
    worksheet.write('D6', '수량', formats["header"])
    worksheet.write('E6', '개당 단가', formats["header"])
    worksheet.write('F6', '총 금액', formats["header"])

    # 품목 정보 입력 (7행부터 시작)
    for idx, item in enumerate(items, start=7):
        worksheet.write(f'A{idx}', item['상품 코드'], formats["cell"])
        worksheet.merge_range(f'B{idx}:C{idx}', item['상품 명'], formats["cell"])  # 상품명을 두 칸 사용
        worksheet.write(f'D{idx}', item['수량'], formats["cell"])
        worksheet.write(f'E{idx}', item['개당 단가'], formats["cell"])
        if(item['수량'] == '' or item['개당 단가'] == ''):
            worksheet.write(f'F{idx}', '', formats["cell"])
        else:
            worksheet.write(f'F{idx}', int(item['수량']) * int(item['개당 단가']), formats["cell"])  # 총 금액 계산

    # 비고란 추가
    worksheet.merge_range('A17:F20', '비 고 : '+remark, formats["note"])

    # 파일 저장
    workbook.close()

    file_name = file_name.replace('purchase_order/', '')

    return file_name


# 필요 수량을 현재 재고 수량에 따라 분배해주는 함수
def getDistributedQuantity(qlist, total_items):
    for i in range(len(qlist)):
        if qlist[i] == 0:
            qlist[i] = 1

    # 예제 데이터 설정
    costs = torch.tensor(qlist, dtype=torch.float32)  # 대상 A, B, C, D의 비용

    # 비용 기반 역비례 가중치 계산
    weights = 1 / costs  # 비용이 낮을수록 더 높은 가중치
    weights_normalized = weights / weights.sum()  # 가중치 정규화

    # 물건 배분
    allocation = (weights_normalized * total_items).floor()  # 정수로 배분
    remaining_items = total_items - allocation.sum()  # 소수점으로 남은 물건 계산

    # 남는 물건 처리 (가중치가 높은 순으로 배분)
    for i in torch.argsort(weights_normalized, descending=True):
        if remaining_items > 0:
            allocation[i] += 1
            remaining_items -= 1

    # 최종 배분 출력
    # print("최적 배분 결과:", allocation.int().tolist())
    # print("총 배분 개수:", int(allocation.sum()))

    return allocation.int().tolist()
