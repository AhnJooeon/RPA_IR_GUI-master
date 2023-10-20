from PySide6.QtCore import *
class MainController(QThread):
    print()


    def __init__(self, parent=None):
        super().__init__()
        self.flag = True
        self.prog = ProgressPresenter.instance()

    def run(self):
        # self.Naver_Crawling()
        print()

    def stop(self):
        self.quit()