from PySide6.QtWidgets import *
from PySide6.QtCore import *
import time
import threading
from View.Main_View import Ui_MainWindow
from Model.RPA_Processor import RPAProcessor
from Presenter.Progress_Presenter import ProgressPresenter
import Model.RPA_Processor

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.btnReadOpen.clicked.connect(self.Read_Folder)
        self.btnOutOpen.clicked.connect(self.Read_Open)
        self.btnStart.clicked.connect(self.Start)
        self.btnStop.clicked.connect(self.Stop)

        self.dot = 0

        # self.prog = ProgressPresenter.instance()
        self.Set_Timer()

        self.rule_Path = './Data/Rule_Format.csv'
        self.lbRule.setText(self.rule_Path)
        self.inst = RPAProcessor.instance()
        self.prog = ProgressPresenter.instance()

    def Defalut_Setting(self):
        print("init")
        self.Set_FormatFile()

    def Read_Folder(self):
        print("folder")
        self.folder = QFileDialog.getExistingDirectory(None, "폴더 선택")
        print(self.folder)
        self.tbReadFolder.setText(self.folder)

    def Read_Open(self):
        print("Click ReadOpen")
        self.fname = QFileDialog.getOpenFileName(self)
        self.tbWriteFile.setText(self.fname[0])

    def Start(self):
        self.timeVar.start()
        self.inst = RPAProcessor()
        self.inst.Set_Path(self.fname[0], self.folder, self.rule_Path)
        self.inst.pause = False
        start = time.time()
        self.threadpool = QThreadPool()
        self.threadpool.start(self.inst)
        end = time.time()
        print(f"{end - start:.5f} sec")

    def Stop(self):
        # self.threadpool.deleteLater()
        self.inst.pause = True
        self.timeVar.stop()

    def Set_Timer(self):
        # Define timer.
        self.timeVar = QTimer()
        self.timeVar.setInterval(500)  # msecs 100 = 1/10th sec
        self.timeVar.timeout.connect(self.Update_Progress)

    def Update_Progress(self):
        dot_text = "."
        for i in range(self.dot):
            dot_text += "."
        # self.lbProgress.setText(f"{self.prog.task_name}{dot_text}")
        # print(f"Running Timer {dot_text}")

        if self.dot > 3:
            self.dot = 0
        else:
            self.dot += 1

        self.progressBar.setMaximum(self.prog.max_value)
        self.progressBar.setValue(self.prog.cur_value)
        self.lbProgress.setText(f"{self.prog.cur_value} / {self.prog.max_value} {dot_text}")

        if self.inst.pause == True:
            self.timeVar.stop()



