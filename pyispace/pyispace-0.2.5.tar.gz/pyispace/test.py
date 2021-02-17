import json
import pandas as pd
from pyispace.train import train_is


meta = pd.read_csv('/Users/pedropaiva/Documents/Doutorado/dev-workspace/metadata.csv', index_col='instances')

with open('/Users/pedropaiva/Documents/Doutorado/dev-workspace/options.json') as f:
    opts = json.load(f)

model = train_is(meta, opts)
