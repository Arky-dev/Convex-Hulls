from datasets import DataSet
from hull import SweepingHull, OSHull, GiftWrappingHull

def main():
    print("CONVEX HULL PROJECT - DATASET SHOWCASE")
    print("The following demo will show examples of datasets and hulls calculated in the projet. Close the visualization window to go to the next visual.")
    _ = input("The seed can be updated manually in the code. Press enter to continue.")

    # --- DATASET A: Rotated Square ---
    print("--- 1. DATASET A: Rotated Square ---")
    print("Algorithm: Sweeping Hull")
    ds_a = DataSet(size=50, method='A', seed=10)
    ds_a.visualize()
    SweepingHull(ds_a).visualize()

    # --- DATASET B: Uniform Square ---
    print("--- 2. DATASET B: Uniform Square Distribution ---")
    print("Algorithm: Output Sensitive (Marriage-before-Conquest)")
    ds_b = DataSet(size=200, method='B', seed=42)
    ds_b.visualize()
    OSHull(ds_b).visualize()

    # --- DATASET C: Uniform Disk ---
    print("--- 3. DATASET C: Uniform Disk Distribution ---")
    print("Algorithm: Sweeping Hull")
    ds_c = DataSet(size=200, method='C', seed=99)
    ds_c.visualize()
    SweepingHull(ds_c).visualize()

    # --- DATASET D: Circle Boundary ---
    print("--- 4. DATASET D: Circle Boundary (Worst Case) ---")
    print("Algorithm: Gift Wrapping")
    ds_d = DataSet(size=30, method='D', seed=1)
    ds_d.visualize()
    GiftWrappingHull(ds_d).visualize()


if __name__ == '__main__':
    main()