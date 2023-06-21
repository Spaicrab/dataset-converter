import glob, os
from .Wrapper import *
from .PathUtil import fixPath
from .data.LabelData import LabelData

class DatasetConverter:
    def __init__(self):
        self.__wrappers = {
            'voc': VOCWrapper,
            # 'labelme': LabelMeWrapper,
            # 'fpds': FPDSWrapper,
            'yolo': YOLOWrapper,
            # 'coco': CocoWrapper
        }

    def convert(self, sourcePath, destinationPath, inputWrapper, outputWrapper):
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
        data_list = iw.read_directory(sourcePath)
        ow.write_directory(destinationPath, data_list)
        print("Done!")