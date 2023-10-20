import pandas as pd
import traceback
class WFGProcessor():
    def __init__(self):
        self.std_Date = ['1Q', '2Q', '3Q', '4Q']

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

            date = f"FY20{year}{qua}"  # 우리은행 형태
        except Exception as ex:
            print(traceback.format_exc())

        return date

    def Get_Quater(self, tmp):
        try:
            dateDic = {'1H': '2Q', 'FY': '4Q'}
            qua = tmp[:2]  # 1H -> 2Q
            year = tmp[2:4]
            print(f"Quater : {qua} / Year : {year}")
            dates = []
            if qua in dateDic.keys():
                qua = dateDic[qua]
            for i in self.std_Date:
                date = f"FY20{year}{i}"
                dates.append(date)
                if i == qua:
                    break
        except Exception as ex:
            print(traceback.format_exc())

        return dates

    def Get_ComplexType(self, fact_df, sheets, colIndex):
        startRow = 0  # 카피 확인 i를 넣어서 같을수도 있음
        endRow = 0
        idx = 0
        tol = 0

        topTitle = len(sheets) - 1

        # 덩어리 찾기
        for i in range(fact_df.shape[0]):
            try:
                tmp_value = fact_df.iloc[i, colIndex]
                if startRow == 0:
                    if not pd.isna(tmp_value):
                        tmp_value = tmp_value.replace(' ', '')
                        tmp_value = tmp_value.replace("'", "")
                        tmp_std = sheets[topTitle].replace(' ', '')
                        if tmp_std in tmp_value:
                            startRow = i
                else:
                    if pd.isna(tmp_value):
                        for bais in range(0, 4):
                            bais_value = fact_df.iloc[i, colIndex + bais]
                            if pd.notna(bais_value):
                                break
                        endRow = i
                        if pd.isna(bais_value):
                            tol += 1
                    else:
                        if tol > 3:
                            endRow = i
                            break
                        else:
                            tol = 0

                    if tol > 15:
                        break
            except Exception as ex:
                print(traceback.format_exc())

        # nan 나오기전에 루프가 끝나는 경우
        if endRow != 0 and tol < 3:
            endRow = fact_df.shape[0]

        # Text에 '/'가 있는 경우..? (Nomal Type)
        if startRow and endRow == 0:
            endRow = fact_df.shape[0]  # 한번 더 찾기

        # 덩어리에서 칼럼 찾기
        for bais in range(0, 4):
            for j in range(startRow, endRow):
                try:
                    tmp_value = fact_df.iloc[j, colIndex + bais]
                    if pd.notna(tmp_value):
                        tmp_value = tmp_value.replace(' ', '')
                        if '/' in tmp_value:
                            tmp_std = f"{sheets[1]}/{sheets[2]}"
                            tmp_std = tmp_std.replace(' ', '')
                        else:
                            tmp_std = sheets[1].replace(' ', '')
                        if tmp_value == tmp_std:
                            idx = j
                            print(f"idx in Get_ComplexType : {idx} / {sheets[1]} / {sheets[2]}")
                            return idx
                except Exception as ex:
                    print(traceback.format_exc())

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
                print(traceback.format_exc())

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
                    print(traceback.format_exc())

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
            print(traceback.format_exc())
        return typeNum

    def Get_Colnum(self, fact_df, date, date_col):
        colnum = 0
        try:
            if type(date) == list:
                colnums = []
                for j in range(fact_df.shape[1]):
                    tmp_value = fact_df.iloc[date_col, j]
                    if pd.notna(tmp_value):
                        for tmp_date in date:
                            tmp_value = tmp_value.replace("'", "")
                            tmp_value = tmp_value.replace('"', "")
                            tmp_value = tmp_value.replace(' ', "")
                            if tmp_value == tmp_date:
                                colnums.append(j)

                colnum = colnums
            else:
                # 일반적인 상황
                for j in range(fact_df.shape[1]):
                    tmp_value = fact_df.iloc[date_col, j]
                    if pd.notna(tmp_value):
                        tmp_value = tmp_value.replace(' ', '')
                        tmp_value = tmp_value.replace("'", '')
                        if tmp_value == date:
                            colnum = j
                            break

        except Exception as ex:
            print(traceback.format_exc())

        return colnum

    def Get_Columns(self, fact_df, date, date_col, sheet):
        try:
            colnum = 0
            for j in range(fact_df.shape[1]):
                tmp_value = fact_df.iloc[date_col, j]
                if pd.notna(tmp_value):
                    tmp_value = tmp_value.replace(' ', '')
                    date = date.replace(' ', '')
                    if tmp_value == date:
                        colnum = j

            if sheet == "Net Interest Margin":
                colnum += 2
        except Exception as ex:
            print(traceback.format_exc())
        return colnum
    def Get_FactBook(self, fact_df, sheet, qua, colIndex):
        fact_value = 0
        date_colNum = float('nan')
        # colIndex -= 1
        try:
            # path = self.bank_dic[bank]
            sheets = sheet.split('/')

            for i in range(0, 3):
                typeNum = self.Get_Typenum(fact_df, sheets, colIndex + i)
                if typeNum != 0:
                    break

            if sheets[1].endswith('+'):
                date = self.Get_Quater(qua)
            else:
                date = self.Quater(qua)  # Factbook 형태로 반환

            date_col = 2
            date_colNum = 0
            for i in range(0, 2):
                if sheets[0] == "NIM NIS_Bank":
                    date_colNum = self.Get_Columns(fact_df, date, date_col + i, sheets[1])
                else:
                    date_colNum = self.Get_Colnum(fact_df, date, date_col + i)

                if date_colNum != 0:
                    break

            # Year만 있는 4Q 경우
            if date_colNum == 0:
                tmp_date = date[:6]
                date_colNum = self.Get_Colnum(fact_df, tmp_date, date_col)

            if type(typeNum) == list:
                for sum_idx in typeNum:
                    fact_value += fact_df.iloc[sum_idx, date_colNum]  # 합산 확인 필요
            elif type(date_colNum) == list:
                for sum_date in date_colNum:
                    fact_value += fact_df.iloc[typeNum, sum_date]  # 합산 확인 필요
            else:
                if pd.notna(typeNum) and pd.notna(date_colNum):
                    fact_value = fact_df.iloc[typeNum, date_colNum]
                    # strTest = fact_df.iloc[typeNum, date_colNum].str
            print(f"fact_value : {fact_value} / date : {date} / TypeNum : {typeNum} / date_colNum : {date_colNum}")
            # print(f"str Result : {strTest}")

            if sheets[0] == 'NIM NIS_Bank' and fact_value < 100:
                fact_value = fact_value / 100  # % 값이 아닌 일반 소수점

        except Exception as ex:
            print(traceback.format_exc())

        return fact_value