from collections.abc import Iterator
from pathlib import Path
import pandas as pd

def read_csv_chunks(path: str | Path, chunksize: int = 250_000) -> Iterator[pd.DataFrame]:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    yield from pd.read_csv(path, chunksize=chunksize)

def read_csv(path: str | Path, nrows: int | None = None) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    return pd.read_csv(path, nrows=nrows)
