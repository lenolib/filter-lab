# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'filterframe.ui'
#
# Created: Mon Oct 03 01:56:42 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_filterframe(object):
    def setupUi(self, filterframe):
        filterframe.setObjectName(_fromUtf8("filterframe"))
        filterframe.resize(78, 18)
        filterframe.setAutoFillBackground(True)
        filterframe.setFrameShape(QtGui.QFrame.NoFrame)
        filterframe.setFrameShadow(QtGui.QFrame.Plain)
        filterframe.setLineWidth(0)
        self.verticalLayout = QtGui.QVBoxLayout(filterframe)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.filtername_label = QtGui.QLabel(filterframe)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filtername_label.sizePolicy().hasHeightForWidth())
        self.filtername_label.setSizePolicy(sizePolicy)
        self.filtername_label.setAlignment(QtCore.Qt.AlignCenter)
        self.filtername_label.setWordWrap(True)
        self.filtername_label.setObjectName(_fromUtf8("filtername_label"))
        self.verticalLayout.addWidget(self.filtername_label)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout_outputs = QtGui.QVBoxLayout()
        self.verticalLayout_outputs.setSpacing(1)
        self.verticalLayout_outputs.setObjectName(_fromUtf8("verticalLayout_outputs"))
        self.gridLayout.addLayout(self.verticalLayout_outputs, 0, 1, 1, 1)
        self.verticalLayout_inputs = QtGui.QVBoxLayout()
        self.verticalLayout_inputs.setSpacing(1)
        self.verticalLayout_inputs.setObjectName(_fromUtf8("verticalLayout_inputs"))
        self.gridLayout.addLayout(self.verticalLayout_inputs, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(filterframe)
        QtCore.QMetaObject.connectSlotsByName(filterframe)

    def retranslateUi(self, filterframe):
        filterframe.setWindowTitle(QtGui.QApplication.translate("filterframe", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.filtername_label.setText(QtGui.QApplication.translate("filterframe", "Name", None, QtGui.QApplication.UnicodeUTF8))

