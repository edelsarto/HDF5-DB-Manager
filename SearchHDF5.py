from inspect import Parameter, _void
#from nis import match
from h5py._hl import base, dataset
from h5py._hl.datatype import Datatype
from h5py._hl.files import File
from h5py import File, _hl
import h5py

import numpy as np
from numpy.core.defchararray import count, index
from numpy.core.fromnumeric import _choose_dispatcher

from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QWidget, QWidgetAction
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader

from widgets import *

class Functions():

    #da finire
    def GetSearchMod(path):

        split_path = path.split("/")

        testName = split_path[0]
        param = split_path[1]
        datasetName = split_path[2]

        if testName != "" and param == "" and datasetName == "":
            return "ONLYTESTNAME"
        elif testName != "" and param != "" and datasetName == "":
            return "PARAMETER"
        elif testName != "" and param != "" and datasetName != "":
            return "FULLPATH"

    def SearchHDF5File(path, tags, absolute):
        
        split_path = path.split("/")
        #print("SEARCHHDF5 fun - path: " + str(split_path))
        with h5py.File("C:/Users/Andrea/Desktop/Hdf5Manager/HDF5 File/" + split_path[0] + ".h5", 'r') as hdf:

            item = hdf

            hdf5_element_list = list(item.keys())

            for element in split_path:
                
                i = 0

                for keyElement in hdf5_element_list:
                    
                    if element == keyElement:
                        
                        item = item.get(hdf5_element_list[i])
                        
                        if item.__class__ != _hl.dataset.Dataset:

                            hdf5_element_list = list(item.keys())
                        
                        elif item.__class__ == _hl.dataset.Dataset:

                            dsName = item.name.split("/")

                            print(dsName[2])

                            if dsName[2] == split_path[2]:
                                print("OK!!")
                                datasetValues = np.array(item)

                                return datasetValues

                    i += 1
                
                print("\n")

    def SearchDatasetAttr(path):

        split_path = path.split("/")
        #print("SEARCHHDF5 fun - path: " + str(split_path))
        with h5py.File("C:/Users/Andrea/Desktop/Hdf5Manager/HDF5 File/" + split_path[0] + ".h5", 'r') as hdf:

            item = hdf

            hdf5_element_list = list(item.keys())

            for element in split_path:
                
                i = 0

                for keyElement in hdf5_element_list:
                    
                    if element == keyElement:
                        
                        item = item.get(hdf5_element_list[i])
                        
                        if item.__class__ != _hl.dataset.Dataset:

                            hdf5_element_list = list(item.keys())
                        
                        elif item.__class__ == _hl.dataset.Dataset:
                            
                            print("TAGS: " + item.attrs["TAGS"])

                            print(split_path[2])
                            
                            dsName = item.name.split("/")

                            print(dsName[2])

                            if dsName[2] == split_path[2]:
                                print("OK!")
                                return item.attrs["TAGS"]

                    i += 1
                
                print("\n")

    def InsertTag():

        i=0
        listAddTags = []

        while i < 3:

            print(i + 1)
            listAddTags.append(input("insert tag: "))
            i += 1
            
        return listAddTags