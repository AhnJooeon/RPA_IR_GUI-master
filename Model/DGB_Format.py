from Model.Bank_Format import BankFormat
import pandas as pd


# 기준 Format
class DGBFormat(BankFormat):
    def __init__(self):
        self.dateRow = 5  # Date Row
        self.dateDic = dict()

    def Set_FactBook(self, path, sheet, col):
        self.df = pd.read_excel(path, sheet_name=sheet, index_col=0)
        self.col = col

    # 1Q23, 2Q23 ...
    def Quater(self, tmp):
        qua = tmp[:1]  # 1H -> 2Q
        year = tmp[2:4]
        print(f"Quater : {qua} / Year : {year}")
        date = f"{self.dateDic[qua]}{year}"
        return date

    def Get_IRTypeNum(self, name):
        typecolNum  = self.find_colname(self.col)
        typerowNum = 0  # 0 인지 확인 필요
        while True:
            tmpName = self.df.loc[typerowNum, typecolNum]

            if tmpName == self.col:
                return typerowNum
            else:
                typerowNum += 1


    def Get_IRType(self, typeName):
        types = typeName.split('/')  # len > 1 한 Sheet에 내용 두개 이상 ex) NIM 분기 / 누적
        if len(types) > 1:
            print(f"누적 / 분기 : {types[1]}")
        else:
            self.Get_IRTypeNum()

    # Format 통일
    # date : 분기값 / Type : 필요한 항목 이름 ex) 당기순이익
    # 해당 value 반환
    def Get_Value(self, date, type):
        qua = self.Quater(date)  # DGB FactBook Date Format
        dataRow = self.Get_IRType(type)  # Row 고정용

        init_queNum = 0

        # While 사용 고려 필요
        while True:
            # 해당 Column 찾기
            quacol = self.df.loc[self.dateRow, init_queNum]

            if qua == quacol:
                val = self.df.loc[dataRow, init_queNum]
                return val
            else:
                init_queNum += 1