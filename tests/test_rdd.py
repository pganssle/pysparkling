from pysparkling import Context

import unittest


class RDDTest(unittest.TestCase):
    """ Tests for the resilient distributed databases """

    def setUp(self):
        self.context = Context()

    def testLeftOuterJoinSimple(self):
        """ Test the basic left outer join with simple key-value pairs """
        x = self.context.parallelize([('a', 'xa'), ('b', 'xb'), ('c', 'xc')])
        y = self.context.parallelize([('b', 'yb'), ('c', 'yc')])
        z = self.context.parallelize([('c', 'zc'), ('d', 'zd')])

        xy = sorted(x.leftOuterJoin(y).collect())
        xz = sorted(x.leftOuterJoin(z).collect())
        zx = sorted(z.leftOuterJoin(x).collect())

        self.assertEqual(xy, [('a', ('xa', None)),
                              ('b', ('xb', 'yb')),
                              ('c', ('xc', 'yc'))])

        self.assertEqual(xz, [('a', ('xa', None)),
                              ('b', ('xb', None)),
                              ('c', ('xc', 'zc'))])

        self.assertEqual(zx, [('c', ('zc', 'xc')),
                              ('d', ('zd', None))])

    def testLeftOuterJoinDuplicate(self):
        """ Test the left outer join with duplicate keys """
        x = self.context.parallelize([('a', 'xa'), ('c', 'xc1'), ('c', 'xc2')])
        y = self.context.parallelize([('b', 'yb'), ('c', 'yc')])
        z = self.context.parallelize([('c', 'zc1'), ('c', 'zc2'), ('d', 'zd')])

        xy = sorted(x.leftOuterJoin(y).collect())
        xz = sorted(x.leftOuterJoin(z).collect())

        self.assertEqual(xy, [('a', ('xa', None)),
                              ('c', ('xc1', 'yc')),
                              ('c', ('xc2', 'yc'))])

        # Two sets of duplicate keys gives cartesian product
        self.assertEqual(xz, [('a', ('xa', None)),
                              ('c', ('xc1', 'zc1')),
                              ('c', ('xc1', 'zc2')),
                              ('c', ('xc2', 'zc1')),
                              ('c', ('xc2', 'zc2'))])

    def testRightOuterJoinSimple(self):
        """ Test the basic right outer join with simple key-value pairs """
        x = self.context.parallelize([('a', 'xa'), ('b', 'xb'), ('c', 'xc')])
        y = self.context.parallelize([('b', 'yb'), ('c', 'yc')])
        z = self.context.parallelize([('c', 'zc'), ('d', 'zd')])

        xy = sorted(x.rightOuterJoin(y).collect())
        xz = sorted(x.rightOuterJoin(z).collect())
        zx = sorted(z.rightOuterJoin(x).collect())

        self.assertEqual(xy, [('b', ('xb', 'yb')),
                              ('c', ('xc', 'yc'))])

        self.assertEqual(xz, [('c', ('xc', 'zc')),
                              ('d', (None, 'zd'))])

        self.assertEqual(zx, [('a', (None, 'xa')),
                              ('b', (None, 'xb')),
                              ('c', ('zc', 'xc'))])

    def testRightOuterJoinDuplicate(self):
        """ Test the right outer join with duplicate keys """
        x = self.context.parallelize([('a', 'xa'), ('c', 'xc1'), ('c', 'xc2')])
        y = self.context.parallelize([('b', 'yb'), ('c', 'yc')])
        z = self.context.parallelize([('c', 'zc1'), ('c', 'zc2'), ('d', 'zd')])

        xy = sorted(x.rightOuterJoin(y).collect())
        xz = sorted(x.rightOuterJoin(z).collect())

        self.assertEqual(xy, [('b', (None, 'yb')),
                              ('c', ('xc1', 'yc')),
                              ('c', ('xc2', 'yc'))])

        # Two sets of duplicate keys gives cartesian product
        self.assertEqual(xz, [('c', ('xc1', 'zc1')),
                              ('c', ('xc1', 'zc2')),
                              ('c', ('xc2', 'zc1')),
                              ('c', ('xc2', 'zc2')),
                              ('d', (None, 'zd'))])

    def testFullOuterJoinSimple(self):
        """ Test the basic full outer join with simple key-value pairs """
        x = self.context.parallelize([('a', 'xa'), ('b', 'xb'), ('c', 'xc')])
        y = self.context.parallelize([('b', 'yb'), ('c', 'yc')])
        z = self.context.parallelize([('c', 'zc'), ('d', 'zd')])

        xy = sorted(x.fullOuterJoin(y).collect())
        xz = sorted(x.fullOuterJoin(z).collect())
        zx = sorted(z.fullOuterJoin(x).collect())

        self.assertEqual(xy, [('a', ('xa', None)),
                              ('b', ('xb', 'yb')),
                              ('c', ('xc', 'yc'))])

        self.assertEqual(xz, [('a', ('xa', None)),
                              ('b', ('xb', None)),
                              ('c', ('xc', 'zc')),
                              ('d', (None, 'zd'))])

        self.assertEqual(zx, [('a', (None, 'xa')),
                              ('b', (None, 'xb')),
                              ('c', ('zc', 'xc')),
                              ('d', ('zd', None))])

    def testFullOuterJoinDuplicate(self):
        """ Test the full outer join with duplicate keys """
        x = self.context.parallelize([('a', 'xa'), ('c', 'xc1'), ('c', 'xc2')])
        y = self.context.parallelize([('b', 'yb'), ('c', 'yc')])
        z = self.context.parallelize([('c', 'zc1'), ('c', 'zc2'), ('d', 'zd')])

        xy = sorted(x.fullOuterJoin(y).collect())
        xz = sorted(x.fullOuterJoin(z).collect())

        self.assertEqual(xy, [('a', ('xa', None)),
                              ('b', (None, 'yb')),
                              ('c', ('xc1', 'yc')),
                              ('c', ('xc2', 'yc'))])

        # Two sets of duplicate keys gives cartesian product
        self.assertEqual(xz, [('a', ('xa', None)),
                              ('c', ('xc1', 'zc1')),
                              ('c', ('xc1', 'zc2')),
                              ('c', ('xc2', 'zc1')),
                              ('c', ('xc2', 'zc2')),
                              ('d', (None, 'zd'))])

    def test_cartesian(self):
        x = self.context.parallelize(range(0, 2))
        y = self.context.parallelize(range(3, 6))
        c = x.cartesian(y)
        result = sorted(c.collect())
        expected = sorted([(0, 3), (0, 4), (0, 5), (1, 3), (1, 4), (1, 5)])
        self.assertListEqual(result, expected)

    def test_sample(self):
        rdd = self.context.parallelize(range(100), 4)
        self.assertTrue(6 <= rdd.sample(False, 0.1, 81).count() <= 14)

    def test_sampleByKey(self):
        fractions = {"a": 0.2, "b": 0.1}
        range_rdd = self.context.parallelize(range(0, 1000))
        rdd = self.context.parallelize(fractions.keys()).cartesian(range_rdd)
        sample = dict(
            rdd.sampleByKey(False, fractions, 2).groupByKey().collect()
        )
        self.assertTrue(100 < len(sample["a"]) < 300 and
                        50 < len(sample["b"]) < 150)
        self.assertTrue(max(sample["a"]) <= 999 and min(sample["a"]) >= 0)
        self.assertTrue(max(sample["b"]) <= 999 and min(sample["b"]) >= 0)


if __name__ == "__main__":
    unittest.main()
