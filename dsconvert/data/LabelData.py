from .BoundingBox import BoundingBox

class LabelData:
    def __init__(self, path, imageWidth, imageHeight):
        self.path = path
        self.width = int(imageWidth)
        self.height = int(imageHeight)
        self.objects = []

    def filter_classes(self, classes):
        contains_accepted_class = False
        for obj in self.objects:
            if obj.name() in classes:
                contains_accepted_class = True
                break
        return contains_accepted_class

    def addObject(self, name, minX, minY, maxX, maxY):
        self.objects.append(BoundingBox(name, minX, minY, maxX, maxY))

    def show(self):
        print(f"Image Path: {self.path}")
        print(f"Width: {self.imageWidth}")
        print(f"Height: {self.imageHeight}")
        print(f"Objects: ")
        for obj in self.objects:
            obj.print()
