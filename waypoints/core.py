"""航点序列简化：按容差和节点预算抽稀，首尾永不删。

增量维护：每个航点只在首次接入时被扫描一次，删点只重算受影响
相邻两点的距离；重复 simplify 直接命中缓存，不全扫历史航点。
"""

import heapq


class Route:
    """航点序列。"""

    def __init__(self, tolerance=0, max_points=100):
        self.tolerance = tolerance
        self.max_points = max_points
        self.points = []
        self.recomputed = 0
        self.scanned = 0
        self._ids = set()
        # 增量状态（在 simplify 中惰性接入）
        self._alive = []
        self._prev = []
        self._next = []
        self._dist = []
        self._version = []
        self._integrated = 0
        self._alive_count = 0
        self._tail = -1
        self._heap = []
        self._cached = None

    def add(self, point_id, x, y):
        """加入一个航点。同一 point_id 只加入一次，重复返回 False。"""
        if point_id in self._ids:
            return False
        self._ids.add(point_id)
        self.points.append((point_id, x, y))
        self._cached = None
        return True

    def size(self):
        return len(self.points)

    def simplify(self):
        """返回简化后的航点 id 列表。首尾恒在，结果保持原顺序。"""
        if self._cached is not None:
            return list(self._cached)
        self._integrate()
        # 容差阶段：垂直距离不大于 tolerance 的中间点删掉（等于也算）。
        while self._heap and self._heap[0][0] <= self.tolerance:
            entry = heapq.heappop(self._heap)
            if self._valid(entry):
                self._remove(entry[2])
        # 预算阶段：仍超 max_points 时反复删当前距离最小的中间点。
        while self._alive_count > self.max_points and self._heap:
            entry = heapq.heappop(self._heap)
            if self._valid(entry):
                self._remove(entry[2])
        out = []
        index = 0
        while index != -1:
            out.append(self.points[index][0])
            index = self._next[index]
        self._cached = out
        return list(out)

    def _integrate(self):
        """把新增航点接入增量结构，每个航点只扫描一次。"""
        while self._integrated < len(self.points):
            index = self._integrated
            self._integrated += 1
            self.scanned += 1
            self._alive.append(True)
            self._prev.append(-1)
            self._next.append(-1)
            self._dist.append(0.0)
            self._version.append(0)
            if self._tail == -1:
                self._tail = index
                self._alive_count = 1
                continue
            old_tail = self._tail
            self._prev[index] = old_tail
            self._next[old_tail] = index
            self._tail = index
            self._alive_count += 1
            if index >= 2:
                # 旧的尾点变成中间点，首次计算它的距离。
                self._set_dist(old_tail)

    def _set_dist(self, index):
        """计算中间点当前到相邻两点连线的垂直距离并入堆。"""
        prev_index = self._prev[index]
        next_index = self._next[index]
        distance = self._distance(
            self.points[index], self.points[prev_index], self.points[next_index]
        )
        self._dist[index] = distance
        self._version[index] += 1
        heapq.heappush(self._heap, (distance, index, index, self._version[index]))

    def _valid(self, entry):
        index = entry[2]
        return (
            self._alive[index]
            and self._prev[index] != -1
            and self._next[index] != -1
            and self._version[index] == entry[3]
        )

    def _remove(self, index):
        """删除中间点，只重算受影响相邻两点的距离。"""
        prev_index = self._prev[index]
        next_index = self._next[index]
        self._alive[index] = False
        self._next[prev_index] = next_index
        self._prev[next_index] = prev_index
        self._alive_count -= 1
        if self._prev[prev_index] != -1:
            self.recomputed += 1
            self._set_dist(prev_index)
        if self._next[next_index] != -1:
            self.recomputed += 1
            self._set_dist(next_index)

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
