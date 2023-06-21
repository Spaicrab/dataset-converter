import imagesize, glob

from .data.LabelData import LabelData
from .PathUtil import *

class Wrapper:
    def __init__(self, data=None):
        self._path = None
        self._data = None
        if data is None or data is not LabelData:
            pass
        self._data = data

    def read_directory(self, dir_path):
        data_list = []
        dir_path = fixPath(dir_path)
        images = glob.glob(dir_path + "/*.[jp][pn]g")
        to_parse = len(images)
        parsed = 0
        for img_path in images:
            img_path = fixPath(img_path)
            parsed += 1
            print(f"\r[DatasetConverter] Parsing files: {parsed}/{to_parse}", end="")
            data = self.read(img_path)
            data_list.append(data)
        return data_list

    def read(self, path):
        self._path = path

    def write_directory(self, dir_path):
        pass

    def write(self, path):
        self._path = path

    def data(self):
        return self._data

    def ext(self):
        return None

class YOLOWrapper(Wrapper):
    def ext(self):
        return "txt"

    def read(self, img_path):
        classes = []
        try:
            cpath = changeTargetFile(img_path, 'classes.txt')
            with open(cpath) as f:
                for line in f.readlines():
                    classes.append(line.replace("\n", ""))
        except:
            raise Exception("Missing classes.txt file")
        label_path = findByExtList(img_path, ['txt'])
        if label_path == None:
            return
        width, height = imagesize.get(img_path)
        self._data = data = LabelData(
            img_path,
            width,
            height
        )
        with open(label_path) as f:
            lines = f.readlines()
            for line in lines:
                args = line.split(" ")
                args[1] = float(args[1]) * width
                args[3] = float(args[3]) * width
                args[2] = float(args[2]) * height
                args[4] = float(args[4]) * height

                pmin = [float(args[1]) - float(args[3]) / 2, float(args[2]) - float(args[4]) / 2]
                pmax = [float(args[1]) + float(args[3]) / 2, float(args[2]) + float(args[4]) / 2]
                data.addObject(
                    classes[int(args[0])],
                    pmin[0],
                    pmin[1],
                    pmax[0],
                    pmax[1]
                )
        return data

    def write(self, path):
        # cpath = changeTargetFile(path, 'classes.txt')
        # try:
        #     with open(cpath) as f:
        #         for line in f.readlines():
        #             classes.append(line)
        # except:
        #     raise Exception("Missing classes.txt file")
        classes = []
        with open(changeExt(path, 'txt'), 'w') as f:
            for obj in self._data.objects():
                # objClass = None
                # for i in range(len(classes)):
                #     if obj.name() == classes[i].replace("\n", ""):
                #         objClass = i
                #         break
                # if objClass is None:
                #     raise Exception(f"Class not found for element with name: {obj.name()}")
                objClass = obj.name()
                if not objClass in classes:
                    classes.append(objClass)
                    print("\n" + str(classes))
                objName = classes.index(objClass)
                width = obj.maxX() - obj.minX()
                height = obj.maxY() - obj.minY()
                center = [obj.maxX() - width / 2, obj.maxY() - height / 2]
                f.write(
                    f"{objName} {center[0] / self._data.width()} {center[1] / self._data.height()} {width / self._data.width()} {height / self._data.height()}\n")
        classes_path = changeTargetFile(path, 'classes.txt')
        with open(classes_path, "w") as f:
            text = ""
            for name in classes:
                text += name + "\n"
            text = text[:len(text)-1]
            f.write(text)