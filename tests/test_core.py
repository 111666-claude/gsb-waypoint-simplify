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


if __name__ == "__main__":
    unittest.main()


class RouteSpecTest(unittest.TestCase):
    def test_first_and_last_kept_when_collinear(self):
        route = Route(0, 100)
        route.add("p1", 0, 0)
        route.add("p2", 1, 0)
        route.add("p3", 3, 0)
        result = route.simplify()
        self.assertEqual(result, ["p1", "p3"])
        self.assertEqual(result[0], "p1")
        self.assertEqual(result[-1], "p3")

    def test_order_preserved(self):
        route = Route(0, 100)
        route.add("p1", 0, 0)
        route.add("p2", 1, 5)
        route.add("p3", 2, 0)
        self.assertEqual(route.simplify(), ["p1", "p2", "p3"])

    def test_tolerance_boundary_equal_removed(self):
        route = Route(5, 100)
        route.add("p1", 0, 0)
        route.add("p2", 1, 5)
        route.add("p3", 2, 0)
        self.assertEqual(route.simplify(), ["p1", "p3"])

    def test_tolerance_above_kept(self):
        route = Route(5, 100)
        route.add("p1", 0, 0)
        route.add("p2", 1, 6)
        route.add("p3", 2, 0)
        self.assertEqual(route.simplify(), ["p1", "p2", "p3"])

    def test_budget_caps_result(self):
        route = Route(0, 4)
        for index in range(10):
            route.add("p%d" % index, index, 10 if index % 2 else 0)
        result = route.simplify()
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], "p0")
        self.assertEqual(result[-1], "p9")

    def test_budget_tie_removes_earliest_first(self):
        route = Route(0, 3)
        route.add("p1", 0, 0)
        route.add("p2", 1, 1)
        route.add("p3", 2, 1)
        route.add("p4", 3, 0)
        result = route.simplify()
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], "p1")
        self.assertEqual(result[-1], "p4")

    def test_duplicate_add_rejected(self):
        route = Route(0, 100)
        self.assertTrue(route.add("p1", 0, 0))
        self.assertTrue(route.add("p2", 5, 0))
        self.assertFalse(route.add("p1", 10, 0))
        self.assertEqual(route.size(), 2)
        self.assertEqual(route.simplify(), ["p1", "p2"])

    def test_repeated_simplify_consistent_and_cached(self):
        route = Route(0, 100)
        for index in range(50):
            route.add("p%d" % index, index, index % 3)
        first = route.simplify()
        second = route.simplify()
        self.assertEqual(first, second)
        self.assertEqual(route.scanned_count(), 50)

    def test_scanned_not_growing_with_simplify_count(self):
        route = Route(0, 100000)
        for index in range(300):
            route.add("p-%d" % index, index, 0)
        for _ in range(300):
            route.simplify()
        self.assertEqual(route.scanned_count(), 300)

    def test_recomputed_only_from_budget_removals(self):
        route = Route(0, 100)
        for index in range(20):
            route.add("p%d" % index, index, 0)
        route.simplify()
        self.assertEqual(route.recomputed_count(), 0)


if __name__ == "__main__":
    unittest.main()
