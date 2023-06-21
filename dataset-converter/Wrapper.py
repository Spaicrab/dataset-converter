import os, glob, shutil, imagesize
import xml.etree.ElementTree as et
import datetime, json

from .data.LabelData import LabelData
from .PathUtil import *

class Wrapper:
    def ext(self):
        return None
    
    def read_directory(self, dir_path, recursive=False):
        data_list = []
        dir_path = fixPath(dir_path)
        file_condition = dir_path
        if recursive:
            file_condition += '/**/*.' + self.ext()
        else:
            file_condition += '/*.' + self.ext()
        for label_path in glob.iglob(file_condition, recursive=recursive):
            label_path = fixPath(label_path)
            imgPath = findByExtList(label_path, ['jpg', 'png'])
            if imgPath != None:
                data = self.read(label_path)
                if data != None:
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
            self.write_with_image(path, data)

    def write_with_image(self, path, data):
        imgPath = data.path()
        imgPath = findByExtList(imgPath, ['jpg', 'png'])
        if imgPath == None:
            raise Exception(f"Missing image file. - {imgPath}")
        shutil.copy(imgPath, os.path.dirname(path))
        self.write(path, data)

    def write(self, path, data):
        pass

class YOLOWrapper(Wrapper):
    def ext(self):
        return "txt"

    def read(self, label_path):
        classes = []
        try:
            cpath = changeTargetFile(label_path, 'classes.txt')
            with open(cpath) as f:
                for line in f.readlines():
                    classes.append(line.replace("\n", ""))
        except:
            raise Exception("Missing classes.txt file for YOLOWrapper")
        img_path = findByExtList(label_path, ['jpg', 'png'])
        if img_path == None:
            return None
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
            classes = self.write_with_image(path, data, classes)

    def write_with_image(self, path, data, classes):
        imgPath = data.path()
        imgPath = findByExtList(imgPath, ['jpg', 'png'])
        if imgPath == None:
            raise Exception(f"Missing image file. - {imgPath}")
        shutil.copy(imgPath, os.path.dirname(path))
        return self.write(path, data, classes)

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

    def read(self, label_path):
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
    
class CocoWrapper(Wrapper):
    def ext(self):
        return "json"

    def read(self, label_path):
        label = open(label_path)
        label_data = json.load(label)
        data = LabelData(
            label_path,
            label_data['images'][0]['width'],
            label_data['images'][0]['height']
        )
        for obj in label_data['annotations']:
            data.addObject(label_data['categories'][obj['category_id']]['name'], obj['bbox'][0], obj['bbox'][1], obj['bbox'][2], obj['bbox'][3])
        return data

    def write(self, path, data):
        imgPath = data.path()
        imgPath = findByExtList(imgPath, ['jpg', 'png'])
        info = {
            'description': 'Dataset converted with DatasetConverter',
            'url': '',
            'version': '1.0',
            'year': int(datetime.datetime.now().year),
            'contributor': 'DatasetConverter',
            'date_created': f'{datetime.datetime.now().year}/{datetime.datetime.now().month}/{datetime.datetime.now().day}'
        }
        licenses = []
        images = [
            {
                'file_name': imgPath.split("/")[-1],
                'height': data.height(),
                'width': data.width(),
                'id': 1
            }
        ]
        annotations = []
        categories = []
        idx = 0
        for obj in data.objects():
            cat = None
            for i in range(len(categories)):
                if categories[i]['name'].replace("\n", "") == obj.name().replace("\n",""):
                    cat = i
                    break
            if cat is None:
                categories.append({
                    'supercategory': obj.name(),
                    'id': len(categories),
                    'name': obj.name()
                })
                cat = len(categories)-1
            annotations.append({
                'segmentation': [],
                'area': (obj.maxX()-obj.minX())*(obj.maxY()-obj.minY()),
                'iscrowd': 0,
                'image_id': 1,
                'bbox': [
                    obj.minX(),
                    obj.minY(),
                    obj.maxX(),
                    obj.maxY()
                ],
                'category_id': cat,
                'id': idx
            })
            idx += 1
        data_to_write = {
            'info': info,
            'licenses': licenses,
            'images': images,
            'annotations': annotations,
            'categories': categories

        }
        f = open(changeExt(path, "json"), 'w')
        f.write(json.dumps(data_to_write, sort_keys=True, indent=4))