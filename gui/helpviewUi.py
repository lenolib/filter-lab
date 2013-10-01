# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'helpview.ui'
#
# Created: Tue Oct 18 14:54:42 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_helpView(object):
    def setupUi(self, helpView):
        helpView.setObjectName(_fromUtf8("helpView"))
        helpView.resize(576, 373)
        helpView.setWindowTitle(QtGui.QApplication.translate("helpView", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout = QtGui.QGridLayout(helpView)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.textBrowser = QtGui.QTextBrowser(helpView)
        self.textBrowser.setMinimumSize(QtCore.QSize(558, 355))
        self.textBrowser.setHtml(QtGui.QApplication.translate("helpView", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">Add </span><span style=\" font-size:10pt;\">filters to the scene by double clicking them in either of the two lists.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">Select </span><span style=\" font-size:10pt;\">multiple filters by dragging over them with the right mouse button or click on them while holding down the \'Ctrl\' key.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">Save</span><span style=\" font-size:10pt;\"> a collection of connected filters by selecting them and chose \'save from the File menu. Make sure the collection of filters does not have connections to filters outside of the selection.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">Display</span><span style=\" font-size:10pt;\"> two or more pictures at the same time in the viewer window by right-clicking on two stacked tabs. It is also possible to choose &quot;New Tab View&quot; from the menu and simply drag a displayed image to the newly created empty Tab View in the viewer window.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">Pan</span><span style=\" font-size:10pt;\"> the filter scene by left clicking somewhere on the white background and drag.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">Hold</span><span style=\" font-size:10pt;\"> the mouse over a filter for a second to display some data about the images that the filter has processed, such as resolution, pixel data type, and maximum and minimum pixel values.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 1)

        self.retranslateUi(helpView)
        QtCore.QMetaObject.connectSlotsByName(helpView)

    def retranslateUi(self, helpView):
        pass

