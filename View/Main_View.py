# -*- coding: utf-8 -*-
import os.path

################################################################################
## Form generated from reading UI file 'MainView.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QMenuBar, QProgressBar,
    QPushButton, QSizePolicy, QStatusBar, QVBoxLayout,
    QWidget)
import sys

def resource_path(relative_path):
    """Get Absolute path to resource, works for dev and for PyInstaller"""
    # base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 100)
        icon_path = resource_path('./data/rpa.ico')
        MainWindow.setWindowIcon(QIcon(icon_path))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(150, 0))
        self.label_4.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout_4.addWidget(self.label_4)

        self.lbRule = QLabel(self.centralwidget)
        self.lbRule.setObjectName(u"lbRule")

        self.horizontalLayout_4.addWidget(self.lbRule)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_4.addWidget(self.label_8)


        self.gridLayout.addLayout(self.horizontalLayout_4, 2, 0, 1, 1)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(150, 0))
        self.label.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout.addWidget(self.label)

        self.tbReadFolder = QLineEdit(self.centralwidget)
        self.tbReadFolder.setObjectName(u"tbReadFolder")

        self.horizontalLayout.addWidget(self.tbReadFolder)

        self.btnReadOpen = QPushButton(self.centralwidget)
        self.btnReadOpen.setObjectName(u"btnReadOpen")
        self.btnReadOpen.setMinimumSize(QSize(100, 0))
        self.btnReadOpen.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.btnReadOpen)


        self.verticalLayout_3.addLayout(self.horizontalLayout)


        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.lbProgress = QLabel(self.centralwidget)
        self.lbProgress.setObjectName(u"lbProgress")
        self.lbProgress.setMinimumSize(QSize(150, 0))
        self.lbProgress.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout_5.addWidget(self.lbProgress)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.horizontalLayout_5.addWidget(self.progressBar)


        self.gridLayout.addLayout(self.horizontalLayout_5, 3, 0, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.btnStart = QPushButton(self.centralwidget)
        self.btnStart.setObjectName(u"btnStart")

        self.horizontalLayout_7.addWidget(self.btnStart)

        self.btnStop = QPushButton(self.centralwidget)
        self.btnStop.setObjectName(u"btnStop")

        self.horizontalLayout_7.addWidget(self.btnStop)


        self.gridLayout.addLayout(self.horizontalLayout_7, 4, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(150, 0))
        self.label_2.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout_2.addWidget(self.label_2)

        self.tbWriteFile = QLineEdit(self.centralwidget)
        self.tbWriteFile.setObjectName(u"tbWriteFile")

        self.horizontalLayout_2.addWidget(self.tbWriteFile)

        self.btnOutOpen = QPushButton(self.centralwidget)
        self.btnOutOpen.setObjectName(u"btnOutOpen")
        self.btnOutOpen.setMinimumSize(QSize(100, 0))
        self.btnOutOpen.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_2.addWidget(self.btnOutOpen)


        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 24))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"RPA IR Ver_1.0.0", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Rule Format", None))
        self.lbRule.setText("")
        self.label_8.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Read Folder(FactBook)", None))
        self.btnReadOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.lbProgress.setText(QCoreApplication.translate("MainWindow", u"Task", None))
        self.btnStart.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.btnStop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Wirte File", None))
        self.btnOutOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
    # retranslateUi

