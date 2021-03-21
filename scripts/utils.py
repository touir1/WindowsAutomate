class Point:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y


class ImagePosition:
    center = Point(0, 0)
    min = Point(0, 0)
    max = Point(0, 0)

    def __init__(self, x_center, y_center, x_min, y_min, x_max, y_max):
        self.center = Point(x_center, y_center)
        self.min = Point(x_min, y_min)
        self.max = Point(x_max, y_max)


def in_vicinity(x, y, x_min, y_min, x_max, y_max):
    return x_min <= x <= x_max and y_min <= y <= y_max


def in_vicinity_pt(pt: Point, min: Point, max: Point):
    return in_vicinity(pt.x, pt.y, min.x, min.y, max.x, max.y)


def overlapping_rect(min_1: Point, max_1: Point, min_2: Point, max_2: Point):
    # If one rectangle is on left side of other
    if min_1.x >= max_2.x or min_2.x >= max_1.x:
        return False
    # If one rectangle is above other
    if min_1.y <= max_2.y or min_2.y <= max_1.y:
        return False
    return True
