# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'param_codebox.ui'
#
# Created: Thu Oct 06 15:27:57 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_param_codebox(object):
    def setupUi(self, param_codebox):
        param_codebox.setObjectName(_fromUtf8("param_codebox"))
        param_codebox.resize(149, 84)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(param_codebox.sizePolicy().hasHeightForWidth())
        param_codebox.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(param_codebox)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(param_codebox)
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_groupBox = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_groupBox.setSpacing(1)
        self.verticalLayout_groupBox.setMargin(2)
        self.verticalLayout_groupBox.setObjectName(_fromUtf8("verticalLayout_groupBox"))
        self.codebox_Qsci = Qsci.QsciScintilla(self.groupBox)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier New"))
        font.setPointSize(10)
        self.codebox_Qsci.setFont(font)
        self.codebox_Qsci.setToolTip(_fromUtf8(""))
        self.codebox_Qsci.setWhatsThis(_fromUtf8(""))
        self.codebox_Qsci.setObjectName(_fromUtf8("codebox_Qsci"))
        self.verticalLayout_groupBox.addWidget(self.codebox_Qsci)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(param_codebox)
        QtCore.QMetaObject.connectSlotsByName(param_codebox)

    def retranslateUi(self, param_codebox):
        param_codebox.setWindowTitle(QtGui.QApplication.translate("param_codebox", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("param_codebox", "This is the parameter name", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import Qsci
