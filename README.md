# waypoint-simplify

航点序列简化：去掉与相邻连线偏离不超过容差的中间点，保留首尾，只用 Python 标准库。

```
python3 -m waypoints.cli --sample first
python3 -m waypoints.cli --sample tolerance
python3 -m waypoints.cli --sample dup
python3 -m waypoints.cli --sample scan
python3 -m unittest discover -s tests -v
```

## 口径（README 为准）

- **保留首尾**：简化结果的第一项必须是序列的第一个航点，最后一项必须是最后一个航点。
- **容差**：中间点到相邻两点连线的垂直距离不大于 `tolerance` 就删掉，正好等于容差也算偏离以内而被删。
- **单调不增**：简化结果的节点数不大于原序列，同一序列重复简化结果相同。
- **幂等**：同一个 `point_id` 只加入一次，重复加入不改变序列。
- **查询代价**：`simplify` 不许每次全扫历史航点，`scanned_count()` 不随航点数乘简化次数增长。
- **规模**：10 万航点、每秒 10 万次加入，单次摊还 O(航点数)。

## 输出契约（不改格式）

```
first=.. count=..
count=..
points=..
scanned=..
```

## 目录

```
waypoints/core.py   垂直距离、容差与首尾保留
waypoints/cli.py    命令行入口
tests/              unittest 用例
```
