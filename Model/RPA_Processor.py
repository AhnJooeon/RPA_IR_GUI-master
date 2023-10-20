from Model.DGB_Processor import DGBProcessor
from Model.BNK_Processor import BNKProcessor
from Model.JBFG_Processor import JBFGProcessor
from Model.SFG_Processor import SFGProcessor
from Model.KB_Processor import KBProcessor
from Model.WFG_Processor import WFGProcessor
from Model.HFG_Processor import HFGProcessor
from Presenter.Progress_Presenter import ProgressPresenter
from Model.Singleton_Instance import SingletonInstance
import os
from PySide6.QtCore import *
import pandas as pd
import os
class RPAProcessor(QRunnable, SingletonInstance):
    sig = Signal()
    def __init__(self, parent=None):
        super().__init__()
        self.pause = False
        self.processDic = {'대구':DGBProcessor,
                           '부산':BNKProcessor,
                           '경남':BNKProcessor,
                           '전북':JBFGProcessor,
                           '광주':JBFGProcessor,
                           '신한':SFGProcessor,
                           '국민':KBProcessor,
                           '우리':WFGProcessor,
                           '하나':HFGProcessor}
        # self.processDic = {'신한':SFGProcessor}

    def start(self):
        print("---- Start overload ----")
        self.prog = ProgressPresenter.instance
        self.Run()
        print("---- Stop QRun ----")

    def run(self):
        print("---- run overload ----")
        self.prog = ProgressPresenter.instance
        self.Run()
        print("---- stop run ----")

    def Set_Path(self, out, fact, rule):
        tmp = os.path.split(out)
        self.write_path = f'{tmp[0]}/[결과]{tmp[1]}'
        rule_path = rule

        self.output_df = pd.read_excel(out)
        self.rule_df = pd.read_csv(rule_path)

        self.bankDic, self.typeDic = self.Set_RuleDic(self.rule_df)
        self.Get_FactBook(fact)

    def Get_FactBook(self, path):
        try:
            fileList = os.listdir(path)
            self.factPath = {}
            for i in range(self.rule_df.shape[0]):
                tmp_path = ''
                bankName = self.rule_df.iloc[i, 0]
                fileName = self.rule_df.iloc[i, 2]
                for j in fileList:
                    if fileName in j:
                        tmp_path = j
                        break
                if tmp_path != '':
                    self.factPath[bankName] = f"{path}/{tmp_path}"
        except Exception as ex:
            print(f"Get_FactBook : {ex}")


    def num_to_col_letters(self, num):
        letters = ''
        while num:
            mod = (num - 1) % 26
            letters += chr(mod + 65)
            num = (num - 1) // 26
        return ''.join(reversed(letters))

    def find_colname(self, colName):
        initNum = 1

        while True:
            tmpName = self.num_to_col_letters(initNum)

            if tmpName == colName:
                # print(f"Find : {initNum}")
                return initNum - 2  # df가 A부터 시작이 아님
            else:
                initNum += 1

    def Set_RuleDic(self, df):
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

    def Run(self):
        bank = ""
        try:
            self.prog.Set_Task("RPA - IR", self.output_df.shape[0])
            for i in range(self.output_df.shape[0]):
                if self.pause:
                    break

                self.prog.Set_Progress(i)

                tmp = self.output_df.iloc[i, 0]
                if not pd.isna(tmp):
                    tmp = tmp.replace('\r', '')
                    tmp = tmp.replace('\n', '')

                    if tmp in self.typeDic.keys():
                        typeName = tmp
                        # break
                    if tmp in self.bankDic.keys():
                        bank = tmp

                    print(f"i : {i} / bank : {bank} / type : {typeName}")

                    # if typeName != "은행 보통주자본비율단위 : %":
                    #     continue

                    if typeName and bank != "" and bank in self.processDic.keys():
                        rule_row = self.bankDic[bank]
                        rule_col = self.typeDic[typeName]
                        sheetName = self.rule_df.iloc[rule_row, rule_col]
                        if bank in self.processDic.keys():  # 임시?
                            proc = self.processDic[bank]()
                        print(f"Sheet Name : {sheetName}")

                        if pd.isna(bank) or pd.isna(sheetName):
                            pass
                        else:
                            path = self.factPath[bank]
                            sheets = sheetName.split('/')
                            fact_df = pd.read_excel(path, sheet_name=sheets[0], index_col=0)
                            for colNum in range(1, self.output_df.shape[1]):  # 엑셀파일/시트 ... 임시 제거 (-1)
                                value = self.output_df.iloc[i, colNum]
                                if pd.isna(value):
                                    qua = self.output_df.iloc[0, colNum]
                                    colName = self.rule_df.iloc[rule_row, 3]
                                    colIndex = self.find_colname(colName)
                                    proc.Get_Setting(self.factPath)

                                    # 칼럼이 다른 곳에 위치할 수도 있음
                                    for colLoop in range(0, 3):
                                        fact_value = proc.Get_FactBook(fact_df, sheetName, qua, colIndex + colLoop)
                                        if pd.notna(fact_value):
                                            break

                                    # Unit 적용
                                    units = self.rule_df.iloc[rule_row, 1]
                                    units = units.split('/')
                                    if type(fact_value) is not str:
                                        if '%' in typeName:
                                            fact_value = fact_value * int(units[1])  # %
                                        else:
                                            fact_value = fact_value * int(units[0])  # 억

                                        #
                                        # if fact_value < 100:
                                        #     fact_value = fact_value * int(units[1])  # %
                                        # else:
                                        #     fact_value = fact_value * int(units[0])  # 억

                                    self.output_df.iloc[i, colNum] = fact_value
                                    # print(f"Date : {qua}")

                        self.output_df.to_excel(self.write_path)

            print("End Run")
            self.pause = True
        except Exception as ex:
            print(f"[Run]{ex}")

    def Stop(self):
        print("Stop")