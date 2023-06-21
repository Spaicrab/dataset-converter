import os, glob, imagesize

from .data.LabelData import LabelData
from .PathUtil import *

class Wrapper:
    def read_directory(self, dir_path):
        data_list = []
        dir_path = fixPath(dir_path)
        for img_path in glob.iglob(dir_path + "/*.[jp][pn]g"):
            img_path = fixPath(img_path)
            data = self.read(img_path)
            data_list.append(data)
        return data_list

    def read(self, path):
        return None

    def write_directory(self, dir_path, data_list):
        dir_path = fixPath(dir_path)
        os.makedirs(dir_path, exist_ok=True)
        to_parse = len(data_list)
        parsed = 0
        for data in data_list:
            img_name = os.path.basename(data.path())
            path = dir_path + "/" + img_name
            self.write(path, data)

    def write(self, path, data):
        pass

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

    def write(self, path, data):
        classes = []
        with open(changeExt(path, 'txt'), 'w') as f:
            for obj in data.objects():
                objClass = obj.name()
                if not objClass in classes:
                    classes.append(objClass)
                objName = classes.index(objClass)
                width = obj.maxX() - obj.minX()
                height = obj.maxY() - obj.minY()
                center = [obj.maxX() - width / 2, obj.maxY() - height / 2]
                f.write(
                    f"{objName} {center[0] / data.width()} {center[1] / data.height()} {width / data.width()} {height / data.height()}\n")
        classes_path = changeTargetFile(path, 'classes.txt')
        with open(classes_path, "w") as f:
            text = ""
            for name in classes:
                text += name + "\n"
            text = text[:len(text)-1]
            f.write(text)