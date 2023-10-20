import pandas as pd


class SFGProcessor():
    def __init__(self):
        print()
        self.std_Date = ['1Q', '2Q', '3Q', '4Q']
        self.allDateDic = {'1H': '2Q', 'FY': '4Q',
                           '2Q': '1H', '4Q': 'FY'}

    def Get_Setting(self, bank_dic):
        self.bank_dic = bank_dic

    # tmp : DGB Output Date Format
    def Quater(self, tmp):
        try:
            # dateDic = {'1H': '2Q', 'FY': '4Q'}
            dateDic = {'2Q': '1H', '4Q': 'FY'}
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

    def Convert_Date(self, date):  # date = 23.06 Format
        cdate = ""
        try:
            numDic = {'03': '1Q', '06': '1H',
                      '09': '3Q', '12': 'FY'}
            if '.' in str(date):
                date = date.replace("'", "")
                tmp = date.split('.')
                tmp[1] = tmp[1].zfill(2)
                cdate = f"{numDic[tmp[1]]}{tmp[0]}"  # 2Q23
            else:
                cdate = date

        except Exception as ex:
            print(ex)

        return cdate

    def Get_Quater(self, tmp):
        try:
            dateDic = {'1H': '2Q', 'FY': '4Q'}
            numDic = {'1Q':'03', '1H':'06',
                      '3Q':'09', 'FY':'12'}
            tmp = tmp.replace("'", "")
            if '.' in tmp: # 23.06
                tmp = tmp.split('.')
                if len(tmp) > 1:
                    year = tmp[0]
                    qua = tmp[1]
            else:
                year = tmp[:2]
                qua = tmp[2:4]
            print(f"Quater : {qua} / Year : {year}")

            dates = []
            if qua in dateDic.keys():
                qua = dateDic[qua]
            for i in self.std_Date:
                date = f"{i}{year}"
                dates.append(date)
                if i == qua:
                    break

        except Exception as ex:
            print(ex)

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
                        tol += 1

                    else:
                        if tol > 3 :
                            endRow = i
                            break
                        else:
                            tol = 0

                    # if tol > 15:
                    #     break
            except Exception as ex:
                print(ex)

        # nan 나오기전에 루프가 끝나는 경우
        if endRow != 0 and tol < 3:
            endRow = fact_df.shape[0]

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
                    print(ex)
        # Sum
        if ',' in sheets[1]:
            tmp_df = fact_df.iloc[startRow:endRow]
            for bais in range(0, 3):
                idx = self.Get_SumType(tmp_df, sheets, colIndex+bais)  # list 반환
                if type(idx) == list and len(idx) > 1:
                    for i in range(len(idx)):
                        idx[i] = startRow + idx[i]

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

        if len(idxs) == 0:
            idxs = 0

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
            elif ',' in sheets[1]:  # 이름에 , 가 포함임
                # 이름에 "," 포함된 경우
                tmp_type = sheets[1].split(',')
                if len(tmp_type) > 2:
                    typeNum = self.Get_SumType(fact_df, sheets, colIndex)  # list 반환
                else:
                    typeNum = self.Get_NomalType(fact_df, sheets, colIndex)
            elif 'row:' in sheets[1]:
                typeNum = self.Get_RowType(sheets)
            else:
                typeNum = self.Get_NomalType(fact_df, sheets, colIndex)

        except Exception as ex:
            print(ex)
        return typeNum

    def Get_Colnum(self, fact_df, date, date_col):
        colnum = 0
        try:
            # 일반적인 상황
            for j in range(fact_df.shape[1]):
                tmp_value = fact_df.iloc[date_col, j]
                if pd.notna(tmp_value):
                    if date in tmp_value:  # IFRS-17이 들어가 있음
                        colnum = j
                        break

                    qua = date[:2]
                    year = date[2:4]
                    if qua in self.allDateDic.keys():
                        tmp_date = f"{self.allDateDic[qua]}{year}"
                        if tmp_date in tmp_value:
                            colnum = j
                            break

            # 23.06 숫자 상황
            if colnum == 0:
                for j in range(fact_df.shape[1]):
                    tmp_value = fact_df.iloc[date_col, j]
                    tmp_value = self.Convert_Date(tmp_value)
                    if tmp_value == date:
                        colnum = j
                        break

        except Exception as ex:
            print(ex)

        return colnum

    def Get_FactBook(self, fact_df, sheet, qua, colIndex):
        fact_value = 0
        date_colNum = float('nan')
        colIndex -= 1
        try:
            sheets = sheet.split('/')
            for i in range(0, 3):
                typeNum = self.Get_Typenum(fact_df, sheets, colIndex + i)
                if typeNum != 0:
                    break

            # if '+' in sheets[1]:
            if sheets[1].endswith('+'):
                date = self.Get_Quater(qua)
            else:
                date = self.Quater(qua)  # Factbook 형태로 반환

            date_col = 1  # 대구:3 / BNK:1 / JBFG : 1
            date_colNum = 0
            for i in range(0, 2):
                date_colNum = self.Get_Colnum(fact_df, date, date_col + i)
                if date_colNum != 0:
                    break

            if type(typeNum) == list:
                for sum_idx in typeNum:
                    fact_value += fact_df.iloc[sum_idx, date_colNum]  # 합산 확인 필요
            elif type(date_colNum) == list:
                for sum_date in date_colNum:
                    fact_value += fact_df.iloc[typeNum, sum_date]  # 합산 확인 필요
            else:
                if pd.notna(typeNum) and pd.notna(date_colNum):
                    fact_value = fact_df.iloc[typeNum, date_colNum]
            print(f"fact_value : {fact_value} / date : {date} / TypeNum : {typeNum} / date_colNum : {date_colNum}")

        except Exception as ex:
            print(ex)

        return fact_value