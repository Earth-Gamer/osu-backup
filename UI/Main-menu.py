# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Main-menu.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(500, 180)
        MainWindow.setMinimumSize(QSize(500, 180))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setCursor(QCursor(Qt.ArrowCursor))
        self.label.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout.addWidget(self.label)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 20, 10, 20)
        self.CreateBackup = QPushButton(self.centralwidget)
        self.CreateBackup.setObjectName(u"CreateBackup")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.CreateBackup.sizePolicy().hasHeightForWidth())
        self.CreateBackup.setSizePolicy(sizePolicy1)
        self.CreateBackup.setCursor(QCursor(Qt.PointingHandCursor))
        self.CreateBackup.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))

        self.verticalLayout.addWidget(self.CreateBackup)

        self.EditBackup = QPushButton(self.centralwidget)
        self.EditBackup.setObjectName(u"EditBackup")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.EditBackup.sizePolicy().hasHeightForWidth())
        self.EditBackup.setSizePolicy(sizePolicy2)
        self.EditBackup.setCursor(QCursor(Qt.PointingHandCursor))
        self.EditBackup.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))

        self.verticalLayout.addWidget(self.EditBackup)

        self.ReadBackup = QPushButton(self.centralwidget)
        self.ReadBackup.setObjectName(u"ReadBackup")
        sizePolicy1.setHeightForWidth(self.ReadBackup.sizePolicy().hasHeightForWidth())
        self.ReadBackup.setSizePolicy(sizePolicy1)
        self.ReadBackup.setCursor(QCursor(Qt.PointingHandCursor))
        self.ReadBackup.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))

        self.verticalLayout.addWidget(self.ReadBackup)

        self.Options = QPushButton(self.centralwidget)
        self.Options.setObjectName(u"Options")
        sizePolicy1.setHeightForWidth(self.Options.sizePolicy().hasHeightForWidth())
        self.Options.setSizePolicy(sizePolicy1)
        self.Options.setCursor(QCursor(Qt.PointingHandCursor))
        self.Options.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))

        self.verticalLayout.addWidget(self.Options)


        self.horizontalLayout.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"osu!backup", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.CreateBackup.setText(QCoreApplication.translate("MainWindow", u"Create Backup", None))
        self.EditBackup.setText(QCoreApplication.translate("MainWindow", u"Edit Backup file", None))
        self.ReadBackup.setText(QCoreApplication.translate("MainWindow", u"Download beatmaps", None))
        self.Options.setText(QCoreApplication.translate("MainWindow", u"Options", None))
    # retranslateUi

