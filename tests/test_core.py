import unittest

from waypoints.core import Route


class RouteTest(unittest.TestCase):
    def test_single_point_kept(self):
        route = Route(0)
        route.add("p1", 0, 0)
        self.assertEqual(route.simplify(), ["p1"])

    def test_two_points_kept(self):
        route = Route(0)
        route.add("p1", 0, 0)
        route.add("p2", 5, 0)
        self.assertEqual(route.simplify(), ["p1", "p2"])

    def test_last_point_kept(self):
        route = Route(0)
        route.add("p1", 0, 0)
        route.add("p2", 5, 5)
        route.add("p3", 10, 0)
        self.assertEqual(route.simplify()[-1], "p3")

    def test_scanned_starts_at_zero(self):
        self.assertEqual(Route(0).scanned_count(), 0)


if __name__ == "__main__":
    unittest.main()
