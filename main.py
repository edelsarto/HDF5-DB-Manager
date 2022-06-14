# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html

from asyncio.windows_events import NULL
from cgi import test
from itertools import count
import os
from pathlib import Path
from posixpath import split
import string
import sys
from webbrowser import get

from h5py._hl import base, dataset
from h5py._hl.datatype import Datatype
from h5py._hl.files import File
from h5py import File, _hl
import h5py

import numpy as np
from numpy import dtype
from SearchHDF5 import Functions as searchhdf5

from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QWidget, QWidgetAction
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader

# IMPORT / GUI AND MODULES AND WIDGETS

from modules import *
from widgets import *
os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL WIDGET
widgets = None

param_list_item = []
ds_list_item = []
resultsArray = []
listItemsSelected = []
h5file = []

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        global param_list_item
        global ds_list_item
        global resultsArray
        global listItemsSelected
        global h5file

######### USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX

        Settings.ENABLE_CUSTOM_TITLE_BAR = True

######### APP NAME #########

        title = "HDF5 - Database Manager"
        description = "HDF5 Database Manager"

######### APPLY TEXTS #########

        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

######### TOGGLE MENU #########
        
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

######### SET UI DEFINITIONS #########
        
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

######### BUTTONS CLICK #########
        

######### LEFT MENUS #########

        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)
        widgets.btn_save.clicked.connect(self.buttonClick)
        widgets.btn_exit.clicked.connect(self.buttonClick)

        widgets.btn_test.clicked.connect(self.buttonClick)

        widgets.btn_search.clicked.connect(self.buttonClick)
        widgets.tableWidget_showSearchResult.doubleClicked.connect(self.buttonClick)

######### EXTRA LEFT BOX #########

        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
            widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
            widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

######### EXTRA RIGHT BOX #########

        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
            widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

######### SHOW APP #########
        
        self.show()

######### SET CUSTOM THEME #########
        
        useCustomTheme = False
        themeFile = "themes\py_dracula_light.qss"

######### SET THEME AND HACKS #########

        if useCustomTheme:

            # LOAD AND APPLY STYLE

            UIFunctions.theme(self, themeFile, True)

            # SET HACKS

            AppFunctions.setThemeHack(self)

######### SET HOME PAGE AND SELECT MENU #########
        
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))

######### BUTTONS CLICK #########

    # Post here your functions for clicked buttons #
    def buttonClick(self):

        ### Take data ###
        def GetData(self):
            
            path = widgets.lineEdit_url_1.text() + "/" + (widgets.lineEdit_url_2.text())  + "/" + (widgets.lineEdit_url_3.text())
            tags = widgets.lineEdit_tags.text()
            
            mod = searchhdf5.GetSearchMod(path)

            if(mod == "ONLYTESTNAME"):
                GetSearchReuslts(path)#passa solo prima linea
                #scegli dataset da spacchettare

            elif(mod == "PARAMETER"):
                GetSearchReuslts(path)#modifica per mettere solo gruppo scelto
                #scegli dataset da spacchettare

            elif(mod == "FULLPATH"):
                #spacchetta direttamente il dataset
                exit
    
        ### Found .h5 file and trace members ###
        def GetSearchReuslts(path):
            
            param_list_item.clear()
            ds_list_item.clear()
            h5file.clear()

            split_path = path.split("/")

            #mod = Functions.PartialSearch(path)

            with h5py.File("C:/Users/Andrea/Desktop/Hdf5Manager/HDF5 File/" 
            + split_path[0] + ".h5", 'r') as hdf:
                
                h5file.insert(0, h5py.File("C:/Users/Andrea/Desktop/Hdf5Manager/HDF5 File/" + 
                split_path[0] + ".h5", 'r'))
               
                DiscoverDataset(hdf)

        ### Found .h5 file and trace datasets ###
        def DiscoverDataset(hdf):

            groupItem = hdf

            param_list_str = list(groupItem.keys())
            
            i = 0
            y = 0

            for group in param_list_str:
                
                param_list_item.insert(i, groupItem.get(group))
                
                ds_list_str = list(param_list_item[i].keys())

                for ds in ds_list_str:

                    ds_list_item.insert(y, param_list_item[i].get(ds))

                    y += 1
                    
                i += 1

            FillSearchResultTable(param_list_str, ds_list_item)

        ### Fill search result table with dataset path founded ###
        def FillSearchResultTable(groupList, dsList):

            widgets.tableWidget_showSearchResult.setRowCount(len(dsList))
            widgets.tableWidget_showSearchResult.setColumnCount(1)

            indX = 0

            for group in groupList:

                for ds in dsList:

                    widgets.tableWidget_showSearchResult.setItem(indX, 0, QTableWidgetItem(str(ds.name)))

                    indX += 1

                indX += 1

            return

        ### Fill result table with dataset choose data ###
        def FillTable(toFillArray):

            indX = 0
            indY = 0
            
            widgets.tableWidget_showResult.setRowCount(toFillArray.shape[1])
            widgets.tableWidget_showResult.setColumnCount(toFillArray.shape[0])

            for y in range(toFillArray.shape[1]):

                indX = 0

                for x in range(toFillArray.shape[0]):

                    widgets.tableWidget_showResult.setItem(indX, indY, QTableWidgetItem(str(toFillArray[indX][indY])))
                    
                    indX += 1

                indY += 1
          
        ### Set column label name with dataset attribute ###
        def SetHorizontalLabel(path):

            searchhdf5.SearchDatasetAttr(path)
            #split_path = path.split("/")
                                           
            #print("tag: ", item.attrs["TAGS"])
            widgets.tableWidget_showResult.setHorizontalHeaderLabels(searchhdf5.SearchDatasetAttr(path))

######## GET BUTTON CLICKED #########

        btn = self.sender()
        btnName = btn.objectName()

######## PRINT BTN NAME #########

        #print(f'Button "{btnName}" pressed!')
        #print(f'Button "{btn}" pressed!')

######## SELECT RESULT #########

        if btnName == "tableWidget_showSearchResult":

            listItemsSelected = btn.selectedItems()
                        
            FillTable(searchhdf5.SearchHDF5File(widgets.lineEdit_url_1.text() 
            + listItemsSelected[0].text(), "", 0))

            SetHorizontalLabel(widgets.lineEdit_url_1.text() 
            + listItemsSelected[0].text())

######## SHOW HOME PAGE #########

        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

######## SHOW WIDGETS PAGE #########

        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

######## SHOW NEW PAGE #########

        if btnName == "btn_new":
            widgets.stackedWidget.setCurrentWidget(widgets.new_page) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU
        
######## SHOW TEST PAGE #########

        if btnName == "btn_test":
            widgets.stackedWidget.setCurrentWidget(widgets.test) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU
            
        if btnName == "btn_save":
            print("Save BTN clicked!")
        
        if btnName == "btn_exit":
            print("Exit BTN clicked!")

        if btnName == "btn_search":
            GetData(self)

######## RESIZE EVENTS #########
    
    def resizeEvent(self, event):

        # Update Size Grips

        UIFunctions.resize_grips(self)

######## MOUSE CLICK EVENTS #########
    
    def mousePressEvent(self, event):

######## SET DRAG POS WINDOW ######### 

        self.dragPos = event.globalPos()

######## PRINT MOUSE EVENTS #########

        #if event.buttons() == Qt.LeftButton:
        #    print('Mouse click: LEFT CLICK')
        #if event.buttons() == Qt.RightButton:
        #    print('Mouse click: RIGHT CLICK')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec())
