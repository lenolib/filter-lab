# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'param_variable.ui'
#
# Created: Mon Oct 10 23:35:38 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_param_variable(object):
    def setupUi(self, param_variable):
        param_variable.setObjectName(_fromUtf8("param_variable"))
        param_variable.resize(214, 75)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(param_variable.sizePolicy().hasHeightForWidth())
        param_variable.setSizePolicy(sizePolicy)
        param_variable.setMinimumSize(QtCore.QSize(214, 0))
        param_variable.setWindowTitle(QtGui.QApplication.translate("param_variable", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout = QtGui.QVBoxLayout(param_variable)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(param_variable)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox.setTitle(QtGui.QApplication.translate("param_variable", "This is the parameter name", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_groupBox = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_groupBox.setSpacing(1)
        self.verticalLayout_groupBox.setContentsMargins(2, 0, 2, 2)
        self.verticalLayout_groupBox.setObjectName(_fromUtf8("verticalLayout_groupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.min_label = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.min_label.sizePolicy().hasHeightForWidth())
        self.min_label.setSizePolicy(sizePolicy)
        self.min_label.setText(QtGui.QApplication.translate("param_variable", "Slider min", None, QtGui.QApplication.UnicodeUTF8))
        self.min_label.setAlignment(QtCore.Qt.AlignCenter)
        self.min_label.setObjectName(_fromUtf8("min_label"))
        self.verticalLayout_2.addWidget(self.min_label)
        self.doubleSpinBoxMin = QtGui.QDoubleSpinBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBoxMin.sizePolicy().hasHeightForWidth())
        self.doubleSpinBoxMin.setSizePolicy(sizePolicy)
        self.doubleSpinBoxMin.setMinimumSize(QtCore.QSize(62, 0))
        self.doubleSpinBoxMin.setFrame(True)
        self.doubleSpinBoxMin.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxMin.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.doubleSpinBoxMin.setKeyboardTracking(False)
        self.doubleSpinBoxMin.setPrefix(_fromUtf8(""))
        self.doubleSpinBoxMin.setDecimals(2)
        self.doubleSpinBoxMin.setMinimum(-99999.99)
        self.doubleSpinBoxMin.setMaximum(99999.99)
        self.doubleSpinBoxMin.setSingleStep(0.01)
        self.doubleSpinBoxMin.setProperty("value", -88888.0)
        self.doubleSpinBoxMin.setObjectName(_fromUtf8("doubleSpinBoxMin"))
        self.verticalLayout_2.addWidget(self.doubleSpinBoxMin)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        spacerItem = QtGui.QSpacerItem(0, 10, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.current_label = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.current_label.sizePolicy().hasHeightForWidth())
        self.current_label.setSizePolicy(sizePolicy)
        self.current_label.setText(QtGui.QApplication.translate("param_variable", "Value", None, QtGui.QApplication.UnicodeUTF8))
        self.current_label.setAlignment(QtCore.Qt.AlignCenter)
        self.current_label.setObjectName(_fromUtf8("current_label"))
        self.verticalLayout_3.addWidget(self.current_label)
        self.doubleSpinBoxCurrent = QtGui.QDoubleSpinBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBoxCurrent.sizePolicy().hasHeightForWidth())
        self.doubleSpinBoxCurrent.setSizePolicy(sizePolicy)
        self.doubleSpinBoxCurrent.setMinimumSize(QtCore.QSize(74, 0))
        self.doubleSpinBoxCurrent.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxCurrent.setKeyboardTracking(False)
        self.doubleSpinBoxCurrent.setMinimum(-99999.99)
        self.doubleSpinBoxCurrent.setMaximum(99999.99)
        self.doubleSpinBoxCurrent.setSingleStep(0.01)
        self.doubleSpinBoxCurrent.setProperty("value", -88888.0)
        self.doubleSpinBoxCurrent.setObjectName(_fromUtf8("doubleSpinBoxCurrent"))
        self.verticalLayout_3.addWidget(self.doubleSpinBoxCurrent)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        spacerItem1 = QtGui.QSpacerItem(0, 10, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.max_label = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.max_label.sizePolicy().hasHeightForWidth())
        self.max_label.setSizePolicy(sizePolicy)
        self.max_label.setText(QtGui.QApplication.translate("param_variable", "Slider max", None, QtGui.QApplication.UnicodeUTF8))
        self.max_label.setAlignment(QtCore.Qt.AlignCenter)
        self.max_label.setObjectName(_fromUtf8("max_label"))
        self.verticalLayout_4.addWidget(self.max_label)
        self.doubleSpinBoxMax = QtGui.QDoubleSpinBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBoxMax.sizePolicy().hasHeightForWidth())
        self.doubleSpinBoxMax.setSizePolicy(sizePolicy)
        self.doubleSpinBoxMax.setMinimumSize(QtCore.QSize(62, 0))
        self.doubleSpinBoxMax.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxMax.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.doubleSpinBoxMax.setKeyboardTracking(False)
        self.doubleSpinBoxMax.setMinimum(-99999.99)
        self.doubleSpinBoxMax.setMaximum(99999.99)
        self.doubleSpinBoxMax.setSingleStep(0.01)
        self.doubleSpinBoxMax.setProperty("value", -88888.0)
        self.doubleSpinBoxMax.setObjectName(_fromUtf8("doubleSpinBoxMax"))
        self.verticalLayout_4.addWidget(self.doubleSpinBoxMax)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(3, 1)
        self.verticalLayout_groupBox.addLayout(self.horizontalLayout)
        self.valueSlider = QtGui.QSlider(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.valueSlider.sizePolicy().hasHeightForWidth())
        self.valueSlider.setSizePolicy(sizePolicy)
        self.valueSlider.setMinimum(-9999999)
        self.valueSlider.setMaximum(99999)
        self.valueSlider.setSingleStep(2)
        self.valueSlider.setPageStep(12)
        self.valueSlider.setTracking(True)
        self.valueSlider.setOrientation(QtCore.Qt.Horizontal)
        self.valueSlider.setInvertedAppearance(False)
        self.valueSlider.setInvertedControls(False)
        self.valueSlider.setTickPosition(QtGui.QSlider.NoTicks)
        self.valueSlider.setObjectName(_fromUtf8("valueSlider"))
        self.verticalLayout_groupBox.addWidget(self.valueSlider)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(param_variable)
        QtCore.QMetaObject.connectSlotsByName(param_variable)

    def retranslateUi(self, param_variable):
        pass
