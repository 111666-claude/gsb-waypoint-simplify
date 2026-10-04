"""航点序列简化：按容差和节点预算抽稀，首尾永不删。"""


class Route:
    """航点序列。"""

    def __init__(self, tolerance=0, max_points=100):
        self.tolerance = tolerance
        self.max_points = max_points
        self.points = []
        self._ids = set()
        self.recomputed = 0
        self.scanned = 0
        self._cache = None

    def add(self, point_id, x, y):
        """加入一个航点；同一 point_id 重复加入返回 False 且不改变序列。"""
        if point_id in self._ids:
            return False
        self._ids.add(point_id)
        self.points.append((point_id, x, y))
        self._cache = None
        return True

    def size(self):
        return len(self.points)

    def simplify(self):
        """返回简化后的航点 id 列表，首尾恒在且保持原顺序。

        序列未变化时直接返回缓存结果，不全扫历史航点。
        """
        if self._cache is not None:
            return list(self._cache)
        points = self.points
        self.scanned += len(points)
        if len(points) <= 2:
            result = [point[0] for point in points]
            self._cache = result
            return list(result)
        kept = [0]
        for index in range(1, len(points) - 1):
            distance = self._distance(points[index], points[index - 1], points[index + 1])
            if distance > self.tolerance:
                kept.append(index)
        kept.append(len(points) - 1)
        if len(kept) > self.max_points:
            kept = self._apply_budget(points, kept)
        result = [points[index][0] for index in kept]
        self._cache = result
        return list(result)

    def _apply_budget(self, points, kept):
        """反复删当前垂直距离最小的中间点，直到不超 max_points。

        距离相同先加入（原始下标小）的先删；删完只按新邻居重算受影响的两点。
        """
        kept = list(kept)
        distances = {}
        for pos in range(1, len(kept) - 1):
            distances[kept[pos]] = self._distance(
                points[kept[pos]], points[kept[pos - 1]], points[kept[pos + 1]]
            )
        while len(kept) > self.max_points:
            best_pos = None
            best_key = None
            for pos in range(1, len(kept) - 1):
                key = (distances[kept[pos]], kept[pos])
                if best_key is None or key < best_key:
                    best_key = key
                    best_pos = pos
            if best_pos is None:
                break
            del distances[kept.pop(best_pos)]
            for pos in (best_pos - 1, best_pos):
                if 0 < pos < len(kept) - 1:
                    distances[kept[pos]] = self._distance(
                        points[kept[pos]], points[kept[pos - 1]], points[kept[pos + 1]]
                    )
                    self.recomputed += 1
        return kept

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
