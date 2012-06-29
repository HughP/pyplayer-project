# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\PyPlayer\ui\progresswindow.ui'
#
# Created: Sat May 12 11:07:13 2012
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
        progressDialog.resize(400, 130)
        self.label = QtGui.QLabel(progressDialog)
        self.label.setGeometry(QtCore.QRect(10, 20, 371, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.progressBar = QtGui.QProgressBar(progressDialog)
        self.progressBar.setGeometry(QtCore.QRect(30, 60, 211, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.pushButton = QtGui.QPushButton(progressDialog)
        self.pushButton.setGeometry(QtCore.QRect(300, 90, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))

        self.retranslateUi(progressDialog)
        QtCore.QMetaObject.connectSlotsByName(progressDialog)

    def retranslateUi(self, progressDialog):
        progressDialog.setWindowTitle(QtGui.QApplication.translate("progressDialog", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("progressDialog", "Обрабатывается:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("progressDialog", "Отмена", None, QtGui.QApplication.UnicodeUTF8))

