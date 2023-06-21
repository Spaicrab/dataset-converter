import glob, os

from .Wrapper import *
from .PathUtil import fixPath
from .data.LabelData import LabelData

class DatasetConverter:
    def __init__(self):
        self.__wrappers = {
            'voc': VOCWrapper,
            'yolo': YOLOWrapper,
            'coco': CocoWrapper
        }

    def convert(self, sourcePath, destinationPath, inputWrapper, outputWrapper, classes=None, copy=True, recursive=True):
        try:
            self.__wrappers[inputWrapper]
        except:
            raise Exception(f'No wrappers found with name {inputWrapper}')
        try:
            self.__wrappers[outputWrapper]
        except:
            raise Exception(f'No wrappers found with name {outputWrapper}')

        iw = self.__wrappers[inputWrapper]()
        ow = self.__wrappers[outputWrapper]()

        print("Parsing files...")
        data_list = iw.read_directory(sourcePath, recursive)
        total_files = len(data_list)

        if classes != None:
            remove_list = []
            for i, data in enumerate(data_list, start=0):
                data.filter_classes(classes)
                if len(data.objects()) == 0:
                    remove_list.insert(0, i)
            for i in remove_list:
                data_list.pop(i)
            converted_files = len(data_list)
            text = f"Converted {converted_files} of {total_files} files."
        else:
            text = f"Converted {total_files} files."
        
        ow.write_directory(destinationPath, data_list, copy)
        print(text)