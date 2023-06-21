import glob
from .wrapper import *
from .util.PathUtil import fixPath

class DatasetConverter:
    def __init__(self):
        self.__wrappers = {
            'voc': VOCWrapper,
            'labelme': LabelMeWrapper,
            'fpds': FPDSWrapper,
            'yolo': YOLOWrapper,
            'coco': CocoWrapper
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
        files = glob.glob(f"{sourcePath}/*.{self.__wrappers[inputWrapper]().ext()}", recursive=True)

        toParse = len(files)
        parsed = 0
        print(f"[DatasetConverter] Parsing files: {parsed}/{toParse}", end="")

        for file in files:
            parsed += 1
            print(f"\r[DatasetConverter] Parsing files: {parsed}/{toParse}", end="")
            iw = self.__wrappers[inputWrapper]()
            iw.read(file)

            ow = self.__wrappers[outputWrapper](iw.data())
            file = fixPath(file)
            ow.write(f'{destinationPath}/{file.split("/")[-1]}')
        print("\n[DatasetConverter] Done!")
