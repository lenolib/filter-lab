# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'viewer.ui'
#
# Created: Mon Oct 03 01:56:56 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Viewer_Window(object):
    def setupUi(self, Viewer_Window):
        Viewer_Window.setObjectName(_fromUtf8("Viewer_Window"))
        Viewer_Window.resize(535, 435)
        self.gridLayout_2 = QtGui.QGridLayout(Viewer_Window)
        self.gridLayout_2.setMargin(2)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.scrollArea = QtGui.QScrollArea(Viewer_Window)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 527, 427))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(4)
        self.grid.setObjectName(_fromUtf8("grid"))
        self.gridLayout.addLayout(self.grid, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(Viewer_Window)
        QtCore.QMetaObject.connectSlotsByName(Viewer_Window)

    def retranslateUi(self, Viewer_Window):
        Viewer_Window.setWindowTitle(QtGui.QApplication.translate("Viewer_Window", "Viewer", None, QtGui.QApplication.UnicodeUTF8))

