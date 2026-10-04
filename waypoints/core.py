"""航点序列简化：按容差和节点预算抽稀，首尾永不删。

缺陷：首个航点被丢掉、容差判定用不小于、节点预算完全没做、
同一个 point_id 重复加入照收、每次简化全扫航点。
"""


class Route:
    """航点序列。"""

    def __init__(self, tolerance=0, max_points=100):
        self.tolerance = tolerance
        self.max_points = max_points
        self.points = []
        self.recomputed = 0
        self.scanned = 0

    def add(self, point_id, x, y):
        """加入一个航点。缺陷：同 point_id 重复加入也照收。"""
        self.points.append((point_id, x, y))
        return True

    def size(self):
        return len(self.points)

    def simplify(self):
        """返回简化后的航点 id 列表。缺陷：丢首点、容差用不小于、不看预算、全扫航点。"""
        self.scanned += len(self.points)
        if len(self.points) <= 2:
            return [point[0] for point in self.points]
        out = []
        for index in range(1, len(self.points)):
            point = self.points[index]
            if index == len(self.points) - 1:
                out.append(point[0])
                continue
            distance = self._distance(point, self.points[index - 1], self.points[index + 1])
            if distance >= self.tolerance:
                out.append(point[0])
        return out

    def _distance(self, point, start, end):
        """点到相邻两点连线的垂直距离。"""
        x0, y0 = start[1], start[2]
        x1, y1 = end[1], end[2]
        px, py = point[1], point[2]
        dx = x1 - x0
        dy = y1 - y0
        length = (dx * dx + dy * dy) ** 0.5
        if length == 0:
            return ((px - x0) ** 2 + (py - y0) ** 2) ** 0.5
        return abs(dy * (px - x0) - dx * (py - y0)) / length

    def recomputed_count(self):
        return self.recomputed

    def scanned_count(self):
        return self.scanned
