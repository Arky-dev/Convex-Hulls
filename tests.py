import unittest
import math
from datasets import DataSet
import copy
from hull import Hull, SweepingHull, OSHull, GiftWrappingHull

class TestGeometry(unittest.TestCase):
    """Tests for the fundamental geometric operations."""

    def setUp(self):
        self.ds = DataSet(size=0)
        self.hull_instance = Hull(self.ds)
        self.hull_instance.dataset.x_list = [0, 1, 0, 2]
        self.hull_instance.dataset.y_list = [0, 0, 1, 2]

    def test_orientation_ccw(self):
        # Checks the orientation method for an expected Counter-Clockwise turn
        res = self.hull_instance.orient(0, 1, 2)
        self.assertEqual(res, 1, "Should return 1 for Counter-Clockwise turn")

    def test_orientation_cw(self):
        # Checks the orientation method for an expected Clockwise turn
        res = self.hull_instance.orient(0, 2, 1)
        self.assertEqual(res, -1, "Should return -1 for Clockwise turn")

    def test_orientation_collinear(self):
        # Checks the orientation method for an expected flat turn
        self.hull_instance.dataset.x_list = [0, 1, 2]
        self.hull_instance.dataset.y_list = [0, 1, 2]
        res = self.hull_instance.orient(0, 1, 2)
        self.assertEqual(res, 0, "Should return 0 for Collinear points")


class TestDatasets(unittest.TestCase):
    """Tests to ensure datasets follow their mathematical definitions."""

    def test_bounds(self):
        # Check that all points are within [0, 1] x [0, 1].
        for method in ['A', 'B', 'C', 'D']:
            ds = DataSet(size=50, method=method)
            for x, y in ds.dataset:
                self.assertTrue(0 <= x <= 1, f"X out of bounds in method {method}")
                self.assertTrue(0 <= y <= 1, f"Y out of bounds in method {method}")

    def test_dataset_A_corners(self):
        # Dataset A must contain extreme points, though rotated : we check that the convex hull is of size 4
        ds = DataSet(size=100, method='A')
        hull = SweepingHull(ds)
        self.assertTrue(len(hull.hull) <= 5, "Dataset A should effectively be a quadrilateral")
    
    def test_dataset_C_disk(self):
        """Points in C must lie strictly inside or on the disk."""
        ds = DataSet(size=50, method='C')
        center = 0.5
        radius = 0.5
        for x, y in ds.dataset:
            dist = math.sqrt((x - center)**2 + (y - center)**2)
            self.assertLessEqual(dist, radius, f"Point outside disk in method C: {dist}")

    def test_dataset_D_circularity(self):
        # Points in D must lie on the circle of radius .5
        ds = DataSet(size=50, method='D')
        center = 0.5
        radius = 0.5
        tolerance = 1e-9
        for x, y in ds.dataset:
            dist = math.sqrt((x - center)**2 + (y - center)**2)
            self.assertAlmostEqual(dist, radius, delta=tolerance, 
                                   msg="Point in Dataset D is not on the circle boundary")


class TestHullCorrectness(unittest.TestCase):
    """Tests the logic of the Hull algorithms."""

    def is_convex(self, hull_indices, dataset):
        # Helper function : Checks if hull as a list of indexes is convex
        if len(hull_indices) <= 3: 
            return True
        
        hull_obj = Hull(dataset)
        turns = []
        n = len(hull_indices)
        for i in range(n):
            p1 = hull_indices[i]
            p2 = hull_indices[(i+1) % n]
            p3 = hull_indices[(i+2) % n]
            turn = hull_obj.orient(p1, p2, p3)
            if turn != 0:
                turns.append(turn)
        
        return all(t == 1 for t in turns) or all(t == -1 for t in turns)

    def points_are_contained(self, hull_indices, dataset):
        # Helper function : Check that all points are inside the hull
        # For every edge of the hull, every point in the dataset must be 'left' (or 'right')
        hull_ops = Hull(dataset) 
        n_hull = len(hull_indices)
        
        for i in range(n_hull):
            u = hull_indices[i]
            v = hull_indices[(i + 1) % n_hull]
            
            for k in range(dataset.size):
                if hull_ops.orient(u, v, k) == -1:
                    return False
                    
        return True

    def test_trivial_hull(self):
        # Test on a simple Square + Center point: the center should not be in hull
        manual_points = [(0.2,0.2), (0.8,0.2), (0.8,0.8), (0.2,0.8), (0.5, 0.5)]
        ds = DataSet(method='list', list=manual_points)
        
        algos = [SweepingHull, OSHull, GiftWrappingHull]
        
        for AlgoClass in algos:
            ds_copy = copy.deepcopy(ds) 
            h = AlgoClass(ds_copy)
            
            self.assertNotIn((0.5, 0.5), [h.dataset.dataset[i] for i in h.hull], f"{AlgoClass.__name__} included the center point!")
            self.assertEqual(len(h.hull), 4, f"{AlgoClass.__name__} failed simple square test")

    def test_algorithm_consistency(self):
        # Checking that Sweeping and OSHull return the same set of points for the same random dataset.
        ds = DataSet(size=50, method='B')
        
        ds_sweep = copy.deepcopy(ds)
        ds_os = copy.deepcopy(ds)
        
        sweep_hull = SweepingHull(ds_sweep)
        os_hull = OSHull(ds_os)
        
        sweep_coords = set([(ds_sweep.x_list[i], ds_sweep.y_list[i]) for i in sweep_hull.hull])
        os_coords = set([(ds_os.x_list[i], ds_os.y_list[i]) for i in os_hull.hull])
        
        self.assertEqual(sweep_coords, os_coords, 
                         "Sweeping and OS algorithms produced different hulls!")

    def test_convexity_property(self):
        """Verify the mathematical property of convexity on a random set."""
        # This remains largely the same, but utilizing the class correctly
        ds = DataSet(size=30, method='C', seed=55)
        
        algos = [SweepingHull, OSHull, GiftWrappingHull]
        
        for AlgoClass in algos:
            ds_copy = copy.deepcopy(ds) 
            h = AlgoClass(ds_copy)
        
            self.assertTrue(self.is_convex(h.hull, DataSet(method='list', list=h.dataset.dataset)), f"{AlgoClass.__name__} result is not convex")

if __name__ == '__main__':
    unittest.main()