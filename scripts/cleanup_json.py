import os
import json

raw_dir = "raw_data"
if not os.path.exists(raw_dir):
    print("No raw_eu directory.")
    exit()

files = [f for f in os.listdir(raw_dir) if f.endswith(".json")]
print(f"Checking {len(files)} files...")

deleted = 0
for f in files:
    path = os.path.join(raw_dir, f)
    try:
        with open(path, "r", encoding="utf-8") as jf:
            json.load(jf)
    except Exception as e:
        print(f"Delete invalid: {f} - {e}")
        os.remove(path)
        deleted += 1

print(f"Cleanup complete. Deleted {deleted} invalid files.")
