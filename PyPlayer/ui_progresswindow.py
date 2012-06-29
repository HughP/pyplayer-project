# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\pyplayer\ui\progresswindow.ui'
#
# Created: Fri Jun 22 20:30:37 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_progressDialog(object):
    def setupUi(self, progressDialog):
        progressDialog.setObjectName(_fromUtf8("progressDialog"))
        progressDialog.resize(400, 139)
        self.label = QtGui.QLabel(progressDialog)
        self.label.setGeometry(QtCore.QRect(10, 20, 121, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.pushButton = QtGui.QPushButton(progressDialog)
        self.pushButton.setGeometry(QtCore.QRect(10, 100, 81, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.checkBox = QtGui.QCheckBox(progressDialog)
        self.checkBox.setGeometry(QtCore.QRect(10, 60, 131, 17))
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.abort = QtGui.QPushButton(progressDialog)
        self.abort.setGeometry(QtCore.QRect(100, 100, 75, 23))
        self.abort.setObjectName(_fromUtf8("abort"))
        self.anim = QtGui.QLabel(progressDialog)
        self.anim.setGeometry(QtCore.QRect(240, 20, 111, 101))
        self.anim.setText(_fromUtf8(""))
        self.anim.setScaledContents(True)
        self.anim.setObjectName(_fromUtf8("anim"))

        self.retranslateUi(progressDialog)
        QtCore.QMetaObject.connectSlotsByName(progressDialog)

    def retranslateUi(self, progressDialog):
        progressDialog.setWindowTitle(QtGui.QApplication.translate("progressDialog", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("progressDialog", "Обрабатывается:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("progressDialog", "Сканировать", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("progressDialog", "Очистка библиотеки", None, QtGui.QApplication.UnicodeUTF8))
        self.abort.setText(QtGui.QApplication.translate("progressDialog", "Отмена", None, QtGui.QApplication.UnicodeUTF8))

