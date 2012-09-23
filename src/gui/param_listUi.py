# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'param_list.ui'
#
# Created: Mon Oct 03 01:56:49 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_param_list(object):
    def setupUi(self, param_list):
        param_list.setObjectName(_fromUtf8("param_list"))
        param_list.resize(149, 44)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(param_list.sizePolicy().hasHeightForWidth())
        param_list.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(param_list)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(param_list)
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_groupBox = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_groupBox.setSpacing(1)
        self.verticalLayout_groupBox.setMargin(2)
        self.verticalLayout_groupBox.setObjectName(_fromUtf8("verticalLayout_groupBox"))
        self.list_comboBox = QtGui.QComboBox(self.groupBox)
        self.list_comboBox.setObjectName(_fromUtf8("list_comboBox"))
        self.verticalLayout_groupBox.addWidget(self.list_comboBox)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(param_list)
        QtCore.QMetaObject.connectSlotsByName(param_list)

    def retranslateUi(self, param_list):
        param_list.setWindowTitle(QtGui.QApplication.translate("param_list", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("param_list", "This is the parameter name", None, QtGui.QApplication.UnicodeUTF8))

