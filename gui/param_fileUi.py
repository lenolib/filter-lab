# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'param_file.ui'
#
# Created: Mon Oct 03 01:56:48 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_param_file(object):
    def setupUi(self, param_file):
        param_file.setObjectName(_fromUtf8("param_file"))
        param_file.resize(149, 69)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(param_file.sizePolicy().hasHeightForWidth())
        param_file.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(param_file)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(param_file)
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_groupBox = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_groupBox.setSpacing(1)
        self.verticalLayout_groupBox.setMargin(2)
        self.verticalLayout_groupBox.setObjectName(_fromUtf8("verticalLayout_groupBox"))
        self.fileButton = QtGui.QPushButton(self.groupBox)
        self.fileButton.setObjectName(_fromUtf8("fileButton"))
        self.verticalLayout_groupBox.addWidget(self.fileButton)
        self.historyComboBox = QtGui.QComboBox(self.groupBox)
        self.historyComboBox.setInsertPolicy(QtGui.QComboBox.InsertAtTop)
        self.historyComboBox.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.historyComboBox.setDuplicatesEnabled(True)
        self.historyComboBox.setObjectName(_fromUtf8("historyComboBox"))
        self.verticalLayout_groupBox.addWidget(self.historyComboBox)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(param_file)
        QtCore.QMetaObject.connectSlotsByName(param_file)

    def retranslateUi(self, param_file):
        param_file.setWindowTitle(QtGui.QApplication.translate("param_file", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("param_file", "This is the parameter name", None, QtGui.QApplication.UnicodeUTF8))
        self.fileButton.setText(QtGui.QApplication.translate("param_file", "Select file", None, QtGui.QApplication.UnicodeUTF8))

