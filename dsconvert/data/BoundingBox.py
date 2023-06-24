class BoundingBox:
    def __init__(self, name, minX, minY, maxX, maxY):
        self.name = str(name)
        self.minX = float(minX)
        self.minY = float(minY)
        self.maxX = float(maxX)
        self.maxY = float(maxY)

    def print(self):
        print(f"{self.name}:")
        print(f"minX: {self.minX}")
        print(f"minY: {self.minY}")
        print(f"maxX: {self.maxX}")
        print(f"maxY: {self.maxY}")

    def insertion(self, box2):
        xMin = max(self.minX, box2.minX)
        yMin = max(self.minY, box2.minY)
        xMax = min(self.maxX, box2.maxX)
        yMax = min(self.maxY, box2.maxY)
        if xMin > xMax or yMin > yMax or xMax < xMin or yMax < yMin:
            return 0.0
        width = xMax - xMin
        height = yMax - yMin
        return max(0.0, width * height)
