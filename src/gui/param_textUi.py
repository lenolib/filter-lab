# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'param_text.ui'
#
# Created: Mon Oct 03 01:56:51 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_param_text(object):
    def setupUi(self, param_text):
        param_text.setObjectName(_fromUtf8("param_text"))
        param_text.resize(149, 65)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(param_text.sizePolicy().hasHeightForWidth())
        param_text.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(param_text)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(param_text)
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_groupBox = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_groupBox.setSpacing(1)
        self.verticalLayout_groupBox.setMargin(2)
        self.verticalLayout_groupBox.setObjectName(_fromUtf8("verticalLayout_groupBox"))
        self.text_lineEdit = QtGui.QLineEdit(self.groupBox)
        self.text_lineEdit.setObjectName(_fromUtf8("text_lineEdit"))
        self.verticalLayout_groupBox.addWidget(self.text_lineEdit)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(param_text)
        QtCore.QMetaObject.connectSlotsByName(param_text)

    def retranslateUi(self, param_text):
        param_text.setWindowTitle(QtGui.QApplication.translate("param_text", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("param_text", "This is the parameter name", None, QtGui.QApplication.UnicodeUTF8))

