import unittest

from waypoints.core import Route


class RouteTest(unittest.TestCase):
    def test_single_point_kept(self):
        route = Route(0, 100)
        route.add("p1", 0, 0)
        self.assertEqual(route.simplify(), ["p1"])

    def test_two_points_kept(self):
        route = Route(0, 100)
        route.add("p1", 0, 0)
        route.add("p2", 5, 0)
        self.assertEqual(route.simplify(), ["p1", "p2"])

    def test_last_point_kept(self):
        route = Route(0, 100)
        route.add("p1", 0, 0)
        route.add("p2", 5, 5)
        route.add("p3", 10, 0)
        self.assertEqual(route.simplify()[-1], "p3")

    def test_counters_start_at_zero(self):
        route = Route(0, 100)
        self.assertEqual(route.scanned_count(), 0)
        self.assertEqual(route.recomputed_count(), 0)

    def test_first_and_last_kept_collinear(self):
        route = Route(0, 100)
        route.add("p1", 0, 0)
        route.add("p2", 1, 0)
        route.add("p3", 3, 0)
        self.assertEqual(route.simplify(), ["p1", "p3"])

    def test_order_preserved(self):
        route = Route(0, 2)
        for index in range(6):
            route.add("p%d" % index, index, index % 2)
        result = route.simplify()
        self.assertEqual(result, ["p0", "p5"])

    def test_tolerance_equal_is_within(self):
        # p2、p4 到邻点连线的垂直距离正好等于 5。
        route = Route(5, 100)
        route.add("p1", 0, 0)
        route.add("p2", 1, 5)
        route.add("p3", 2, 0)
        route.add("p4", 3, 5)
        route.add("p5", 4, 0)
        self.assertEqual(route.simplify(), ["p1", "p5"])

    def test_tolerance_just_above_kept(self):
        route = Route(4, 100)
        route.add("p1", 0, 0)
        route.add("p2", 1, 5)
        route.add("p3", 2, 0)
        self.assertEqual(route.simplify(), ["p1", "p2", "p3"])

    def test_budget_limits_count(self):
        route = Route(0, 4)
        for index in range(10):
            route.add("p%d" % index, index, 10 if index % 2 else 0)
        result = route.simplify()
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], "p0")
        self.assertEqual(result[-1], "p9")

    def test_budget_removes_smallest_distance_first(self):
        # p2 距离 1（先删），p3 距离 5（后删）；预算 3 时 p3 应保留。
        route = Route(0, 3)
        route.add("p1", 0, 0)
        route.add("p2", 1, 1)
        route.add("p3", 2, 5)
        route.add("p4", 3, 0)
        self.assertEqual(route.simplify(), ["p1", "p3", "p4"])

    def test_budget_tie_insertion_order_first(self):
        # p2、p3 距离相等（均为 5），先加入的 p2 先删。
        route = Route(0, 3)
        route.add("p1", 0, 0)
        route.add("p2", 1, 5)
        route.add("p3", 2, 5)
        route.add("p4", 3, 0)
        self.assertEqual(route.simplify(), ["p1", "p3", "p4"])

    def test_duplicate_id_rejected(self):
        route = Route(0, 100)
        self.assertTrue(route.add("p1", 0, 0))
        self.assertTrue(route.add("p2", 5, 0))
        self.assertFalse(route.add("p1", 10, 0))
        self.assertEqual(route.size(), 2)
        self.assertEqual(route.simplify(), ["p1", "p2"])

    def test_repeated_simplify_same_result(self):
        route = Route(1, 4)
        for index in range(8):
            route.add("p%d" % index, index, index % 2 * 3)
        self.assertEqual(route.simplify(), route.simplify())

    def test_scanned_not_per_simplify(self):
        route = Route(0, 100000)
        for index in range(3000):
            route.add("p-%d" % index, index, 0)
        for _ in range(3000):
            route.simplify()
        self.assertLessEqual(route.scanned_count(), 6000)

    def test_recomputed_incremental(self):
        route = Route(0, 100000)
        for index in range(3000):
            route.add("p-%d" % index, index, 0)
        route.simplify()
        # 删 2998 个中间点，每次只重算受影响相邻点，总量是线性级。
        self.assertLessEqual(route.recomputed_count(), 6000)


if __name__ == "__main__":
    unittest.main()
