from Model.DGB_Format import DGBFormat
from openpyxl.utils.cell import get_column_letter
import pandas as pd

Fact_path = 'Data/DGB FactBook 2Q23.xlsx'
sheet = 'B_IS'
colName = 'E'
Fact_df = pd.read_excel(Fact_path, sheet_name=sheet, index_col=0)
print(Fact_df)

output_path = './Data/국내은행IR DATA(2023.2Q)_test.xlsx'
output_df = pd.read_excel(output_path)
print(output_df)

bank_path = {'대구':'Data/DGB FactBook 2Q23.xlsx',
             '부산':'Data/BNKFG2Q23_Factbook(K)(F).xlsx',
             '경남':'Data/BNKFG2Q23_Factbook(K)(F).xlsx'}
bank_format = {'대구':DGBFormat}
dateDic = {'1H':'2Q', 'FY':'4Q'}

# {bank, path} Dic 필요 <- 폴더에서 불러오기
def num_to_col_letters(num):
    letters = ''
    while num:
        mod = (num - 1) % 26
        letters += chr(mod + 65)
        num = (num - 1) // 26
    return ''.join(reversed(letters))

def Quater(tmp):
    try:
        qua = tmp[:2]  # 1H -> 2Q
        year = tmp[2:4]
        print(f"Quater : {qua} / Year : {year}")
        if qua in dateDic.keys():
            # date = f"{dateDic[qua]}{year}"
            qua = dateDic[qua]

        date = f"FY20{year} {qua}"  # BNK 형태
    except Exception as ex:
        print(ex)

    return date

def find_colname(colName):
    initNum = 1

    while True:
        tmpName = num_to_col_letters(initNum)

        if tmpName == colName:
            # print(f"Find : {initNum}")
            return initNum - 2  # df가 A부터 시작이 아님
        else:
            initNum += 1

def Get_ComplexType(fact_df, sheets, colIndex):
    startRow = 0  # 카피 확인 i를 넣어서 같을수도 있음
    endRow = 0
    idx = 0
    tol = 0

    # 덩어리 찾기
    for i in range(fact_df.shape[0]):
        try:
            tmp_value = fact_df.iloc[i, colIndex]
            if startRow == 0:
                if not pd.isna(tmp_value):
                    tmp_value = tmp_value.replace(' ', '')
                    tmp_std = sheets[2].replace(' ', '')
                    if tmp_std in tmp_value:
                        startRow = i
            else:
                if pd.isna(tmp_value):
                    endRow = i
                    tol += 1
                else:
                    tol = 0

                if tol > 3:
                    break
        except Exception as ex:
            print(ex)

    # nan 나오기전에 루프가 끝나는 경우
    if endRow != 0 and tol < 3:
        endRow = fact_df.shape[0]


    # 덩어리에서 칼럼 찾기
    for j in range(startRow, endRow):
        try:
            tmp_value = fact_df.iloc[j, colIndex]
            tmp_value = tmp_value.replace(' ', '')
            tmp_std = sheets[1].replace(' ', '')
            if tmp_value == tmp_std:
                idx = j
                print(f"idx in Get_ComplexType : {idx} / {sheets[1]} / {sheets[2]}")
                break
        except Exception as ex:
            print(ex)

    return idx

def Get_NomalType(fact_df, sheets, colIndex):
    idx = 0
    for i in range(fact_df.shape[0]):
        try:
            tmp_value = fact_df.iloc[i, colIndex]
            if pd.isna(tmp_value):
                pass
            else:
                tmp_value = tmp_value.replace(' ', '')

            tmp_std = sheets[1].replace(' ', '')
            if tmp_value == tmp_std:
                idx = i
        except Exception as ex:
            print(ex)

    return idx

def Get_SumType(fact_df, sheets, colIndex):
    idxs = []
    sum_list = sheets[1].split(',')

    for sumName in sum_list:
        for i in range(fact_df.shape[0]):
            try:
                tmp_value = fact_df.iloc[i, colIndex]
                if pd.isna(tmp_value):
                    pass
                else:
                    tmp_value = tmp_value.replace(' ', '')

                sumName = sumName.replace(' ', '')
                if tmp_value == sumName:
                    idxs.append(i)
                    break
            except Exception as ex:
                print(ex)

    return idxs



def Get_Typenum(fact_df, sheets, colIndex):
    typeNum = 0
    try:
        if len(sheets) > 2:
            typeNum = Get_ComplexType(fact_df, sheets, colIndex)
        elif ',' in sheets[1]:
            typeNum = Get_SumType(fact_df, sheets, colIndex)  # list 반환
        else:
            typeNum = Get_NomalType(fact_df, sheets, colIndex)
    except Exception as ex:
        print(ex)
    return typeNum


def Get_Colnum(fact_df, date):
    colnum = 0
    date_col = 1   # 대구:3 / BNK:1
    try:
        # 일반적인 상황
        for j in range(fact_df.shape[1]):
            tmp_value = fact_df.iloc[date_col, j]
            if tmp_value == date:
                colnum = j
                return colnum

        # 금액, 비중 포함인 상황
        for j in range(fact_df.shape[1]):
            tmp_value = fact_df.iloc[date_col, j]
            if tmp_value == '금액' or tmp_value == '비중':
                date_col = date_col - 1
                tmp_value = fact_df.iloc[date_col, j]

            if tmp_value == date:
                colnum = j
                return colnum

        # 등급법 포함인 경우?
        date_col += 1
        for j in range(fact_df.shape[1]):
            tmp_value = fact_df.iloc[date_col, j]
            if tmp_value == date:
                colnum = j
                break
    except Exception as ex:
        print(ex)

    return colnum

def Get_FactBook(bank, sheet, qua):
    fact_value = ""
    date_colNum = float('nan')
    try:
        path = bank_path[bank]
        # format = bank_format[bank]
        sheets = sheet.split('/')
        # print(fact_df)
        fact_df = pd.read_excel(path, sheet_name=sheets[0], index_col=0)
        colIndex = find_colname(colName) - 1
        typeNum = Get_Typenum(fact_df, sheets, colIndex)
        date = Quater(qua)  # Factbook 형태로 반환
        date_colNum = Get_Colnum(fact_df, date)

        if not pd.isna(date_colNum):
            if type(typeNum) == list:
                fact_value = 0
                for sum_idx in typeNum:
                    fact_value += fact_df.iloc[sum_idx, date_colNum]  # 합산 확인 필요
            else:
                if not pd.isna(typeNum):
                    fact_value = fact_df.iloc[typeNum, date_colNum]
            print(f"fact_value : {fact_value} / date : {date}")
    except Exception as ex:
        print(ex)

    return fact_value


def Set_RuleDic(df):
    Bank_dict = dict()
    type_dict = dict()

    for idx, row in df.iterrows():
        Bank_dict[row['Type']] = idx
    print(f"Rule Dict Key / Value : {Bank_dict.keys()} / {Bank_dict.values()}")

    idx = 0
    for i in df.columns:
        i = i.replace('\r', '')
        i = i.replace('\n', '')
        if "Unnamed" not in i:
            type_dict[i] = idx
            idx += 1
            print(f"Rule df.column : {i}")  # Unnamed 제외 필요

    print(f"type Dict Key / Value : {type_dict.keys()} / {type_dict.values()}")
    return Bank_dict, type_dict

rule_path = './Data/Rule_Format.csv'
rule_df = pd.read_csv(rule_path)
bankDic, typeDic = Set_RuleDic(rule_df)

thredhold = 0
rowNum = 0
typeName = ""
bank = ""

for i in range(output_df.shape[0]):
    tmp = output_df.iloc[i, 0]
    if not pd.isna(tmp):
        tmp = tmp.replace('\r', '')
        tmp = tmp.replace('\n', '')

    if tmp in typeDic.keys():
        typeName = tmp
        # break
    if tmp in bankDic.keys():
        bank = tmp

    print(f"i : {i} / bank : {bank} / type : {typeName}")

    if typeName and bank != "":
        rule_row = bankDic[bank]
        rule_col = typeDic[typeName]
        sheetName = rule_df.iloc[rule_row, rule_col]
        print(f"Sheet Name : {sheetName}")

        if pd.isna(bank) or pd.isna(sheetName):
            pass
        else:
            for colNum in range(1, output_df.shape[1] - 1):  # 엑셀파일/시트 ... 임시 제거 (-1)
                value = output_df.iloc[i, colNum]
                if pd.isna(value):
                    qua = output_df.iloc[0, colNum]
                    # print(f"Date : {qua}")
                    if bank == '부산' or bank == '경남':  # 임시
                        fact_value = Get_FactBook(bank, sheetName, qua)
                        output_df.iloc[i, colNum] = fact_value

        output_df.to_excel(f'Test_02.xlsx')