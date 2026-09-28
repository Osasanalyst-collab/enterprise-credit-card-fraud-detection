from pathlib import Path
for folder in ["data/raw","data/interim","data/processed","data/samples","artifacts/models","logs"]: Path(folder).mkdir(parents=True,exist_ok=True)
print("Environment folders created. Next: pip install -r requirements-dev.txt")
