"""Gera dataset sintético reproduzível."""
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path("data") / "processed.csv"
OUT.parent.mkdir(exist_ok=True)

rng = np.random.default_rng(42)
n = 3000
df = pd.DataFrame({
    "x1": rng.normal(size=n),
    "x2": rng.normal(size=n),
    "x3": rng.uniform(0, 1, n),
})
df["y"] = ((0.7 * df["x1"] - 0.3 * df["x2"] + 0.5 * df["x3"]) > 0).astype(int)
df.to_csv(OUT, index=False)
print(f"Dataset salvo em {OUT} ({len(df)} linhas)")
