import pandas as pd
class DGBProcessor():
    def __init__(self):
        print()

    def Get_Setting(self, bank_dic):
        self.bank_dic = bank_dic

    def Quater(self, tmp):
        try:
            dateDic = {'1H': '2Q', 'FY': '4Q'}
            qua = tmp[:2]  # 1H -> 2Q
            year = tmp[2:4]
            print(f"Quater : {qua} / Year : {year}")
            if qua in dateDic.keys():
                qua = dateDic[qua]
            else:
                date = tmp

            date = f"{qua}{year}"
        except Exception as ex:
            print(ex)

        return date

    def Get_ComplexType(self, fact_df, sheets, colIndex):
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
                        if sheets[2] in tmp_value:
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

    def Get_NomalType(self, fact_df, sheets, colIndex):
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

    def Get_SumType(self, fact_df, sheets, colIndex):
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

    def Get_RowType(self, sheets):
        idx = 0
        tmp = sheets[1].split(':')
        tmp = tmp[1].replace(' ', '')
        tmp = tmp.replace('+', '')
        idx = int(tmp)
        idx = idx - 2  # 우리은행 기준 row - 2
        return idx

    def Get_Typenum(self, fact_df, sheets, colIndex):
        typeNum = 0
        try:
            if len(sheets) > 2:
                typeNum = self.Get_ComplexType(fact_df, sheets, colIndex)
            elif ',' in sheets[1]:
                typeNum = self.Get_SumType(fact_df, sheets, colIndex)  # list 반환
            elif 'row:' in sheets[1]:
                typeNum = self.Get_RowType(sheets)
            else:
                typeNum = self.Get_NomalType(fact_df, sheets, colIndex)
        except Exception as ex:
            print(ex)
        return typeNum

    def Get_Colnum(self, fact_df, date):
        colnum = 0
        date_col = 3
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
    def Get_FactBook(self, fact_df, sheet, qua, colIndex):
        fact_value = ""
        date_colNum = float('nan')
        try:
            # path = self.bank_dic[bank]
            sheets = sheet.split('/')
            # print(fact_df)
            # fact_df = pd.read_excel(path, sheet_name=sheets[0], index_col=0)
            # colIndex = find_colname(colName)
            typeNum = self.Get_Typenum(fact_df, sheets, colIndex)
            date = self.Quater(qua)
            date_colNum = self.Get_Colnum(fact_df, date)

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