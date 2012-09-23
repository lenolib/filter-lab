# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'param_empty.ui'
#
# Created: Tue Oct 04 18:55:24 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_param_empty(object):
    def setupUi(self, param_empty):
        param_empty.setObjectName(_fromUtf8("param_empty"))
        param_empty.resize(149, 70)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(param_empty.sizePolicy().hasHeightForWidth())
        param_empty.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(param_empty)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(param_empty)
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_groupBox = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_groupBox.setSpacing(1)
        self.verticalLayout_groupBox.setMargin(2)
        self.verticalLayout_groupBox.setObjectName(_fromUtf8("verticalLayout_groupBox"))
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(param_empty)
        QtCore.QMetaObject.connectSlotsByName(param_empty)

    def retranslateUi(self, param_empty):
        param_empty.setWindowTitle(QtGui.QApplication.translate("param_empty", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("param_empty", "This is the parameter name", None, QtGui.QApplication.UnicodeUTF8))

