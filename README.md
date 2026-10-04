# waypoint-simplify

航点序列简化：按容差和节点预算抽稀，首尾永不删，只用 Python 标准库。

```
python3 -m waypoints.cli --sample first
python3 -m waypoints.cli --sample tolerance
python3 -m waypoints.cli --sample budget
python3 -m waypoints.cli --sample dup
python3 -m waypoints.cli --sample scan
python3 -m unittest discover -s tests -v
```

## 口径（README 为准）

- **首尾保留**：第一个和最后一个航点永不删，简化结果保持原有先后顺序。
- **容差**：中间点到相邻两点连线的垂直距离不大于 `tolerance` 就删掉，正好等于 `tolerance` 也算以内。
- **节点预算**：按容差删完之后节点数仍超过 `max_points` 时，继续反复删掉当前垂直距离最小的中间点
  （删完要按新邻居重算受影响那两点的距离），直到节点数不超过 `max_points`；距离相同时先加入的先删。
- **幂等**：同一个 `point_id` 只加入一次，重复加入返回 False 且不改变序列。
- **增量**：删点只重算受影响的相邻两点，`recomputed_count()` 不随航点数乘操作次数增长。
- **代价**：`simplify` 不许每次全扫历史航点，`scanned_count()` 不随航点数乘简化次数增长。
- **不变量**：首尾恒在；节点数超过 `max_points` 时简化结果不超过 `max_points`；同一序列重复简化结果相同。

## 输出契约（不改格式）

```
first=.. count=..
count=..
points=..
scanned=..
```

## 目录

```
waypoints/core.py   容差、节点预算与增量重算
waypoints/cli.py    命令行入口
tests/              unittest 用例
```
