# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'paramWidget.ui'
#
# Created: Mon Oct 03 01:59:22 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_paramWidget(object):
    def setupUi(self, paramWidget):
        paramWidget.setObjectName(_fromUtf8("paramWidget"))
        paramWidget.resize(250, 164)
        self.verticalLayout = QtGui.QVBoxLayout(paramWidget)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label = QtGui.QLabel(paramWidget)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.filtername_lineEdit = QtGui.QLineEdit(paramWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filtername_lineEdit.sizePolicy().hasHeightForWidth())
        self.filtername_lineEdit.setSizePolicy(sizePolicy)
        self.filtername_lineEdit.setObjectName(_fromUtf8("filtername_lineEdit"))
        self.verticalLayout_2.addWidget(self.filtername_lineEdit)
        self.label_2 = QtGui.QLabel(paramWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.label_2)
        self.description_plainTextEdit = QtGui.QPlainTextEdit(paramWidget)
        self.description_plainTextEdit.setMaximumSize(QtCore.QSize(16777215, 80))
        self.description_plainTextEdit.setObjectName(_fromUtf8("description_plainTextEdit"))
        self.verticalLayout_2.addWidget(self.description_plainTextEdit)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        spacerItem = QtGui.QSpacerItem(10, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(paramWidget)
        QtCore.QMetaObject.connectSlotsByName(paramWidget)

    def retranslateUi(self, paramWidget):
        paramWidget.setWindowTitle(QtGui.QApplication.translate("paramWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("paramWidget", "Filter name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("paramWidget", "Filter description", None, QtGui.QApplication.UnicodeUTF8))

