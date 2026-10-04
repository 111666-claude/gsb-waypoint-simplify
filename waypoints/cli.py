"""命令行入口：跑航点简化样例。"""

import argparse

from .core import Route


def build_parser():
    parser = argparse.ArgumentParser(prog="waypoint-simplify", description="航点序列简化")
    parser.add_argument("--sample", default="first", help="first / tolerance / dup / scan")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.sample == "first":
        route = Route(tolerance=0)
        route.add("p1", 0, 0)
        route.add("p2", 1, 0)
        route.add("p3", 3, 0)
        points = route.simplify()
        print("first=%s count=%d" % (points[0], len(points)))
    elif args.sample == "tolerance":
        route = Route(tolerance=5)
        route.add("p1", 0, 0)
        route.add("p2", 1, 5)
        route.add("p3", 2, 0)
        route.add("p4", 3, 5)
        route.add("p5", 4, 0)
        print("count=%d" % len(route.simplify()))
    elif args.sample == "dup":
        route = Route(tolerance=0)
        route.add("p1", 0, 0)
        route.add("p2", 5, 0)
        route.add("p1", 10, 0)
        print("points=%d" % route.size())
    elif args.sample == "scan":
        route = Route(tolerance=0)
        for index in range(3000):
            route.add("p-%d" % index, index, 0)
        for _ in range(3000):
            route.simplify()
        print("scanned=%d" % route.scanned_count())
    else:
        raise SystemExit("需要 --sample first|tolerance|dup|scan")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
