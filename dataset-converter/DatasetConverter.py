import glob, os
from .wrapper.VOCWrapper import VOCWrapper
from .wrapper.LabelMeWrapper import LabelMeWrapper
from .wrapper.FPDSWrapper import FPDSWrapper
# from .wrapper.YOLOWrapper import YOLOWrapper
from .Wrapper import YOLOWrapper
from .wrapper.CocoWrapper import CocoWrapper
from .PathUtil import fixPath
from .data.LabelData import LabelData

class DatasetConverter:
    def __init__(self):
        self.__wrappers = {
            'voc': VOCWrapper,
            'labelme': LabelMeWrapper,
            'fpds': FPDSWrapper,
            'yolo': YOLOWrapper,
            'coco': CocoWrapper
        }

    # def convert(self, sourcePath, destinationPath, inputWrapper, outputWrapper):
    #     try:
    #         self.__wrappers[inputWrapper]
    #     except:
    #         raise Exception(f'No wrappers found with name {inputWrapper}')
    #     try:
    #         self.__wrappers[outputWrapper]
    #     except:
    #         raise Exception(f'No wrappers found with name {outputWrapper}')
    #     files = glob.glob(f"{sourcePath}/*.{self.__wrappers[inputWrapper]().ext()}", recursive=True)

    #     toParse = len(files)
    #     parsed = 0
    #     print(f"[DatasetConverter] Parsing files: {parsed}/{toParse}", end="")

    #     os.makedirs(destinationPath, exist_ok=True )
    #     for file in files:
    #         parsed += 1
    #         print(f"\r[DatasetConverter] Parsing files: {parsed}/{toParse}", end="")
    #         iw = self.__wrappers[inputWrapper]()
    #         file = fixPath(file)
    #         iw.read(file)

    #         if iw.data() != None:
    #             ow = self.__wrappers[outputWrapper](iw.data())
    #             ow.write(f'{destinationPath}/{file.split("/")[-1]}')
    #     print("\n[DatasetConverter] Done!")

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
        data_list = iw.read_directory(sourcePath)
        print()
        data = data_list[0]
        data.show()
        # for obj in iw._data.objects():
        #     print(obj)