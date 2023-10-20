from PySide6.QtWidgets import QApplication
from Presenter.Main_Presenter import MainWindow

def Main_Show():
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')
    Main_Show()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
