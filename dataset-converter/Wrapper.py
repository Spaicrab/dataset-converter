import os, glob, imagesize
import xml.etree.ElementTree as et

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
            raise Exception("Missing classes.txt file for YOLOWrapper")
        label_path = findByExtList(img_path, ['txt'])
        if label_path == None:
            return
        width, height = imagesize.get(img_path)
        data = data = LabelData(
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

    def write_directory(self, dir_path, data_list):
        dir_path = fixPath(dir_path)
        os.makedirs(dir_path, exist_ok=True)
        to_parse = len(data_list)
        parsed = 0
        classes = []
        for data in data_list:
            img_name = os.path.basename(data.path())
            path = dir_path + "/" + img_name
            classes = self.write(path, data, classes)

    def write(self, path, data, classes):
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
        return classes

class VOCWrapper(Wrapper):
    def ext(self):
        return "xml"

    def read(self, img_path):
        label_path = findByExtList(img_path, ['xml'])
        if label_path == None:
            return
        xml = et.parse(label_path).getroot()
        data = LabelData(
            xml.find("path").text,
            xml.find("size").find("width").text,
            xml.find("size").find("height").text,
        )
        for objj in xml.findall("object"):
            obj = objj.find("bndbox")
            data.addObject(
                objj.find("name").text,
                obj.find("xmin").text,
                obj.find("ymin").text,
                obj.find("xmax").text,
                obj.find("ymax").text,
            )
        return data

    def write(self, path, data):
        xml = et.Element('annotation')
        split_path = path.split("/")
        self.__xmlAdd(xml, "folder", path.split("/")[len(split_path) - 2])
        filename = split_path[-1].split(".")
        filename = filename[len(filename) - 2]
        self.__xmlAdd(xml, 'filename', f"{filename}.jpg")
        self.__xmlAdd(xml, 'path', path.replace(split_path[-1], f"{filename}.jpg"))
        size = et.SubElement(xml, 'size')
        self.__xmlAdd(size, 'width', data.width())
        self.__xmlAdd(size, 'height', data.height())
        self.__xmlAdd(size, 'depth', 3)
        self.__xmlAdd(xml, 'segmented', 0)
        for obj in data.objects():
            xmlObj = et.SubElement(xml, 'object')
            self.__xmlAdd(xmlObj, 'name', obj.name())
            self.__xmlAdd(xmlObj, 'pose', 'Unspecified')
            self.__xmlAdd(xmlObj, 'truncated', 0)
            self.__xmlAdd(xmlObj, 'difficult', 0)
            box = et.SubElement(xmlObj, 'bndbox')
            self.__xmlAdd(box, 'xmin', int(obj.minX()))
            self.__xmlAdd(box, 'ymin', int(obj.minY()))
            self.__xmlAdd(box, 'xmax', int(obj.maxX()))
            self.__xmlAdd(box, 'ymax', int(obj.maxY()))
        with open(path.replace(split_path[-1], f"{filename}.xml"), "wb") as f:
            f.write(et.tostring(xml))

    def __xmlAdd(self, xml, key, value):
        el = et.SubElement(xml, key)
        el.text = str(value)