# run_all.py
# Rebuild the processed data, tables and charts, and check them against the verified numbers.
import runpy
import time
from pathlib import Path

src = Path(__file__).resolve().parent
proc = src.parent / "data/processed"
steps = ["01_load_combine.py", "03_clean.py", "04_reversals.py", "05_analysis.py", "06_returns_customers.py", "07_forecast.py"]
for name in steps:
    if name == "01_load_combine.py" and (proc / "online_retail_combined.csv").exists():
        print("Skipping", name, "- combined CSV already exists (delete it to rebuild from Excel)")
        continue
    print("\n=== Running", name, "===")
    t = time.time()
    runpy.run_path(str(src / name), run_name="__main__")
    print("Finished", name, "in", round(time.time() - t), "seconds")
print("\nPIPELINE COMPLETE: every check passed")
