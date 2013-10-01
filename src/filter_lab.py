# -*- coding: utf-8 -*-    

##Development notes (To-do list):
#Bug: At times when paused, a slider change might not result in the image being updated.
#Bug -ignored: Loop connections possible ->fix: check if the current filter is connected to any of the child's children's children
#Bug: Using slow filters (above 1 second in processing) seems to lock up the gui. \
#    Some mutex thing? No, something to do with the call to c-functions, as python code does not produce the same lockups
#Feature request: Clicking on empty tab views deletes them.
#Feature request: Make filters right-clickable/have context menu
#Feature request: When dragging and dropping views, make them sit on top in their new tab view.
#Feature request: Use the networkx graph library to layout graphs pretty.
#Feature request: Make each filter have it's own thread.
#Feature request: Convert code to exception throwing and catching style instead of return codes style.
 
from __future__ import division, absolute_import
import os,sys
import time
import save_load 
import numpy
import random
import matplotlib
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtCore import (QThread,QWaitCondition,QMutex,pyqtSignal,Qt,QObject,
                          QPoint,QPointF,QMimeData,QLineF,QEvent, pyqtSlot)
from PyQt4.QtGui import (QAction,QKeySequence,QMenu,QFileDialog,
                         QGraphicsView,QWidget,QRadioButton,QTabWidget,
                         QGraphicsScene,QDrag,QGraphicsProxyWidget,QPen,QToolTip,
                         QGraphicsItem,QGraphicsLineItem,QApplication,QLabel,
                         QTreeWidgetItem,QCursor,QPixmap,QImage,QFrame,QVBoxLayout,
                         QListWidget)
from PyQt4 import Qsci
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg
from gui import *
 
import filters_package
from filters_package.filter_base import (disconnect_filters, connect_filters, 
                                    remove_filter, autoConnectPair, 
                                    insertFilter, arr2pixmap, AbortException,
                                    SUCCESS, FAIL, OUTPUT_FILTER, 
                                    SOURCE_FILTER, STANDARD_FILTER)

VERSION = "0.3"

#For determining and setting the layouts of the radiobutton connector sites.
OUTPUT_LAYOUT = QtCore.Qt.RightToLeft  
INPUT_LAYOUT = QtCore.Qt.LeftToRight

#Contants for determining the state of the worker thread
LOOP = 'Loop'
NEXT = 'Next'
PAUSE = 'Pause' 
AGAIN = 'Again'
UPDATE = 'Update'

##For the purpose of debugging function calls 
#def p_rents():
#    import inspect
#    print " << ".join([i[3] for i in inspect.stack()[1:-4]])


def getFilterClass(filter_class_name):
    """Return the class object corresponding to the class name from the
    filter class name dictionary. 
    Simply serves a cosmetic purpose in the code.
    
    """
    return filters_package.filter_class_name_dict[filter_class_name]
        
def is_deleted(obj):
    """Check if a (Qt)object exists or is deleted."""
    import sip
    try:
        sip.unwrapinstance(obj)
    except RuntimeError:
        return True
    return False

def makeCross(side=30):
    cross = numpy.ones((side,side),dtype='uint8')*255
    for i in xrange(side):          
        cross[i,i] = 0
        cross[side-i-1,i] = 0
    return cross


class WorkerThread(QThread):
    """Thread that processes all filters, that is, calls filters' run_filter()-functions.
    
    Description of the class variables:
    mutex -- Mutex used for locking filter variables 
    mutex2 -- Mutex used for locking the thread's wait-condition
    condition -- The thread's wait-condition
    exiting -- Variable that keeps the thread's run-loop alive
    activeState -- Variable that controls thread's run-loop
    do_restart -- 
    filters -- List of filters in the scene
    
    """
    status_update = pyqtSignal(str)
    update_view = pyqtSignal()
    time_calc = pyqtSignal(dict)
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.mutex = QMutex()
        self.mutex2 = QMutex()
        self.condition = QWaitCondition()
        self.exiting = False
        self.activeState = LOOP
        self.do_restart = False
        self.filters = []
        self.start()

    def add_filter(self,fltr):
        """Add a filter to the thread's list of filters in the scene."""
        self.mutex.lock()
        self.filters.append(fltr)
        self.mutex.unlock()
    
    def setParamContent(self,fltr,param_name,content):
        """Lock mutex and call the filter's own setParamContent-function"""
        self.mutex.lock()
        fltr.setParamContent(param_name,content)
        self.mutex.unlock()
        
    def remove_filter(self, fltr):
        """Lock mutex and call its own remove-function."""
        self.mutex.lock()
        self.filters.remove(fltr)
        remove_filter(fltr)
        self.mutex.unlock()
        self.wake_and_activate()
        
    def disconnect_filters(self, parent, child, outputs, inputs):
        """Lock mutex and disconnect filters. Return result."""
        self.mutex.lock()
        res = disconnect_filters(parent, child, outputs, inputs)
        self.mutex.unlock()
        if res is SUCCESS:
            self.wake_and_activate()
        return res
        
    def connect_filters(self, parent, child, outputs, inputs):
        """Lock mutex and connect filters. Return result"""
        self.mutex.lock()
        res = connect_filters(parent, child, outputs, inputs)
        self.mutex.unlock()
        if res is SUCCESS:
            self.wake_and_activate()
        return res
    
    def param_was_changed_slot(self, fltr, param_name, content):
        self.setParamContent(fltr, param_name, content)
        fltr.notify_children()
        if self.activeState == PAUSE:
            try: fltr.processParams()
            except AbortException: pass
            except Exception,e: 
                print "\
In '%s': An exception in 'processParams()' was caught safely. Exception was:\n" %fltr.name,e
        self.wake_and_activate()
    
    def __del__(self):
        """End thread before deleting. Not certain if it's working properly"""
        self.exiting = True        
        while self.isRunning() == True:
            self.mutex2.lock()
            self.condition.wait(self.mutex2,20)
            self.mutex2.unlock()
    
    def setActiveState(self,state):
        """Set 'activeState' to 'state', and pause all filters if 
        'state' is PAUSE"""
        self.mutex.lock()
        if state == PAUSE:# and self.activeState != PAUSE:
            self.status_update.emit("Status: Pausing...")
            for fltr in self.filters: fltr.setAbort(True) 
        self.activeState = state
        self.mutex.unlock()
    
    def pause_resume(self):
        """Pause or resume the worker thread depending on the activeState variable."""
        if self.activeState in [LOOP,AGAIN,NEXT,UPDATE]:
            self.setActiveState(PAUSE)
        else:
            self.setActiveState(LOOP)   
            self.status_update.emit("Status: Running...")
            self.condition.wakeOne()
    
    def wake_and_activate(self):
        """Wake the thread and run it once without advancing the frame sequence."""
        if self.activeState == PAUSE:
            self.setActiveState(UPDATE)
        self.condition.wakeOne()        
    
    def restartInputsSLOT(self):
        """"""
        self.mutex.lock()
        self.do_restart = True
        self.mutex.unlock()
        if self.activeState == PAUSE:
            self.setActiveState(NEXT)
            self.wake_and_activate()

    def waitFPS(self, past_clocking, fps_limit):
        """Wait until the given frames-per-second has been achieved."""
        timing = time.clock()-past_clocking + 1e-9
        if 1/timing > fps_limit and fps_limit != 0:
            self.mutex2.lock()
            wait_time = int( (1/fps_limit-timing)*1000 ) 
            self.condition.wait(self.mutex2, wait_time)
            self.mutex2.unlock()
        
    def emitTimings(self):
        """Get timings from the filters and emit signal 'time_calc'"""
        timings = {}  
        for fltr in self.filters:                    
            if isinstance(fltr.time_consumption,basestring): #time_consumption has been set to "Failed" in fltr.
                timings[fltr] = fltr.time_consumption
            else:
                timings[fltr] = fltr.time_consumption
        self.time_calc.emit(timings) 
        
    def run(self):
        """Process the filters in the scene.
        
        For every loop this function updates the filters, which means that it notifies
        every filter of type SOURCE_FILTER in the scene that it should process 
        the next image, and every filters of type OUTPUT_FILTER in the scene that 
        it should run (ask its parent filters for output images), and then signals 
        that the display view should be updated.
        
        The tot_input_res and tot_disp_res variables are used to signal if any of 
        the input or output type filters did anything useful. If they all did NOT, 
        the thread will pause.
        
        AGAIN - Do NOT run the filters of type SOURCE_FILTER in the scene, 
                i.e. don't progress to the next frame, but notify all the their 
                children that one of their parents have changed,
                even though that is not really the case, 
                and that they should re-process the next time requested to (updated=False)
        LOOP - Run the filters of type SOURCE_FILTER and thus progress to the next frame.
        NEXT - Run the filters of type SOURCE_FILTER and thus progress to the next frame, 
               and then pause the thread.
        UPDATE - Run the input filters only if they have been changed (=not updated).
        PAUSE - Pause the thread.
        
        """
        
        while self.exiting == False:
            if self.activeState in (LOOP,NEXT,AGAIN,UPDATE):
                begun_t = time.clock()
                if self.activeState != LOOP:
                    self.status_update.emit("Status: Working...")
                tot_input_res = 'rest'
                tot_disp_res = 'rest'
                do_restart_copy = self.do_restart
                
                for fltr in self.filters:
                    if fltr.filtertype == SOURCE_FILTER and not fltr.disabled:    
                        if do_restart_copy == True:
                            fltr.restart()
                        if self.activeState == AGAIN:
                            fltr.notify_children()
                            res = SUCCESS                        
                        elif self.activeState in (LOOP,NEXT):
                            res = fltr.run_filter()
                            fltr.notify_children()
                        elif self.activeState == UPDATE:
                            if not fltr.updated:
                                res = fltr.run_filter()
                                fltr.notify_children()
                            else: 
                                res = FAIL #Don't want the thread to continue
                        if res is SUCCESS:
                            tot_input_res = 'process next'
                if do_restart_copy == True: 
                    self.mutex.lock()
                    self.do_restart = False
                    self.mutex.unlock()
                for fltr in self.filters:
                    if fltr.filtertype == OUTPUT_FILTER and not fltr.updated:
#                            fltr.visible == True and fltr.updated == False and (self.parent() is not None and self.parent().viewer.isVisible() == True) ):                        
                        res = fltr.run_filter()
                        if res is SUCCESS:
                            tot_disp_res = 'process next'
                    elif fltr.filtertype == OUTPUT_FILTER and not fltr.updated:
                        fltr.run_filter()                        
                self.update_view.emit()                
                if tot_input_res == 'rest' and tot_disp_res == 'rest':
                    self.setActiveState(PAUSE)                    
                
                self.emitTimings()
                self.waitFPS(begun_t, self.parent().ui.fps_limit_spin.value())
                timing = time.clock()-begun_t    
                         
                if self.activeState in [NEXT,AGAIN,UPDATE]:
                    self.setActiveState(PAUSE)
                    self.status_update.emit("Status: Paused. Last run took: %.2f s" %timing)
                elif self.activeState == PAUSE:
                    self.status_update.emit("Status: Paused")
                elif self.activeState == LOOP:
                    self.status_update.emit("Status: Running at: %.2f fps (%.2f s)..." %(1/timing, timing))    
                
                for fltr in self.filters: fltr.setAbort(False)                             
            elif self.activeState == PAUSE:
                self.mutex2.lock()
                self.condition.wait(self.mutex2)
                self.mutex2.unlock()
             
        for fltr in self.filters:
#            if isinstance(fltr, getFilterClass("Input_filter") ):
#                fltr.deleteCaptures() #Superfluous
            del fltr
                

class Controls(QtGui.QMainWindow):
    """Class that handles the GUI and owns the worker-thread.
    
    
    Description of the class variables, excepting most of the GUI-widgets:
    ui -- This contains the 'controls'-window widgets and GUI-elements as specified
          in the file 'controlsUi.py'.
    filter_path -- Path to folder in which to look for saved filters to display 
                   in the 'Saved filters'-list.
    last_selected -- Contains the FilterProxyItem which is selected in the scene, 
                     or was last selected. Used to display it's parameters in the
                     parameters view area.
    viewer -- This is the QWidget-object that handles the display of the output images
              on screen.
    filter_scene -- This is the QGraphicsScene-object that contains the FilterProxyItems (the graphical 
                    parts of the filters).
    worker_thread -- This is the thread that processes the filters alongside the GUI-thread.
    
    """
    restart_inputs_sig = pyqtSignal()
    quit_sig = pyqtSignal()
    ignoreSceneSelection = False

    def __init__(self):
        """Sets up and displays all the graphical elements and creates a worker-thread."""
        QtGui.QMainWindow.__init__(self)
        self.ui=Ui_Controls_MainWindow()                
        self.ui.setupUi(self)
        self.setWindowTitle("Image Filter Lab version %s - Controls" %VERSION)        
        self.resize(950,650) 
        self.ui.splitter_3.setStretchFactor(0,5)
        self.ui.splitter_3.setStretchFactor(1,2)
        self.ui.splitter_2.setStretchFactor(0,1)
        self.ui.splitter_2.setStretchFactor(1,6)
        self.last_selected = None        
        self.filter_path = os.path.join(os.path.dirname(__file__),'saved_filters').replace('\\','/')
        self.displaySavedFilters(self.filter_path)
        self.ui.filter_list.setMouseTracking(True)
        self.ui.filter_list.setFocus()            
        self.setupFilterList()
        self.viewer = Viewer(self)
        self.viewer.show()
        self.helpview = HelpView(self)   
        self.helpview.setWindowTitle("Usage instructions")
        self.ui.tree_filters_in_scene.resizeColumnToContents(0)     
        self.ui.tree_filters_in_scene.setSortingEnabled(True)
        self.ui.tree_filters_in_scene.sortByColumn(1, Qt.AscendingOrder)
        self.filter_scene = FilterGraphicsScene(self.viewer)
        self.ui.addedFilters_view.setScene(self.filter_scene)
        self.ui.addedFilters_view.show()   
        self.setupSignalsSlots()
        self.setupActionsMenus()
        self.ui.filter_list.keyPressEvent = self.filter_list_keyPressEvent  
        self.ui.saved_filter_list.keyPressEvent = self.saved_filter_list_keyPressEvent
        
    def filter_list_keyPressEvent(self,keyEvent):
        if keyEvent.key() == Qt.Key_Return: 
                self.actions[self.ActAddFilter].trigger()
        else: 
                QListWidget.keyPressEvent(self.ui.filter_list,keyEvent)
    def saved_filter_list_keyPressEvent(self,keyEvent):
        if keyEvent.key() == Qt.Key_Return: 
                self.actions[self.ActAddFilter].trigger()
        else:   QListWidget.keyPressEvent(self.ui.saved_filter_list,keyEvent)


    def setupFilterList(self):
        """Add entries to the new filter list by going through the
        dictionary with filter classes."""
        for filter_name in sorted(filters_package.filter_given_name_dict, reverse=True):
            filter_class = filters_package.filter_given_name_dict[filter_name]    
            tmp_instance = filter_class()
            if tmp_instance is None:
                continue
            else:
                tooltip = tmp_instance.getWrappedDescription()
                if tooltip == "":
                    tooltip = "[No description provided]"            
                self.ui.filter_list.insertItem(0,tmp_instance.name)
                self.ui.filter_list.item(0).setToolTip(tooltip)
                del tmp_instance
    
    def createAction( self, text, slot=None, shortcut=None):
        action = QAction(text,self)
        if slot is not None: action.triggered.connect(slot)
        if shortcut is not None: action.setShortcut(shortcut)
        return action
    
    def setupSignalsSlots(self):
        self.worker_thread = WorkerThread(parent=self)
        pairs_to_connect = [ 
            (self.filter_scene.scene_update_sig,  self.viewer.update_all),
            (self.filter_scene.selectionChanged,  self.updateParamView),
            (self.filter_scene.selectionChanged,  self.updateTreeSelection),
            (self.worker_thread.update_view,      self.viewer.update_all),
            (self.worker_thread.time_calc,        self.updateTimings),        
            (self.filter_scene.remove_filter_sig, self.worker_thread.remove_filter),
            (self.filter_scene.remove_filter_sig, self.remove_tree_item),
            (self.filter_scene.param_changed_sig, self.worker_thread.param_was_changed_slot),
            (self.worker_thread.status_update,    self.ui.status_label.setText),        
            (self.restart_inputs_sig,             self.worker_thread.restartInputsSLOT) ]
        for pair in pairs_to_connect:
            pair[0].connect(pair[1])
            
    def setupActionsMenus(self):    
        self.ActFolderDiag = "Select filter folder..."
        self.ActSaveDiag = "Save filter..."
        self.ActLoadDiag = "Load filter..."
        self.ActQuit = "Quit"
        self.ActAutoConnect = "Auto-connect selected"
        self.ActInsert = "Insert between"
        self.ActLineUp = "Auto-arrange selected on line"
        self.ActCircleUp = "Auto-arrange selected on circle"
        self.ActOnTop = "Auto-arrange selected on top of each other"
        self.ActEnable = "Enable filter(s)"
        self.ActDisable = "Disable filter(s)"
        self.ActSlctAll = "Select all"
        self.ActAddFilter = "Add selected filter"
        self.ActDisconnect = "Disconnect filters"
        self.ActShowViewer = "Show viewer"
        self.ActViewerOnTop = "Viewer always on top"
        self.ActNewTabView = "New tab view"
        self.ActRemove = "Remove filter(s)"
        self.ActPause = "Pause"
        self.ActAgain = "Again"
        self.ActNext = "Next"
        self.ActRestart = "Restart"        
        self.ActHelp = "Help"
        
        
        ActFolderDiag = self.ActFolderDiag
        ActSaveDiag = self.ActSaveDiag
        ActLoadDiag = self.ActLoadDiag
        ActQuit = self.ActQuit
        ActAutoConnect = self.ActAutoConnect
        ActInsert = self.ActInsert
        ActLineUp = self.ActLineUp
        ActEnable = self.ActEnable
        ActDisable = self.ActDisable
        ActSlctAll = self.ActSlctAll
        ActAddFilter = self.ActAddFilter
        ActDisconnect = self.ActDisconnect
        ActShowViewer = self.ActShowViewer
        ActViewerOnTop = self.ActViewerOnTop
        ActNewTabView = self.ActNewTabView
        ActRemove = self.ActRemove
        ActPause = self.ActPause
        ActAgain = self.ActAgain
        ActNext = self.ActNext
        ActRestart = self.ActRestart        
        ActHelp = self.ActHelp
        ActCircleUp = self.ActCircleUp
        ActOnTop = self.ActOnTop
        
        actions_to_setup = {
            ActAddFilter : 
                dict(slot=self.addSelectedFilter),
            ActAgain : 
                dict( slot=self.doFrameAgain, shortcut=QKeySequence("Ctrl+2")),
            ActAutoConnect : 
                dict( slot=self.filter_scene.autoConnect, shortcut=QKeySequence("Ctrl+F")),
            ActDisconnect : 
                dict(slot=self.filter_scene.disconnectFilters, shortcut=QKeySequence("Ctrl+U")),
            ActDisable : 
                dict(slot=None),
            ActEnable : 
                dict(slot=None),
            ActHelp : 
                dict( slot=self.helpSLOT, shortcut=QKeySequence.HelpContents),
            ActInsert : 
                dict( slot=self.filter_scene.insertFilterSLOT, shortcut=QKeySequence("Ctrl+I")),
            ActLoadDiag : 
                dict( slot=self.loadFiltersDiagSLOT, shortcut=QKeySequence.Open),
            ActNext : 
                dict( slot=self.doNextFrame, shortcut=QKeySequence("Ctrl+3")),
            ActNewTabView : 
                dict( slot=self.viewer.addTabView, shortcut=QKeySequence.AddTab),
            ActRemove : 
                dict(slot=self.filter_scene.removeFilterProxyItems, shortcut=QKeySequence.Delete),
            ActPause : 
                dict( slot=self.worker_thread.pause_resume, shortcut=QKeySequence(Qt.Key_Space)),
            ActQuit : 
                dict( slot=self.quit_sig.emit, shortcut=QKeySequence.Quit),
            ActLineUp : 
                dict( slot=self.filter_scene.arrange_line ),
            ActCircleUp : 
                dict( slot=self.filter_scene.arrange_circle, shortcut=QKeySequence("Ctrl+L") ),
            ActOnTop : 
                dict( slot=self.filter_scene.arrange_concentrate ),
            ActRestart : 
                dict( slot=self.restart_inputs_sig.emit, shortcut=QKeySequence("Ctrl+4") ),
            ActShowViewer : 
                dict( slot=self.toggleViewer, shortcut=QKeySequence("Ctrl+D") ),
            ActSlctAll : 
                dict( slot=self.filter_scene.selectAllFilters, shortcut=QKeySequence.SelectAll ),
            ActFolderDiag : 
                dict(slot=self.filterFolderDiagSLOT),
            ActSaveDiag : 
                dict(slot=self.saveFiltersDiagSLOT, shortcut=QKeySequence.Save),
            ActViewerOnTop : 
                dict(slot=self.viewerOnTopChange)
            }
        self.actions = {}
        for k,v in actions_to_setup.iteritems():
            self.actions[k] = self.createAction(k,**v)
        
        pairs_to_connect = [
            (self.viewer.viewer_closing_sig, 
                self.actions[ActShowViewer].setChecked),  
            (self.viewer.viewer_showing_sig, 
                self.actions[ActShowViewer].setChecked),
            (self.actions[ActDisable].triggered, 
                self.filter_scene.disableFilterProxyItems),
            (self.actions[ActDisable].triggered, 
                self.updateTimings),
            (self.actions[ActEnable].triggered, 
                self.filter_scene.enableFilterProxyItems),
            (self.actions[ActEnable].triggered, 
                self.updateTimings),
            (self.ui.framePause.clicked, 
                self.actions[ActPause].trigger), 
            (self.ui.frameAgain.clicked, 
                self.actions[ActAgain].trigger),
            (self.ui.restartButton.clicked, 
                self.actions[ActRestart].trigger),
            (self.ui.frameNext.clicked, 
                self.actions[ActNext].trigger) ]
        for pair in pairs_to_connect:
            pair[0].connect(pair[1])
        
        self.actions[ActNewTabView].setShortcutContext(Qt.ApplicationShortcut)
        self.actions[ActLoadDiag].setShortcut(QKeySequence.Open)
        self.actions[ActShowViewer].setShortcutContext(Qt.ApplicationShortcut)
        self.actions[ActPause].setShortcutContext(Qt.ApplicationShortcut)
        self.actions[ActNext].setShortcutContext(Qt.ApplicationShortcut)
        self.actions[ActRestart].setShortcutContext(Qt.ApplicationShortcut)
        self.actions[ActAgain].setShortcutContext(Qt.ApplicationShortcut)
        self.actions[ActShowViewer].setCheckable(True)
        self.actions[ActShowViewer].setChecked(True)
        self.actions[ActAutoConnect].setToolTip("Attempt to connect the filters in the order of their right-left position.")
        
        self.actions[ActViewerOnTop].setCheckable(True)
#self.ActAddFilter.setShortcuts(["Return", "Enter"])
#self.ActAddFilter.setShortcutContext(Qt.WidgetShortcut)
        self.menuFile = QMenu("File")
        self.menuActions = QMenu("Actions")
        self.menuProcess = QMenu("Process")
        self.ui.menubar.addMenu(self.menuFile)
        self.ui.menubar.addMenu(self.menuActions)
        self.ui.menubar.addMenu(self.menuProcess)
        self.ui.menubar.addAction(self.actions[ActHelp])
        def dic_select(dic,keys): return [dic[key] for key in keys]
        self.menuFile.addActions(dic_select( self.actions,
                                             [ActFolderDiag,
                                              ActSaveDiag,
                                              ActLoadDiag,
                                              ActQuit]) )
        self.menuActions.addActions(dic_select( self.actions,
                                                [ActAutoConnect,
                                                 ActInsert,
                                                 ActLineUp,
                                                 ActCircleUp,
                                                 ActOnTop,
                                                 ActEnable,
                                                 ActDisable,
                                                 ActSlctAll,
                                                 ActAddFilter,
                                                 ActDisconnect,
                                                 ActShowViewer,
                                                 ActViewerOnTop,
                                                 ActNewTabView,
                                                 ActRemove]) )
        self.menuProcess.addActions(dic_select( self.actions,
                                                [ActPause,
                                                 ActAgain,
                                                 ActNext,
                                                 ActRestart]) )
        
    def closeEvent(self, event):
        self.viewer.hide()
        self.worker_thread.exiting = True
        self.worker_thread.wake_and_activate()
        while(self.worker_thread.isRunning()):
            pass
        QtGui.QMainWindow.closeEvent(self, event)
    
    def updateTimings(self, *args):
        """Update the times for the filters in the filter list. 
        A supplied argument with a dictionary with the filter instances and their
        time consumption is optional."""
        if len(args)>0 and isinstance(args[0],dict): timings = args[0]
        else: timings = None
        tot = 0
        for i in xrange(self.ui.tree_filters_in_scene.topLevelItemCount()):            
            treeItem = self.ui.tree_filters_in_scene.topLevelItem(i)
            if timings is None:
                if treeItem.fltr.disabled: 
                    treeItem.setTime("Disabled")
                    continue
                else: 
                    timing = treeItem.fltr.time_consumption
            else:
                try:
                    if treeItem.fltr.disabled: timing = "Disabled"
                    else: timing = timings[treeItem.fltr]
                except KeyError:
    #                print "Could not find a filter in the tree list. Nothing to see, moving along..."
                    timing = "Failed"
            if isinstance(timing,basestring):
                treeItem.setTime(timing)
            else:
                treeItem.setTime("%.3f" %timing)
                tot+=timing
        self.ui.total_time_label.setText("Sum: %.2f s" %tot)
    
    def toggleViewer(self):
        if not self.viewer.isVisible():
            self.viewer.show()
        else:
            self.viewer.hide()            
    
    def viewerOnTopChange(self):
        was_visible = self.viewer.isVisible()
#        was_active = self.viewer.isActiveWindow()
        geo = self.viewer.geometry()
        if self.ActViewerOnTop.isChecked() == True:
            self.viewer.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        else:
            self.viewer.setWindowFlags(QtCore.Qt.Widget)
        if was_visible:
            self.viewer.setGeometry(geo)
            self.viewer.show()
            self.activateWindow()
            
    def helpSLOT(self):
        self.helpview.show()

    def doNextFrame(self):
        if self.worker_thread.activeState == PAUSE:
            self.worker_thread.setActiveState(NEXT)
            self.worker_thread.condition.wakeOne()
    
    def doFrameAgain(self):
        if self.worker_thread.activeState == PAUSE:
            self.worker_thread.setActiveState(AGAIN)
            self.worker_thread.condition.wakeOne()

    def filterFolderDiagSLOT(self):
        fileDialog = QFileDialog()
        fileDialog.setFileMode(QFileDialog.DirectoryOnly)
#        fileDialog.setOptions(QFileDialog.ShowDirsOnly)
        fileDialog.setViewMode(QFileDialog.Detail)
        fileDialog.setNameFilter("Python .py files (*.py)")
        folderNames = []
        if (fileDialog.exec_()):
            folderNames = fileDialog.selectedFiles()
        if folderNames != []:
            self.displaySavedFilters( unicode(folderNames[0]).replace('\\','/') )
        
    def displaySavedFilters(self,path):
        """Load saved filters from a folder and display them in the 'Saved filters'-list."""
        path = unicode(path).replace('\\','/')
        contents = os.listdir(path)
        files = [elem for elem in contents if (os.path.isfile(os.path.join(path,elem)) 
                                               and elem.endswith('.py'))]   
        files.reverse()
        if files != []:
            self.ui.saved_filter_list.clear()
            for file_ in files:
                self.ui.saved_filter_list.insertItem(0,file_.replace('.py','')) 
            self.filter_path = path
        else:
            self.ui.saved_filter_list.clear()        
        
    def on_filter_list_doubleClicked(self):
        self.addListedNewFilter()
        
    def addSelectedFilter(self):
        if self.ui.filter_list.hasFocus():
            self.addListedNewFilter()
        elif self.ui.saved_filter_list.hasFocus():
            self.addListedSavedFilter()
       
    def addListedNewFilter(self):
        """Create a filter of the sort selected in the filter list view and add it to the scene."""
        selected_items = self.ui.filter_list.selectedItems()
        if len(selected_items) != 1:
            print 'Please select one filter in the list'
        else:
            filter_name = unicode( selected_items[0].text() )
            filter_class = filters_package.filter_given_name_dict[filter_name]
            new_filter = filter_class()
            if new_filter is not None:
                cur_filterNames = []
                name = new_filter.name
                for fltr in self.worker_thread.filters:
                    cur_filterNames.append(fltr.name)
                i = 2
                while name in cur_filterNames:
                    name = new_filter.name + ' #' + unicode(i)
                    i+=1
                new_filter.setName(name)
                self.addFilterProxyItem(new_filter)
            else: print "Warning: Could not create a filter instance"

    def saveFiltersDiagSLOT(self):
        """Display a save file dialog and save the selected filters in the scene."""
        if self.checkOutsideConnections() == True:
            print "Please remove all connectors to unselected filters before saving."
            return
        selectedFilters = []
        filter_positions = []
        for item in self.filter_scene.getSelectedFilterItems():
            if isinstance(item, FilterProxyItem):
                selectedFilters.append(item.fltr)
                filter_positions.append( (item.scenePos().x(), item.scenePos().y()) )
        if len(selectedFilters) == 0:
            print "To save some filters, first select them"
            return 
        else:
            fileDialog = QFileDialog()
            fileDialog.setAcceptMode(QFileDialog.AcceptSave)
            fileDialog.setFileMode(QFileDialog.AnyFile)
            fileDialog.setViewMode(QFileDialog.Detail)
            fileDialog.setNameFilter("Python .py files (*.py)")
            fileNames = []
            if (fileDialog.exec_()):
                fileNames = fileDialog.selectedFiles()
            if fileNames != []: 
                save_load.saveFilters(selectedFilters, 
                                      unicode(fileNames[0]),
                                      positions=filter_positions)
                self.displaySavedFilters(self.filter_path)
    
    def checkOutsideConnections(self):
        """Check if currently selected filters have connections to filter's not selected."""
        selected = self.filter_scene.selectedItems()
        for item in selected:
            for connector in item.connectorList:
                if (connector.itemA not in selected or
                    connector.itemB not in selected):
                    return True
        return False   
        
    def on_saved_filter_list_doubleClicked(self):
        self.addListedSavedFilter()

    def addListedSavedFilter(self):
        """Load the selected saved filter file and add it's contents to the scene."""
        selected_items = self.ui.saved_filter_list.selectedItems()
        if len(selected_items) != 1:
            print 'Please select one filter in the list'
            return None
        else:
            filename = unicode( selected_items[0].text() )
            self.loadFiltersFromFile(os.path.join(self.filter_path,filename+'.py'))
                            
    def loadFiltersDiagSLOT(self):
        """Load filters from a selected file and add them to the scene."""
        fileDialog = QFileDialog()
        fileDialog.setFileMode(QFileDialog.AnyFile)
        fileDialog.setViewMode(QFileDialog.Detail)
        fileDialog.setNameFilter
        fileNames = []
        if (fileDialog.exec_()):
            fileNames = fileDialog.selectedFiles()
        if fileNames: 
            self.loadFiltersFromFile(fileNames[0])
        
    def loadFiltersFromFile(self, filename):
        """Load saved filters in 'filename' and add them to the scene, 
        and/or add filter in 'filter_list."""
        filter_list, positions = save_load.loadFilters(filename)        
        self.addFilters(filter_list,positions=positions)
        
    def addFilters(self, filter_list, positions=[]):
        if len(positions) != len(filter_list): 
            positions += [None]*(len(filter_list)-len(positions))
        new_proxyItems = []
        for ind, fltr in enumerate(filter_list):
#            QObject.__init__(fltr)
#            fltr.mutex = QMutex()
            new_proxy = self.addFilterProxyItem(fltr, position=positions[ind])
            new_proxyItems.append(new_proxy)
        self.filter_scene.restore_connectors(new_proxyItems)
        for new_proxy in new_proxyItems:
            new_proxy.setSelected(True)                                                        

    def addFilterProxyItem(self, fltr, position=None):
        """Create and set up the GUI part of the filter,add it to the scene, and return it."""
        paramWidget = ParamWidget(fltr)
        if fltr.filtertype == OUTPUT_FILTER:
            self.viewer.addDisplay(fltr)
        fltr.moveToThread(self.worker_thread)
        self.worker_thread.add_filter(fltr)  
        proxyItem = FilterProxyItem(fltr, paramWidget)
        treeItem = TreeFilterItem(fltr)
        self.ui.tree_filters_in_scene.addTopLevelItem(treeItem)
        paramWidget.filtername_changed_in_paramater_sig.connect(proxyItem.filtername_changed_slot)
        paramWidget.filtername_changed_in_paramater_sig.connect(treeItem.setName)
        paramWidget.filterdescription_changed_in_paramater_sig.connect(proxyItem.filterdescription_changed_slot)
        
        if position is not None:
            proxyItem.setPos( QPointF(position[0],position[1]) )
        else:
            best_pos = None
            best_rating = 0
            view = self.filter_scene.views()[0]
            for i in xrange(20):
                pos = self.calcRandPos(view.viewport().size(),
                                       proxyItem.size())
                rating = self.ratePosition(pos,proxyItem.size())
                if (fltr.filtertype == OUTPUT_FILTER and
                    view.mapFromScene(pos).x() < view.viewport().width()/2): 
                    continue
                if (fltr.filtertype == SOURCE_FILTER and
                    view.mapFromScene(pos).x() > view.viewport().width()/2):
                    continue
                if rating >= best_rating :
                    best_pos = pos
                    best_rating = rating
                    if best_rating == 8:
                        break    
            proxyItem.setPos( best_pos )
        self.filter_scene.addItem(proxyItem)  #Causes the application to crash when scene has been emptied. Worked around by not really removing any items, see FilterGraphicsScene.removeFilterProxyItems-function.      
        if fltr.disabled: proxyItem.disable()
        proxyItem.setFocusSelect()   
        return proxyItem    
    
    def ratePosition(self, NE, psize):
        "Return a score of 'pos' based on the intersection of other filters."
        rating = 0 
        N = QPointF(NE.x()+psize.width()/2, NE.y())
        W = QPointF(NE.x()+psize.width(), NE.y()+psize.height()/2)
        E = QPointF(NE.x(), NE.y()+psize.height()/2)
        S =  QPointF(NE.x()+psize.width()/2, NE.y()+psize.height())
        NW = QPointF(NE.x()+psize.width(), NE.y())
        SW = QPointF(NE.x()+psize.width(), NE.y()+psize.height())
        SE = QPointF(NE.x(), NE.y()+psize.height())
        positions = [N,W,E,S,NE,NW,SW,SE]
        for pos in positions:
            if self.filter_scene.itemAt(pos) == None:
                rating += 1
        return rating
    
    def calcRandPos(self, vsize, psize):        
        pos_in_view = QPointF(random.randint(20,int(vsize.width()-psize.width()-20)),
                              random.randint(20,int(vsize.height()-psize.height()-20)))
        return self.filter_scene.views()[0].mapToScene(QPoint(int(pos_in_view.x()),
                                                              int(pos_in_view.y())))                            

    def updateParamView(self):
        """Display or hide the parameter view for the selected filter in the scene."""
        if is_deleted(self.filter_scene): return
        selected_items = self.filter_scene.getSelectedFilterItems()                
        if len(selected_items) == 1:
            if selected_items[0].paramWidget is not None:
                if self.last_selected is None: pass
                else:                
                    self.last_selected.paramWidget = self.ui.paramView.takeWidget()
                self.ui.paramView.setWidget(selected_items[0].paramWidget)
                self.last_selected = selected_items[0]
            else:
                self.ui.paramView.widget().hide()
        else:
            self.ui.paramView.widget().hide()
    
    def on_tree_filters_in_scene_itemSelectionChanged(self):                
        slct_filts = [treeitem.fltr for treeitem in self.ui.tree_filters_in_scene.selectedItems()] 
        if not self.ignoreSceneSelection: 
            self.filter_scene.selectFilters(slct_filts)
        
    def updateTreeSelection(self):        
        """Select (exclusively) the treeitems corresponding to the filters in 'filter_list'"""
#        if self.ui.tree_filters_in_scene.hasFocus(): return
        self.ignoreSceneSelection = True    
        selected_filters = [prxy.fltr for prxy in self.filter_scene.getSelectedFilterItems()]
        for i in xrange(self.ui.tree_filters_in_scene.topLevelItemCount()):            
            treeitem = self.ui.tree_filters_in_scene.topLevelItem(i)
            if treeitem is not None:  #Un-motivated check, fixed an exception.
                if treeitem.fltr in selected_filters: treeitem.setSelected(True)
                else: treeitem.setSelected(False)
        self.ignoreSceneSelection = False
                    
    def remove_tree_item(self, fltr):
        for i in xrange(self.ui.tree_filters_in_scene.topLevelItemCount()):            
            treeitem = self.ui.tree_filters_in_scene.topLevelItem(i)
            if treeitem is not None:  #Un-motivated check, solved an error message.
                if treeitem.fltr == fltr:
                    self.ui.tree_filters_in_scene.takeTopLevelItem(i)
                    return

class HelpView(QtGui.QWidget):
    """A QWidget for displaying a window with basic usage instructions."""
    def __init__(self, parent):
        QtGui.QWidget.__init__(self)
        self.ui=Ui_helpView()
        self.ui.setupUi(self)

class ImageLabel(QtGui.QLabel):
    """The QLabel that holds a displayed image in the viewer window."""
    def __init__(self, outputfilter, parent=None):
        QtGui.QLabel.__init__(self, parent)
        self.outputfilter = outputfilter
        self.setAlignment(QtCore.Qt.AlignTop|QtCore.Qt.AlignLeft)
        self.no_image_cross = arr2pixmap(makeCross())
        self.updateImage()
    
    def updateImage(self):
        if (hasattr(self.outputfilter,'pixmap') and 
                isinstance(self.outputfilter.pixmap,QPixmap)): 
            self.setPixmap(self.outputfilter.pixmap)
        else:
            self.setPixmap(self.no_image_cross)
#        self.outputfilter.painted = True    


class Viewer(QtGui.QWidget):
    """A QWidget-inherited class that handles the display of result images on screen.
    
    This class keeps track of all the display filters added to the scene and
    displays their result images whenever the 'update_all' function is called.
    
    Description of the class variables:
    ui -- Contains the graphical Qt elements.
    displays -- Dictionary of display filters, with their 
                associated position numbers as keys.
    
    """
    viewer_closing_sig = pyqtSignal(object)
    viewer_showing_sig = pyqtSignal(object)
    def __init__(self, parent):
        QtGui.QWidget.__init__(self)
        self.ui=Ui_Viewer_Window()
        self.ui.setupUi(self)
        self.addTabView()
        self.gridTable = {1:(0,0),2:(0,1),3:(1,0),4:(1,1),
                          5:(0,2),6:(1,2),7:(2,0),8:(2,1),
                          9:(2,2),10:(0,3),11:(1,3),12:(2,3),
                          13:(3,0),14:(3,1),15:(3,2),16:(3,3)}
#        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    def moveToNewTabWidget(self, tabWidget):
        src = tabWidget
        src_ind = src.currentIndex()
        im_label = src.widget(src_ind)
        new_tabWidget = self.addTabView()
        if new_tabWidget is None:
            return
        new_tabWidget.addTab(im_label, src.tabText(src_ind))        
        im_label.outputfilter.filter_name_change_sig.connect(new_tabWidget.setFilterTabText)
#        src.removeTab(src_ind)
        self.tabCheck_and_Remove(src)
        
    def closeEvent(self, event):
        """Send signal informing that the user closed the viewer window."""
        self.viewer_closing_sig.emit(False)
        QWidget.closeEvent(self,event)
        
    def hideEvent(self,event):
        self.viewer_closing_sig.emit(False)
        QWidget.hideEvent(self,event)
    
    def showEvent(self, event):
        self.viewer_showing_sig.emit(True)
        self.update_all()
        QWidget.showEvent(self,event)
        
    
    def addTabView(self):
        """Add a new ViewTabWidget to the viewer, according to the order in 'gridTable'."""
        new_TabWidget = ViewTabWidget()
        count = self.ui.grid.count()
        if count == 0: 
            self.ui.grid.addWidget(new_TabWidget)
        elif count >= 16:
            print "Can not add more than 16 tab views."
            return None 
        else:
            row,col = self.gridTable[count+1]
            self.ui.grid.addWidget(new_TabWidget, row, col)
        new_TabWidget.tab_right_clicked_sig.connect(self.moveToNewTabWidget)
        new_TabWidget.tab_removed_sig.connect(self.tabCheck_and_Remove)
        return new_TabWidget
    
    def addDisplay(self, outputfilter):
        """Display the 'pixmap' attribute of 'outputfilter' inside a ImageLabel 
        in a tab in a tabwidget. If 'outputfilter' does not have a pixmap 
        attribute, as with the case for the save data filter, do nothing.
        
        Note that the pixmap in the filter will 
        not be displayed until 'update_all' is called
        on the image label container.
        
        """
        if not hasattr(outputfilter,'pixmap'):
            return
        grid_item = self.ui.grid.itemAt(0)
        if grid_item is None:
            self.addTabView()        
        tabW = self.ui.grid.itemAt(self.ui.grid.count()-1).widget()
        tabW.addTab(ImageLabel(outputfilter),outputfilter.name)
        outputfilter.filter_name_change_sig.connect(tabW.setFilterTabText)
        tabW.setCurrentIndex(tabW.count()-1)
    
    def tabCheck_and_Remove(self, tabW):
        """Remove tabwidget if it is empty, and reorganize the gridlayout."""
        if tabW.count() == 0:
            self.ui.grid.removeWidget(tabW)
            tabW.setParent(None)
            del tabW
            self.organizeGrid()
    
    def organizeGrid(self):
        """Remove empty spaces in the gridlayout by taking and adding all items."""
        old_items = []
        while self.ui.grid.count() != 0:
            old_items.append(self.ui.grid.itemAt(0))
            self.ui.grid.removeItem(self.ui.grid.itemAt(0))
        for i in range( len(old_items) ):
            row,col = self.gridTable[i+1]
            self.ui.grid.addItem(old_items[i], row, col)
            
    def removeDisplay(self, filter_to_remove):
        """Search for the filter in the tabs, and remove it.
        Raises an exception if the filter is not found.
        """
        for i_grid in range(self.ui.grid.count()):
            tabW = self.ui.grid.itemAt(i_grid).widget()
            for i_tab in range(tabW.count()):
                if tabW.widget(i_tab).outputfilter == filter_to_remove:
                    im_label = tabW.widget(i_tab)
                    tabW.removeTab(i_tab)
                    self.tabCheck_and_Remove(tabW)
                    del im_label
                    self.update()
                    return
        raise Exception("Could not find displayed filter in any tab.")

    def update_all(self):  
        """Update the image for all visible displays in the viewer."""
        for index in range(self.ui.grid.count()):
            for tab_ind in range(self.ui.grid.itemAt(index).widget().count()): 
                imLabel = self.ui.grid.itemAt(index).widget().widget(tab_ind)
                if imLabel is not None:  #hack-fix
                    imLabel.updateImage()

class ViewTabWidget(QTabWidget):
    """A straight QTabWidget class, extended to allow dragging and dropping of tabs."""
    tab_removed_sig = pyqtSignal(object)
    tab_right_clicked_sig = pyqtSignal(object)
    def __init__(self):
        QTabWidget.__init__(self)
        self.setMovable(True)
        self.setAcceptDrops(True)
        
    def mouseReleaseEvent(self, event):        
        if event.button() == Qt.RightButton and self.count() != 0:
            self.tab_right_clicked_sig.emit(self)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            QTabWidget.mousePressEvent(self, event)
            return
        if self.count() == 0:
            return
        drag = QDrag(self)
        mimedata = QMimeData()
        mimedata.setText("sample text")
        drag.setMimeData(mimedata)
        drag.exec_()
    
#    def currentChanged(self,index): #deprecated
#        """Set the displayfilters' 'visible' variables when changing tabs."""
#        if index != -1:
#            for i in range(self.count()):
#                self.widget(i).displayfilter.setVisible(False)
#            self.currentWidget().displayfilter.setVisible(True)
    
    def mouseMoveEvent(self,event):
        drag = QDrag(self.currentWidget())
        drag.setMimeData(QMimeData())
        drag.exec_()
        
    def dropEvent(self,event):
        """Add the dropped tab to a new tabwidget, and signal that a move has occured."""
        if isinstance(event.source(),ViewTabWidget) and event.source() != self:
            src = event.source()
            src_ind = src.currentIndex()
            im_label = src.widget(src_ind)
            self.addTab(im_label, src.tabText(src_ind))
            im_label.outputfilter.filter_name_change_sig.emit(self,self.setFilterTabText)
            self.tab_removed_sig.emit(src)
#            src.removeTab(src_ind)            
            event.acceptProposedAction()    
    
    def findFilter(self,fltr):
        """Return the tab number of a filter."""
        for i in range(self.count()):
            if self.widget(i).outputfilter == fltr:
                return i
        return None
            
    def setFilterTabText(self,fltr,name):
        """Will update the text on the tab containing the filter to 'name'."""
        index = self.findFilter(fltr)
        if index is not None:
            self.setTabText(index,name)
        else:
            pass

    def dragMoveEvent(self,event):
        if isinstance(event.source(),ViewTabWidget):
            event.acceptProposedAction()
            
    def dragEnterEvent(self,event):
        if isinstance(event.source(),ViewTabWidget):
            event.acceptProposedAction()
        

class FilterGraphicsScene(QtGui.QGraphicsScene):
    """Class that handles mouseclicks and connection, disconnection and removal of FilterProxyItems (the filters).
    
    Description of the class variables:
    line -- A variable that contains a Connector(QLine)-object when the user has clicked on
            some filter's input or output in the scene. Is normally None.
    viewer -- A reference to the viewer-instance, with the purpose to 
              be able to remove filters from it's 'displays'-dictionary.
                    
    """
    param_changed_sig = pyqtSignal(object, str,object)
    scene_update_sig = pyqtSignal()
    remove_filter_sig = pyqtSignal(object)
    def __init__(self, viewer):
        QtGui.QGraphicsScene.__init__(self)
        self.line = None
        self.viewer = viewer        
#        self.setSceneRect(-600,-600,1200,1200)'
        self.selectionChanged.connect(self.update_selected_slot)
        
#    def emit_param_update(self, filter, param_name, default):
#        """Emit a signal when a filter's parameter has changed"""
#        self.param_changed_sig.emit(filter, param_name, default)

    def update_selected_slot(self):
        """Mark the filter items in the scene as either selected or unselected."""
        if is_deleted(self): return
        new_selected = self.getSelectedFilterItems()
        for item in self.getFilterItems():
            if item in new_selected:
                item.mark_selected()                    
            else:
                item.mark_unselected()
        return
                
    def mouseMoveEvent(self, mouseEvent):
        """Draw a line if we are in 'line'-mode, that is, if self.line is not None, 
        else, pass along the mouseevent."""
        if self.line is not None:
            self.line.setLine( QLineF( self.line.line().p1(), mouseEvent.scenePos() ) )
        else:
            QGraphicsScene.mouseMoveEvent(self,mouseEvent)
        
    def mousePressEvent(self, mouseEvent):  
        """Handle all the different cases depending on where the user clicked in the scene."""    
#        self.debugConnectedness()  
        pos = mouseEvent.scenePos()        
        startItems = self.items(mouseEvent.scenePos())
        proxyItem = None
        proxyItems = []
        if self.line is not None:
            raise Exception('A previous error has occured. line has not been reset to None after mouse release')
        for item in startItems:  #Case of overlapping proxyitems not yet handled
            if isinstance(item,FilterProxyItem):
                proxyItems.append(item)
        if len(proxyItems) >= 1:
            proxyItem = proxyItems[0]
        if proxyItem is None:
            if mouseEvent.button() == Qt.LeftButton:                
                self.views()[0].setDragMode(QGraphicsView.ScrollHandDrag)
            if mouseEvent.button() == Qt.RightButton:
                self.setFocusItem(None)
                self.clearSelection()
                self.views()[0].setDragMode(QGraphicsView.RubberBandDrag)            
            QtGui.QGraphicsScene.mousePressEvent(self, mouseEvent)
            return
        else:
#            proxyItem.setFocusSelect()
            proxyPos = proxyItem.scenePos().toPoint()
            localPos = QPoint(pos.x() - proxyPos.x(), pos.y() - proxyPos.y())
            alienWidget = proxyItem.widget().childAt(localPos)
            if isinstance(alienWidget, QRadioButton):
                aliengeo = alienWidget.geometry()
                start_x = None
                start_y = aliengeo.y()+aliengeo.height()/2                
                if alienWidget.layoutDirection() == INPUT_LAYOUT:  #To check if alienwidget is input
                    input_connector = proxyItem.getInputRadioConnector(alienWidget)
                    if input_connector is None:  #Input radiobutton has no connection
                        start_x = aliengeo.x()+6
                    else:
                        self.line = input_connector
                        return
                else:
                    start_x = aliengeo.x()+aliengeo.width()-6
                startPos = QPointF(proxyItem.scenePos().x()+start_x, 
                                   proxyItem.scenePos().y()+start_y)
                if alienWidget.layoutDirection() == OUTPUT_LAYOUT:
                    self.line = Connector( QLineF(startPos, startPos), 
                                           itemA = proxyItem, 
                                           local_posA = QPointF(start_x,start_y) )
                elif alienWidget.layoutDirection() == INPUT_LAYOUT:
                    self.line = Connector( QLineF(startPos, startPos), #Sets the p1 position to an endpos
                                           itemB = proxyItem, 
                                           local_posB = QPointF(start_x,start_y) )      
                self.line.setPen(QPen())
                self.addItem(self.line)
                proxyItem.connectorList.append(self.line)
            else:
                QtGui.QGraphicsScene.mousePressEvent(self, mouseEvent)
    

    def cancel_Line(self):    
        """Disconnect filters if necessary, and remove the connector (line)."""
        if self.line.itemA is not None and self.line.itemB is not None:
            if self.line.disconnect_item_filters() is SUCCESS: pass                 
#            else: self.line = None
        self.line.disconnect_connector()
        self.removeItem(self.line)
        self.scene_update_sig.emit()
        self.line = None      
        return
    
    def mouseReleaseEvent(self, mouseEvent):
        """Handle all the different cases depending on where the user released the mouse."""
        if self.line is None:
            QGraphicsScene.mouseReleaseEvent(self, mouseEvent)
            self.views()[0].setDragMode(QGraphicsView.NoDrag)
            temp_selected = []
            for item in self.getFilterItems():                
                if item in self.getSelectedFilterItems():
                    temp_selected.append(item)
                else:
                    item.setUnselectedZValues()
            for item in temp_selected: item.setSelectedZValues() #To make sure connectors get right ZValues.                   
            return        
        else:
            pos = mouseEvent.scenePos()
            endItems = self.items(mouseEvent.scenePos())
            proxyItem = None
            proxyItems = []
            for item in endItems:  #Case of overlapping proxyitems not yet handled
                if isinstance(item,FilterProxyItem):
                    proxyItems.append(item)
            if len(proxyItems) >= 1:
                proxyItem = proxyItems[0]
            if proxyItem is None:
                self.cancel_Line()
                return                
            elif self.line.itemA is not None and self.line.itemB is not None:  
                #If we have grabbed and released an existing input 
                proxyPos = proxyItem.scenePos().toPoint()
                localPos = QPoint( pos.x() - proxyPos.x(), pos.y() - proxyPos.y() )
                alienWidget = proxyItem.widget().childAt(localPos)
                if isinstance(alienWidget, QRadioButton) == False:
                    self.cancel_Line()
                    return
                elif alienWidget.layoutDirection() == INPUT_LAYOUT:  #Releasing over an input radiobutton
                    if proxyItem == self.line.itemB:  #Released over same filter
                        if proxyItem.getInputRadioConnector(alienWidget) == self.line:  #Released over same input radiobutton
                            self.line.redraw()
                            self.line = None
                            return
                        else:  #Released on other input radiobutton 
                            if self.line.disconnect_item_filters() is SUCCESS: 
                                self.scene_update_sig.emit()
                            else: raise Exception("Couldn't disconnect filters to make a reconnection to same filters")
                            self.line.itemB.connectorList.remove(self.line)        
                            self.add_Line(proxyItem, mouseEvent.scenePos())
                            return 
                    elif proxyItem == self.line.itemA:  #Releasing over the parent item (invalid target)
                        self.cancel_Line()
                        return                        
                    else:  #Released over other filter than the two the filter is already connected to
                        if self.line.disconnect_item_filters() is SUCCESS: 
                            self.scene_update_sig.emit()
                        else: raise Exception("Couldn't disconnect filters")
                        self.line.itemB.connectorList.remove(self.line)
                        self.add_Line(proxyItem, mouseEvent.scenePos())
                        return                        
                else:  #Releasing over invalid target
                    self.cancel_Line()
                    return
            elif self.line.itemA is None and self.line.itemB is None:
                raise Exception("line should be none but is not.\
                                 It has no items at it's ends.") 
            else:  #If we have grabbed and released a new connection (either itemA or item B is None)
                if proxyItem == self.line.itemA or proxyItem == self.line.itemB: 
                    #Released over same filter (cannot connect filter to itself)
                    self.cancel_Line()
                    return
                else:
                    self.add_Line(proxyItem, mouseEvent.scenePos())
                    return           
         
    def add_Line(self, proxyItem, mouse_pos):
        """Check if the connection is allowed and connect_filters, else cancel. 
        Return SUCCESS or FAIL."""
        proxyPos = proxyItem.scenePos().toPoint()
        localPos = QPoint(mouse_pos.x() - proxyPos.x(), mouse_pos.y() - proxyPos.y())
        alienWidget = proxyItem.widget().childAt(localPos)
        if isinstance(alienWidget, QRadioButton):
            if self.line.itemA is None and alienWidget.layoutDirection() == INPUT_LAYOUT:
                self.cancel_Line()
                return FAIL                  
            elif self.line.itemB is None and alienWidget.layoutDirection() == OUTPUT_LAYOUT:
                self.cancel_Line()
                return FAIL                                               
            aliengeo = alienWidget.geometry()
            end_x = None
            end_y = aliengeo.y()+aliengeo.height()/2
            if alienWidget.layoutDirection() == OUTPUT_LAYOUT:
                end_x = aliengeo.x()+aliengeo.width()-6
            else:
                end_x = aliengeo.x()+6  
            endPos = QPointF(proxyItem.scenePos().x()+end_x, 
                             proxyItem.scenePos().y()+end_y)              
            newLine = QLineF( self.line.line().p1(), endPos )
            self.line.setLine(newLine) 
            if alienWidget.layoutDirection() == OUTPUT_LAYOUT:
                self.line.itemA = proxyItem
                self.line.local_posA = QPointF(end_x,end_y)
            elif alienWidget.layoutDirection() == INPUT_LAYOUT:
                self.line.itemB = proxyItem
                self.line.local_posB = QPointF(end_x,end_y)
            proxyItem.connectorList.append(self.line)
#            proxyItem.setFocusSelect()
            if self.line.connect_item_filters() is SUCCESS: 
                self.line.redraw()  #To fix that the line item stored in the connector has the wrong direction if line was drawn from itemB to itemA
                self.line = None
                self.scene_update_sig.emit()  #Redundant or necessary?
                return SUCCESS
            else:
                self.cancel_Line()
                return FAIL  
        else:
            self.cancel_Line()
#            print 'widget is not radiobutton'
            return FAIL
    
    def autoConnect(self):
        selected = self.getSelectedFilterItems() 
        selected.sort(key=lambda e: e.pos().x())
        ordered = selected
        for i in range(len(ordered)):
            if i == len(ordered)-1: break             
            filterA = ordered[i].fltr
            filterB = ordered[i+1].fltr
            res = autoConnectPair(filterA, filterB)
            if res is SUCCESS:
                self.restore_connectors([ordered[i],ordered[i+1]])
            else:
                print "Unable to connect '%s' (parent) to '%s' (child)" %(filterA.name,filterB.name)
#        self.scene_update_sig.emit()

    def selectAllFilters(self):
        self.clearSelection()
        for item in self.getFilterItems(): item.setSelected(True)
        
    def selectFilters(self,filter_list):
        """Select (exclusively) the filterproxyitems corresponding to the filters in 'filter_list'"""
        slctd = []
        for prxy in self.getFilterItems():
            if prxy.fltr in filter_list: slctd.append(prxy)
            else: 
                prxy.setSelected(False)
                prxy.setUnselectedZValues()
        for prxy in slctd:
            prxy.setSelected(True)
            prxy.setSelectedZValues()
    
    def arrange_line(self):
        "Put the selected filters on a line"
        selected = self.getSelectedFilterItems()
        if len(selected)<2: return 
        selected.sort(key=lambda e: e.x())
        ypos = selected[0].y() 
        nextX = selected[0].x()
        for item in selected:            
            item.setPos(QPointF(nextX,ypos))
            nextX = item.x() + item.geometry().width() +32
            
    def arrange_circle(self):
        "Put the selected filters on a circle"
        selected = self.getSelectedFilterItems()
        if len(selected)<2: return 
        selected.sort(key=lambda e: e.x())
        xmean = sum([i.x() for i in selected])/len(selected)
        ymean = sum([i.y() for i in selected])/len(selected)
        radius = len(selected)*100/numpy.pi/2
        for num,angle in enumerate(numpy.arange(0,2*numpy.pi, 2*numpy.pi/len(selected))):            
            xpos = xmean + radius*numpy.cos(angle)
            ypos = ymean + radius*numpy.sin(angle)
            selected[num].setPos(QPointF(xpos,ypos))
            
    def arrange_concentrate(self):
        "Put the selected filters on top of each other"
        selected = self.getSelectedFilterItems()
        if len(selected)<2: return 
        selected.sort(key=lambda e: e.x())
        ypos = selected[0].y() 
        nextX = selected[0].x()
        for item in selected:            
            item.setPos(QPointF(nextX,ypos))
            nextX = item.x() + 1
            
                         
    def insertFilterSLOT(self):
        selected = self.getSelectedFilterItems()
        if len(selected) != 3:
            print "Please select three filters; one to insert between the other two."
        else: 
            insertFilter(*[item.fltr for item in selected],
                         auto_identify=True)
            self.restore_connectors(selected, clear_first=True)

    def disconnectFilters(self):
        selected = self.getSelectedFilterItems()
        if len(selected) == 1:
            prxy = selected[0]
            con_filters = []
            for cnctr in prxy.connectorList:
                if cnctr.itemA != prxy and cnctr.itemA not in con_filters: 
                    con_filters.append(cnctr.itemA)
                if cnctr.itemB != prxy and cnctr.itemB not in con_filters: 
                    con_filters.append(cnctr.itemB)  
            for connected in con_filters:
                res = disconnect_filters(prxy.fltr, connected.fltr)
                if res is FAIL:
                    res = disconnect_filters(connected.fltr, prxy.fltr)
                if res is FAIL: raise Exception("Shouldn't get here")
            self.restore_connectors(con_filters+selected, clear_first=True)
        else:
            for i in range(len(selected)-1):
                prxy = selected[i]
                for temp in selected[i:]:
                    res = disconnect_filters(prxy.fltr, temp.fltr)
                    if res is FAIL:
                        disconnect_filters(temp.fltr, prxy.fltr)
                    
            self.restore_connectors(selected, clear_first=True)

    def restore_connectors(self, proxyItem_list, clear_first=False):  #Does not take care of connections to items not in the list, that is, deleting them.
        """Create connectors (lines) between the items in 'proxyItem_list' 
        according to their connectedness. If 'clear_first' is given,
        connectors in between given items will be removed
        """
        if clear_first:
            for proxyItem in proxyItem_list:
                newlist = [] 
                for cnctr in proxyItem.connectorList: 
                    if (cnctr.itemA in proxyItem_list and
                        cnctr.itemB in proxyItem_list):
#                        cnctr.hide()
                        if cnctr.scene() == self: self.removeItem(cnctr)
                    else: newlist.append(cnctr)
                proxyItem.connectorList = newlist
        
        for proxyItem in proxyItem_list:            
            for input_name, parent_tuple in proxyItem.fltr.filter_inputs.iteritems():                
                for parentProxy in proxyItem_list:
                    if parent_tuple[0] == parentProxy.fltr:
                        inputProxy = proxyItem
                        outputProxy = parentProxy
                        output_name = parent_tuple[1]
                        
                        break_outer = False
                        if not clear_first:
                            for cnctr in outputProxy.connectorList:
                                if ((cnctr.itemA,cnctr.itemB) == (outputProxy,inputProxy) and
                                    (cnctr.radioA_name,cnctr.radioB_name) == (output_name,input_name)): #If there already is a connector
                                    break_outer = True 
                                    break
                        if break_outer:
                            continue
                        
                        start_x, start_y = outputProxy.get_radioPos(OUTPUT_LAYOUT, output_name)
                        end_x, end_y = inputProxy.get_radioPos(INPUT_LAYOUT, input_name)                         
                        startPos = QPointF(outputProxy.scenePos().x()+start_x, 
                                           outputProxy.scenePos().y()+start_y)
                        endPos = QPointF(inputProxy.scenePos().x()+end_x, 
                                         inputProxy.scenePos().y()+end_y)                             
                        connector = Connector( QLineF(startPos, endPos), 
                                           itemA = outputProxy, 
                                           local_posA = QPointF(start_x,start_y),
                                           itemB = inputProxy,
                                           local_posB = QPointF(end_x,end_y) )
                        connector.radioA_layout = OUTPUT_LAYOUT
                        connector.radioB_layout = INPUT_LAYOUT
                        connector.radioA_name = output_name
                        connector.radioB_name = input_name
                        inputProxy.connectorList.append(connector)
                        outputProxy.connectorList.append(connector)
                        connector.setPen(QPen())
                        self.addItem(connector)
        self.scene_update_sig.emit()

    def disableFilterProxyItems(self):
        for prxy in self.getSelectedFilterItems(): prxy.disable()
        
    def enableFilterProxyItems(self): 
        for prxy in self.getSelectedFilterItems(): prxy.enable()
                            
    def removeFilterProxyItems(self):
        """Remove the selected filter items and their connectors from the scene.

#        IMPORTANT: It APPEARS this bug has been fixed in later versions of PyQt
#        Explanation of bug-fix:  
#        It seems like a PyQt bug randly crashes the program when removing things 
#        from the graphics scene and then trying to add a new filter. That is why
#        the removed graphics scene items are only hidden, not removed. This means
#        they will stay in the scene, and filter_scene.items() will thus include
#        filterproxyitems that does not have associated filters.
#        Each item does not take up much memory, so it should be fine even for long
#        runs of the program.
         
        """
            
        for item in self.getSelectedFilterItems()[:]:
            if item.fltr.filtertype == OUTPUT_FILTER:
                self.viewer.removeDisplay(item.fltr)                     
            self.remove_filter_sig.emit(item.fltr)  #cross-thread
            for connector in item.connectorList[:]:  #Since the for-loop changes the for-variable's source, we loop over a copy of the list by typing [:]
                connector.disconnect_connector()
                self.removeItem(connector)
                connector.hide()
            item.setSelected(False)
            item.filterframe.fltr = None
            item.fltr = None
            self.removeItem(item) #Bug (deprecated?)
            item.hide()
#            del item
    
    def debugConnectedness(self):
#        print "ALL items in scene: " + str(self.items())
        filterproxies = self.getFilterItems()
        print "--------------------------"
        print "#proxies: ", len(filterproxies), "#connectors: ", len([i for i in self.items() if isinstance(i,Connector)])
        for item in filterproxies:
            fltr = item.fltr
            print fltr.name + " inputs",fltr.filter_inputs
            print fltr.name + " outputs", fltr.filter_outputs
        
    def getFilterItems(self):
        """Return all FilterProxyItems in the scene which has an associated Img_filter instance.""" 
        try:
            return [item for item in self.items() 
                    if isinstance(item,FilterProxyItem) and item.fltr is not None]
        except RuntimeError: return []
                                     
    def getProxy(self, fltr):
        for prxy in self.getFilterItems():
            if prxy.fltr == fltr: return prxy 
        
    def getSelectedFilterItems(self):
        """Return all selected FilterProxyItems in the scene which has an associated Img_filter instance."""
        try:
            return [item for item in self.selectedItems()
                    if isinstance(item,FilterProxyItem) and item.fltr is not None]
        except RuntimeError: return []

class FilterProxyItem(QtGui.QGraphicsProxyWidget):
    """Class that contains an image filter in the form of a FilterFrame QFrame.
    
    Regular Qt widgets cannot be added to a QGraphicsScene to enable the user to move 
    them around. They first have to be wrapped inside QGraphicsProxyWidgets, which 
    can be added. This class contains one 'FilterFrame' object (a QFrame or QWidget), 
    which in turn contains the image filter itself. The 'FilterFrame' object can be
    accessed with the function 'widget()', see the code below.
    
    Description of the class variables:
    paramWidget -- The widget with parameter sliders and options that gets displayed in 
                   the parameter view when the filterproxyitem is selected.
    grabbedByWidget -- If set to True signals that the filterproxyitem should be moved around
                       until the user releases the mouse and it gets set back to False.
    connectorList -- A list of all 'Connector' objects connected to the item.
    ZValue -- This value controls the depth of the filterproxyitem, that is, if it should 
              be drawn behind or on top of other items in the scene. The default value is
              zero. If selected, the value gets set to 1. Connector items has ZValue 2,
              which means that they will be displayed on top of filterproxyitems.
              
    ZValue values used in increasing order:
    UNSLCT -- Unselected filters.
    UNSLCTCNCT -- Connectors between unselected filters, given at creation.
    SLCT -- Selected filters.
    SLCTCNCT -- Connectors to a selected filter.
    SLCTHLD -- Selected filter when the user holds down the mousebutton on it.
    SLCTCNCTHLD -- Connectors to a filter that is being held by the user.
    """
    UNSLCT = 0
    UNSLCTCNCT = 1
    SLCT = 2
    SLCTCNCT = 3
    HLD = 4
    HLDCNCT = 5 
#    paramWidget_changed_sig = pyqtSignal(object,str,object)
    def __init__(self, fltr, paramWidget):
        QtGui.QGraphicsProxyWidget.__init__(self)
        self.connectorList = []
        self.paramWidget = paramWidget
        self.fltr = fltr
        self.filterframe = FilterFrame(fltr)
        self.setWidget(self.filterframe)        
        self.filterframe.tooltip_display_sig.connect(self.update_tooltip)
        self.filterframe.filterframe_resized_sig.connect(self.redrawConnectors)
        self.grabbedByWidget = False
        if paramWidget is not None:
            self.paramWidget.child_param_changed_sig.connect(self.param_changedSLOT)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable,True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable,True)
        self.setFocusPolicy(Qt.ClickFocus)
        self.setZValue(self.UNSLCT)   
        self.setCursor(Qt.ArrowCursor)          
#        self.setWindowFlags(QtCore.Qt.Widget)
    
        
#    def __del__(self):        
#        print "Debug info: '%s''s graphic part is getting destroyed...",self.widget().ui.filtername_label.text()

    def param_changedSLOT(self, param_name, content):
        """Signal that a parameter was updated, and pass along the parameter name and content."""
#        self.fltr.setParamContent(name,content)  #cross-thread, hopefully not unsafe
        self.scene().param_changed_sig.emit(self.fltr, param_name, content)
    
    def redrawConnectors(self):
        for cnctr in self.connectorList: cnctr.redraw()
            
    def disable(self):
        self.filterframe.fltr.disabled = True
        self.filterframe.labelcolor = (192,192,192)
        self.filterframe.labelfont.setItalic(True)
        self.filterframe.ui.filtername_label.setFont(self.filterframe.labelfont)
        self.filterframe.update() 
        
    def enable(self):
        self.filterframe.fltr.disabled = False
        self.filterframe.labelcolor = self.filterframe.fltr.guiColor
        self.filterframe.labelfont.setItalic(False)
        self.filterframe.ui.filtername_label.setFont(self.filterframe.labelfont)
        self.filterframe.update() 
    
    
    def filtername_changed_slot(self, new_name):
        """Update the filter's name and signal it."""
        self.filterframe.fltr.setName(new_name)
        self.filterframe.ui.filtername_label.setText(new_name)        
        self.filterframe.ui.filtername_label.update()
        self.filterframe.adjustSize()
#        for connector in self.connectorList: #To update positions of connectors if the name change resulted in a different framesize
#            connector.redraw()
            
    def filterdescription_changed_slot(self, new_description):
        """Update the filter's description and signal it."""
        self.filterframe.fltr.setDescription(unicode(new_description))
        
    def update_tooltip(self,position):
        """Display a tooltip on top of the filter."""
        QToolTip.showText(position,self.filterframe.toolTip())
        
    def get_radioPos(self, layout, name):
        """Return the position of the center of the cicle of the radiobutton\ 
        with 'layout'-direction and with 'name'."""
        if layout == OUTPUT_LAYOUT:
            for radio in self.filterframe.outputradios:
                if unicode(radio.text()) == name:
                    geo = radio.geometry()
                    y_pos = geo.y()+geo.height()/2
                    x_pos = geo.x()+geo.width()-6
                    return x_pos,y_pos
        elif layout == INPUT_LAYOUT:
            for radio in self.filterframe.inputradios:
                if unicode(radio.text()) == name:
                    geo = radio.geometry()
                    y_pos = geo.y()+geo.height()/2
                    x_pos = geo.x()+6
                    return x_pos,y_pos
        else:
            pass
            
    def getInputRadioConnector(self, radiobutton):
        """Return the connector (line) connected to the input 'radiobutton'."""
        if radiobutton.layoutDirection() == OUTPUT_LAYOUT:
            raise Exception("radiobutton is not an input radiobutton.\
                             Output radiobuttons can have multiple connectors.")
        for connector in self.connectorList:
            if connector.itemB == self:
                if self.filterframe.childAt(connector.local_posB.toPoint()) == radiobutton:
                    return connector
#            if self.widget().childAt(connector.local_posB.toPoint()) == radiobutton:  #For some reason the radiobuttons have the same memory addresses, even though they belong to different filters.  
#                return connector
        return None
    
    def setConnectorsZValue(self,value):
        """Set the ZValue of all connectors to this filter to 'value'."""        
        for connector in self.connectorList:
            connector.setZValue(value)
                      
    def setFocusSelect(self):
        """Set focus to the filterproxyitem."""
        self.setFocus()
        self.scene().clearSelection()
        self.setSelected(True)
    
    def mark_selected(self):
        """Change the apperance of the filterproxyitem when selected."""
        self.filterframe.changeFocusColor(True)
                                       
    def mark_unselected(self):
        """Change the apperance of the filterproxyitem when unselected."""
        self.filterframe.changeFocusColor(False)
        
    def focusInEvent(self, focusEvent):
        """Change the appereance and depth of the filterproxyitem upon focus."""
        QGraphicsItem.focusInEvent(self, focusEvent)
        self.mark_selected()
        self.setSelectedZValues()

    def focusOutEvent(self, focusEvent):
        """Change the appereance and depth of the filterproxyitem upon loss of focus."""
        QGraphicsItem.focusOutEvent(self, focusEvent)        
        if self in self.scene().getSelectedFilterItems():
            return
        self.mark_unselected()
        self.setUnselectedZValues()          

    def setUnselectedZValues(self):
        self.setZValue(self.UNSLCT) 
        self.setConnectorsZValue(self.UNSLCTCNCT)  

    def setSelectedZValues(self):
        self.setZValue(self.SLCT)  
        self.setConnectorsZValue(self.SLCTCNCT)
        
    def setHoldZValues(self):
        self.setZValue(self.HLD)
        self.setConnectorsZValue(self.HLDCNCT)            

    def mousePressEvent(self, pressEvent):
        """Check what the user clicked on in the widget and take action accordingly."""
        pos = pressEvent.pos()
        alienWidget = self.filterframe.childAt(pos.toPoint())         
        if alienWidget is None or isinstance(alienWidget,QLabel):
            self.setHoldZValues()
            QGraphicsItem.mousePressEvent(self, pressEvent)
            self.grabbedByWidget = True
        else:            
            QGraphicsProxyWidget.mousePressEvent(self, pressEvent)

    def mouseMoveEvent(self, moveEvent):
        """Delegate the moveEvent depending on where the user clicked (grabbed) the widget."""
        if self.grabbedByWidget==True:            
            QGraphicsItem.mouseMoveEvent(self, moveEvent)          
        else:
            QGraphicsProxyWidget.mouseMoveEvent(self, moveEvent)
            
    def moveEvent(self, moveEvent):
        """Make sure the filter's connectors move together with the filter when it is moved."""
        for connector in self.connectorList:                
            connector.redraw()

    def mouseReleaseEvent(self, releaseEvent):
        """Delegate the releaseEvent depending on how the user released the widget."""
        if self.grabbedByWidget == True:
            self.setSelectedZValues()
            QGraphicsItem.mouseReleaseEvent(self, releaseEvent)
            self.grabbedByWidget = False  
        else:
            QGraphicsProxyWidget.mouseReleaseEvent(self, releaseEvent)


class FilterFrame(QtGui.QFrame):
    """This is the QFrame that contains the graphical part of the filters, that is, 
    the titel and the input and output radiobuttons.
    
    Description of the class variables:
    filter -- The image filter instance itself
    inputradios -- List of the input radiobuttons
    outputradios -- List of the output radiobuttons
    
    """
    filterframe_resized_sig = pyqtSignal()
    tooltip_display_sig = pyqtSignal(object)
    def __init__(self, img_filter):
        QtGui.QFrame.__init__(self)
        self.ui = Ui_filterframe()
        self.ui.setupUi(self)
        self.fltr = img_filter
        self.labelcolor = img_filter.guiColor
        self.inputradios = []
        self.outputradios = []
        self.ui.filtername_label.setText(self.fltr.name)
        self.labelfont = QtGui.QFont()             
        self.ui.filtername_label.setFont(self.labelfont)   
        self.setTitleColor(self.labelcolor)
        self.setup_Inputs_Outputs()   
    
    def event(self, some_event):
        """Catch any ToolTip event and signal for the display of a tooltip over the filter."""
        if some_event.type() == QEvent.ToolTip:
            lines = self.fltr.getInfo()
            self.setToolTip(lines)      
            self.tooltip_display_sig.emit(QCursor.pos())          
            return True
        elif some_event.type() == QEvent.Resize:
            self.filterframe_resized_sig.emit()
            return True
        else:
            return False
    
    def setTitleColor(self,bg_rgb_tup, text_rgb_tup=(0,0,0)):
        self.ui.filtername_label.setStyleSheet(
            "background-color: rgb(%i,%i,%i); color: rgb(%i,%i,%i)" 
            %(bg_rgb_tup+text_rgb_tup) )
                                
    def changeFocusColor(self, focus_bool):
        """Change the color of the filter name field according to if the filter has focus."""
        if not self.fltr: return
        if focus_bool:
            self.setTitleColor( (0,0,0),(255,255,255) )
        else:
            self.setTitleColor(self.labelcolor) 
            
    def setup_Inputs_Outputs(self):
        """Create and add input and output radiobuttons to the graphical layout of the filter."""
        for input_name in self.fltr.input_names:
            newRadio = QRadioButton(input_name,self)
            newRadio.setMinimumHeight(12)
            newRadio.setCheckable(False)
            newRadio.setAutoExclusive(False)
            self.inputradios.append(newRadio)
            newRadio.setLayoutDirection(INPUT_LAYOUT)
            self.ui.verticalLayout_inputs.addWidget(newRadio)
        for output_name in self.fltr.output_names:
            newRadio = QRadioButton(output_name,self)
            newRadio.setMaximumHeight(12)
            newRadio.setCheckable(False)
            self.outputradios.append(newRadio)
            newRadio.setAutoExclusive(False)
            newRadio.setLayoutDirection(OUTPUT_LAYOUT)
            self.ui.verticalLayout_outputs.addWidget(newRadio)
            

class ParamWidget(QWidget): #Rename to 'ParamsWidget', with the 's' added. 
    """QWidget-inherited class that contains (displays) a filter's parameter widgets."""
    child_param_changed_sig = pyqtSignal(str,object)
    filtername_changed_in_paramater_sig = pyqtSignal(object)
    filterdescription_changed_in_paramater_sig = pyqtSignal(object)
    def __init__(self, fltr):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_paramWidget()
        self.ui.setupUi(self) 
        self.ui.filtername_lineEdit.setText(fltr.name)
        self.ui.description_plainTextEdit.setPlainText(fltr.description)
        self.setupParams(fltr)
        fltr.param_changed_in_filter_sig.connect(self.update_paramfield)
        
    def on_filtername_lineEdit_editingFinished(self):
        self.filtername_changed_in_paramater_sig.emit(self.ui.filtername_lineEdit.text())
        
    def on_description_plainTextEdit_textChanged(self):
        self.filterdescription_changed_in_paramater_sig.emit(self.ui.description_plainTextEdit.toPlainText())
    
    def update_paramfield(self, name, content):
        for i in xrange(self.ui.verticalLayout.count()):
            try: paramfield = self.ui.verticalLayout.itemAt(i).widget()
            except Exception: continue
            if hasattr(paramfield,"updateContent") and paramfield.name == name:
                paramfield.updateContent(content)
        
    def setupParams(self,fltr):
        param_ranks = []
        for param_name in fltr.params:
            param_ranks.append( (fltr.params[param_name].rank, param_name) )
        param_order = sorted(param_ranks, reverse=True)
        for rank,param_name in param_order:            
            p = fltr.params[param_name]
            new_paramField = None
            if p.type == 'text':
                new_paramField = ParamField_text(p.name, p.description, p.content)      
            elif p.type == 'variable':
                new_paramField = ParamField_variable(p.name, p.description, p.content, p.min, p.max)                
            elif p.type == 'file':
                new_paramField = ParamField_file(p.name, p.description, p.content)                
            elif p.type == 'list':
                new_paramField = ParamField_list(p.name, p.description, p.content, p.other_content)
            elif p.type == 'codebox':
                new_paramField = ParamField_codebox(p.name,p.description,p.content)  
            elif p.type == 'display':
                new_paramField = ParamField_display(p.name,p.description,p.content)  
            else:
                continue
            new_paramField.paramfield_changed_sig.connect(self.child_param_changed_sig.emit)                    
            if p.description is not None: 
                new_paramField.description_label = QtGui.QLabel(new_paramField.ui.groupBox)
                setupParamDescriptionLabel(new_paramField.description_label,p.description)
                new_paramField.ui.verticalLayout_groupBox.insertWidget(0,new_paramField.description_label)  
            if rank is None:
                next_to_last = self.ui.verticalLayout.count()-1
                self.ui.verticalLayout.insertWidget(next_to_last,new_paramField)
            else:
                self.ui.verticalLayout.insertWidget(1,new_paramField)

def setupParamDescriptionLabel(descript_label,description):
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(descript_label.sizePolicy().hasHeightForWidth())
    descript_label.setSizePolicy(sizePolicy)
    descript_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
    descript_label.setWordWrap(True)
    descript_label.setText(description)

class ParamField_variable(QWidget):
    """This class has the form of a slider the user can change a filter parameter with."""
    paramfield_changed_sig = pyqtSignal(str,object)
    def __init__(self, name, description, value, mini, maxi):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_param_variable()
        self.ui.setupUi(self)
        self.currspin = self.ui.doubleSpinBoxCurrent
        self.maxspin = self.ui.doubleSpinBoxMax
        self.minspin = self.ui.doubleSpinBoxMin
        self.slider = self.ui.valueSlider
        if mini is None and maxi is not None:
            mini = value+(value-maxi)
        elif mini is not None and maxi is None:
            maxi = value+(value-mini)
        elif mini is None and maxi is None:
            mini = value - value/2
            maxi = value + value/2
        self.name = unicode(name)
        self.ui.groupBox.setTitle(self.name)
#        self.ui.groupBox.setStyleSheet("background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E0E0E0, stop: 1 #FFFFFF)")
        self.emitSignal = True        
        self.multiplier = 100
        self.changeSlider = True
        self.changeCurrspin = True        
        self.maxspin.setValue(maxi)
        self.minspin.setValue(mini)
        self.currspin.setValue(value)
        self.setSliderRange(mini, maxi)
        self.setSliderValue(value)
        self.defaultValue = value
        self.ui.valueSlider.mouseDoubleClickEvent = self.valueSlider_doubleClicked
        
        
    def getSliderValue(self):
        """Translate the sliders current value and return it (the real value)."""
        return self.slider.value()/self.multiplier

    def setSliderValue(self, val):
        """Set the slider to a value by first moving the decimals of 'val' left of the decimal point."""
        self.slider.setValue( val*self.multiplier )
            
    def setSliderRange(self,mini,maxi):
        """Set a new range to the slider."""
        self.slider.setRange(int(mini*self.multiplier), int(maxi*self.multiplier))
    
    def valueSlider_doubleClicked(self, *args, **kwargs):
        """Reset slider value to default when double clicked"""
        print "double!!!"
        self.setSliderValue(self.defaultValue)
        return QWidget.mouseDoubleClickEvent(self.ui.valueSlider, *args, **kwargs)
        
    def on_valueSlider_valueChanged(self):
        """Update the 'current'-spinbox value upon a change in the slider's value."""
        self.changeSlider = False
        if self.changeCurrspin: self.currspin.setValue(self.getSliderValue())
        self.changeSlider = True

    def on_doubleSpinBoxCurrent_valueChanged(self):
        """Emit the 'param_changed' signal."""
        if self.emitSignal:        
            self.paramfield_changed_sig.emit(self.name, self.currspin.value())
            
    def on_doubleSpinBoxCurrent_editingFinished(self):
        val = self.currspin.value()
        if val < self.minspin.value():
            self.setMinVal(val)
        elif val > self.maxspin.value(): self.setMaxVal(val)
        self.changeCurrspin = False
        if self.changeSlider: self.setSliderValue(val)
        self.changeCurrspin = True
          
    def on_doubleSpinBoxMin_editingFinished(self):
        self.setMinVal(None)
        
    def setMinVal(self,val):
        if val is not None: self.minspin.setValue(val)
        self.setSliderRange( self.minspin.value(), self.maxspin.value() )
        
    def on_doubleSpinBoxMax_editingFinished(self):        
        self.setMaxVal(None)
        
    def setMaxVal(self,val):
        if val is not None: self.maxspin.setValue(val)
        self.setSliderRange( self.minspin.value(), self.maxspin.value() ) #Will in effect change self.currspin if necessary
        
    def updateContent(self, content):
        self.emitSignal = False
        if content < self.minspin.value():
            self.setMinVal(content)
        if content > self.maxspin.value():
            self.setMaxVal(content)                        
        self.currspin.setValue(content)
        self.setSliderValue(content)
        self.emitSignal = True

        
class ParamField_file(QWidget):
    """This class has the form of a button the user can select a file with."""
    paramfield_changed_sig = pyqtSignal(str,object)
    def __init__(self, name, description, file_):
        QWidget.__init__(self)
        self.ui = Ui_param_file()
        self.ui.setupUi(self)
        self.name = unicode(name)
        self.ui.groupBox.setTitle(self.name)
        if file_ is None: pass
        else:            
            self.ui.historyComboBox.addItem(file_)
     
    def on_fileButton_clicked(self,dummy=None):
        if dummy is None:return #To handle a pyqt bug where the button fires twice
        fileDialog = QFileDialog()
        fileDialog.setFileMode(QFileDialog.AnyFile)
        fileDialog.setViewMode(QFileDialog.Detail)
        fileNames = []
        if (fileDialog.exec_()):
            fileNames = fileDialog.selectedFiles()        
        if len(fileNames) == 1:
            self.ui.historyComboBox.insertItem(0,fileNames[0])
            if self.ui.historyComboBox.currentIndex() != 0:
                self.ui.historyComboBox.setCurrentIndex(0)
    
    def on_historyComboBox_currentIndexChanged(self, entry):
        self.paramfield_changed_sig.emit(unicode(self.name), unicode(entry))     
        
    def updateContent(self, content):
        self.ui.fileLabel.setText(unicode(content))
            
class ParamField_list(QWidget):
    """This class has the form of a list the user can make a choice from with."""
    paramfield_changed_sig = pyqtSignal(str,object)
    def __init__(self, name, description, default, lst):
        QWidget.__init__(self)
        self.ui = Ui_param_list()
        self.ui.setupUi(self)
        self.list = None
        self.selected = None
        self.name = unicode(name)
        self.ui.groupBox.setTitle(self.name)
        self.setup_complete = False     
        if lst is None or lst == []:
            raise Exception("Error. A list parameter must have at least one item in it at creation.")
        else: 
            self.list = lst
        for index,item in enumerate(self.list):
            if isinstance(item,tuple):
                if unicode(item[0]) == unicode(default): self.selected = index
                self.ui.list_comboBox.addItem(unicode(item[0]))
            else:
                if unicode(item) == unicode(default): self.selected = index
                self.ui.list_comboBox.addItem(unicode(item))
        self.ui.list_comboBox.setCurrentIndex(self.selected)
        self.setup_complete = True
        self.emitSignal = True
    
    @pyqtSlot(int)
    def on_list_comboBox_currentIndexChanged(self, entry):
        if self.setup_complete == False: return
        if not isinstance(entry,int): raise Exception("Wrong argument type")
        if entry == -1: raise Exception("List should not become empty")
        if isinstance(self.list[entry],tuple):
            content = self.list[entry][1]
        else: 
            content = self.list[entry]
        if self.emitSignal:
            self.paramfield_changed_sig.emit(unicode(self.name), content)            
        
class ParamField_text(QWidget):
    paramfield_changed_sig = pyqtSignal(str,object)
    def __init__(self, name, description, default):
        QWidget.__init__(self)
        self.ui = Ui_param_text()
        self.ui.setupUi(self)
        self.name = unicode(name)
        self.ui.groupBox.setTitle(self.name)
        if default is None: default = ""
        self.ui.text_lineEdit.setText(default)
        self.emitSignal = True     
        
    def on_text_lineEdit_editingFinished(self):
        self.paramfield_changed_sig.emit(self.name,unicode(self.ui.text_lineEdit.text()))
        
    def updateContent(self, content):
        self.ui.text_lineEdit.setText(unicode(content))

class PlotFrame(QFrame):
    def __init__(self, fig, parent=None,):
        QFrame.__init__(self, parent)
        self.canvas = FigureCanvasQTAgg(fig)
        self.canvas.setContentsMargins(2,2,2,2)
        self.canvas.setParent(self)
        self.mpl_toolbar = NavigationToolbar2QTAgg(self.canvas, self)
        vbox = QVBoxLayout()
        vbox.setContentsMargins(2,2,2,2)
        vbox.addWidget(self.canvas)
        vbox.addWidget(self.mpl_toolbar)
        self.setLayout(vbox)
        self.canvas.draw()          
        
class ParamField_display(QWidget):
    paramfield_changed_sig = pyqtSignal(str,object)
    def __init__(self, name, description, default):
        QWidget.__init__(self)
        self.ui = Ui_param_empty()
        self.ui.setupUi(self)
        self.name = unicode(name)
        self.ui.groupBox.setTitle(self.name)
        self.arrlabel = QLabel()
        self.arrlabel.setText("")
        self.emitSignal = True
        self.type = None
        self.setContentType(default)
        self.updateContent(default)

        
    def setContentType(self,content):   
        """Remove or add widgets in groupbox and set 'self.type' 
        depending on the type of 'content'"""     
        if isinstance(content,(numpy.ndarray,QPixmap,QImage)):
            if self.type == 'img': return
            elif self.type == 'plot':
                try: self.ui.verticalLayout_groupBox.addWidget(self.plotframe)
                except Exception: pass            
            elif self.type is None:
                self.ui.verticalLayout_groupBox.addWidget(self.arrlabel)
            self.type = 'img'
        elif isinstance(content,matplotlib.figure.Figure):
            if self.type == 'plot': return
            elif self.type == 'img':
                try: self.ui.verticalLayout_groupBox.removeWidget(self.arrlabel)
                except Exception: pass
            elif self.type is None:
                self.plotframe = PlotFrame(content)
                self.ui.verticalLayout_groupBox.addWidget(self.plotframe)
            self.type = 'plot'
        elif content is None:
            if self.type is None: return
            else: 
                try: self.ui.verticalLayout_groupBox.removeWidget(self.arrlabel)
                except Exception: pass
                try: self.ui.verticalLayout_groupBox.addWidget(self.plotframe)
                except Exception: pass
                self.type = None
        else: 
            raise Exception("Unsupported 'content'-argument when creating parameter '%s'" %self.name)
            
    def updateContent(self, content):
        self.setContentType(content)
        if self.type is None: return
        if isinstance(content,numpy.ndarray):
            self.arrlabel.setPixmap(arr2pixmap(content))
        elif isinstance(content,QPixmap):
            self.arrlabel.setPixmap(content)
        elif isinstance(content,QImage):
            self.arrlabel.setPixmap(QPixmap.fromImage(content))                       
        elif isinstance(content,matplotlib.figure.Figure):
            try: self.plotframe.canvas.draw()
            except Exception:
                traceback.print_exc() #TODO fix
        
        
class ParamField_codebox(QWidget):
    paramfield_changed_sig = pyqtSignal(str,object)
    def __init__(self, name, description, default):
        QWidget.__init__(self)
        self.ui = Ui_param_codebox()
        self.ui.setupUi(self)
        self.name = unicode(name)
        self.ui.groupBox.setTitle(self.name)
        self.emitSignal = True
        if default is None or default == "": default = "\n\n\n\n"
        
        lexer = Qsci.QsciLexerPython()
        self.scifont = QtGui.QFont()
        self.scifont.setFamily("Consolas")
        self.scifont.setFixedPitch(True)
        self.scifont.setPointSize(10)
        lexer.setFont(self.scifont)
        self.ui.codebox_Qsci.setMinimumHeight(len(default.split("\n"))*20)
        self.ui.codebox_Qsci.setMaximumHeight(len(default.split("\n"))*20)
        self.ui.codebox_Qsci.setLexer(lexer)
        self.ui.codebox_Qsci.setTabWidth(4)
        self.ui.codebox_Qsci.setAutoIndent(True)
        self.ui.codebox_Qsci.setEdgeMode(Qsci.QsciScintilla.EDGE_NONE)    
        self.ui.codebox_Qsci.setMarginLineNumbers(1,True)
        self.ui.codebox_Qsci.setText(default)                             
        self.ui.codebox_Qsci.focusOutEvent = self.codebox_focusOutEvent
        self.ui.codebox_Qsci.setFocusPolicy(Qt.StrongFocus)
        self.ui.codebox_Qsci.installEventFilter(self)
    
    def eventFilter(self,widget,event):
        """Prevent keyboard shortcuts from firing inside the QScintilla field."""
        if (event.type() == QEvent.ShortcutOverride and
                  widget is self.ui.codebox_Qsci):
            event.accept()
            return True
        return QWidget.eventFilter(self, widget, event)
    
    def updateContent(self, content):
        self.ui.codebox_Qsci.setText(content)

    def codebox_focusOutEvent(self, focusEvent):
        Qsci.QsciScintilla.focusOutEvent(self.ui.codebox_Qsci, focusEvent)
        self.paramfield_changed_sig.emit(self.name, unicode(self.ui.codebox_Qsci.text()))
    
        
class TreeFilterItem(QTreeWidgetItem):
    def __init__(self, fltr):
        QTreeWidgetItem.__init__(self, ["", fltr.name])
#        self.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable))
        self.fltr = fltr

    def setName(self, new_name):
        self.setText(1, new_name)
        
    def setTime(self, time):
        self.setText(0, unicode(time))

    
class Connector(QGraphicsLineItem):
    """Class that contains a connecting line between two filters and handles 
    the connection and disconnection of those filters.
    
    Description of the class variables:
    itemA -- The filterproxyitem that contains the output.
    itemB -- The filterproxyitem that contains the input.
    radioA_layout -- The type of radiobutton, (OUTPUT_LAYOUT or INPUT_LAYOUT)
    radioB_layout -- The type of radiobutton, (OUTPUT_LAYOUT or INPUT_LAYOUT)
    radioA_name -- Name of radiobutton
    radioB_name -- Name of radiobutton
    local_posA -- The (pixel)position of where the connector is connected at itemA
    local_posB -- The (pixel)position of where the connector is connected at itemB
     
    """
    def __init__(self, QLineF, 
                 itemA=None, local_posA=None, 
                 itemB=None, local_posB = None):
        QGraphicsLineItem.__init__(self, QLineF)
        self.itemA = itemA
        self.itemB = itemB
        self.radioA_layout = None
        self.radioB_layout = None
        self.radioA_name = None
        self.radioB_name = None
        self.local_posA = local_posA    
        self.local_posB = local_posB
        self.setZValue(5)            

    def redraw(self):
        """Redraw the line between it's endpoints."""
        if self.itemA is None or self.itemB is None:
            raise Exception('one of the connectors ends are none when they shouldnt be')
        Ax, Ay = self.itemA.get_radioPos(self.radioA_layout, self.radioA_name)
        Bx, By = self.itemB.get_radioPos(self.radioB_layout, self.radioB_name)
        self.local_posA = QPointF(Ax, Ay)
        self.local_posB = QPointF(Bx, By)
        self.setLine( QLineF(self.itemA.scenePos().x()+self.local_posA.x(), 
                             self.itemA.scenePos().y()+self.local_posA.y(),
                             self.itemB.scenePos().x()+self.local_posB.x(),
                             self.itemB.scenePos().y()+self.local_posB.y()) )
        
    def connect_item_filters(self):  #Should be made to raise exception if the connection is invalid or unsuccessful.
        """Connect the filters at the ends of the connector."""
        radioA = self.itemA.widget().childAt(self.local_posA.toPoint())
        radioB = self.itemB.widget().childAt(self.local_posB.toPoint())
        filterA = self.itemA.fltr
        filterB = self.itemB.fltr
        ioA = unicode(self.itemA.widget().childAt(self.local_posA.toPoint()).text())
        ioB = unicode(self.itemB.widget().childAt(self.local_posB.toPoint()).text())        
        
        if radioA.layoutDirection() == radioB.layoutDirection():
            print "Can only connect inputs to outputs. This message should probably not\
                    be displayed, you've may have discovered a bug.", __file__
            return FAIL    
        if radioA.layoutDirection() == OUTPUT_LAYOUT:  #A is an output and B is an input
            self.radioA_layout, self.radioA_name = OUTPUT_LAYOUT, ioA
            self.radioB_layout, self.radioB_name = INPUT_LAYOUT, ioB
            return filterA.thread().connect_filters(filterA,filterB,[ioA],[ioB])  
        else:
            self.radioA_layout, self.radioA_name = INPUT_LAYOUT, ioA
            self.radioB_layout, self.radioB_name = OUTPUT_LAYOUT, ioB
            return filterA.thread().connect_filters(filterB,filterA,[ioB],[ioA])
        
    def disconnect_item_filters(self):
        """Disconnect the filters and the ends of the connector."""
        radioA = self.itemA.widget().childAt(self.local_posA.toPoint())
        radioB = self.itemB.widget().childAt(self.local_posB.toPoint())
        filterA = self.itemA.fltr
        filterB = self.itemB.fltr
        ioA = unicode(self.itemA.widget().childAt(self.local_posA.toPoint()).text())
        ioB = unicode(self.itemB.widget().childAt(self.local_posB.toPoint()).text())
        if self.itemA == self.itemB:
            raise Exception('something went seriously wrong')
        if radioA.layoutDirection() == radioB.layoutDirection():
            print 'error. two inputs or two outputs'
            return FAIL
        return filterA.thread().disconnect_filters(filterA,filterB,[ioA],[ioB])
    
    def disconnect_connector(self):    
        """Disconnect the connector from the filterproxyitems by removing it from their connectorLists."""    
        if self.itemA is not None:
            if self in self.itemA.connectorList:
                self.itemA.connectorList.remove(self)
        if self.itemB is not None:
            if self in self.itemB.connectorList:
                self.itemB.connectorList.remove(self)


def createApp():
    app = QApplication(sys.argv)
    controls = Controls()
    controls.show()
    controls.quit_sig.connect(app.quit)
    return app,controls 
    
if __name__ == '__main__':
    app, controls = createApp()
#    app.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
    if len(sys.argv)>1 :
        sys.path.append(os.path.join(os.path.split(__file__)[0],'filters_package'))
        filters, positions = save_load.loadFilters(sys.argv[1])
        controls.addFilters(filters, positions=positions)

    sys.exit(app.exec_())
