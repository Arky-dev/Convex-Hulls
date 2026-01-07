from datasets import DataSet
from hull import SweepingHull


dataset = DataSet(size=101, method='B', seed=42)
dataset.visualize()

hull = SweepingHull(dataset)

hull.visualize()