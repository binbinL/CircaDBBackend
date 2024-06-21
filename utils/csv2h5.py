import os
import pandas as pd
import h5py
from typing import List, Union


def csv2h5(gse: str, condition: List):
    path = f'C:\\Users\\15423\\OneDrive\\GSE\\done\\{gse}'
    #
    pd1 = pd.read_csv(os.path.join(path, 'D-Ala.csv'))
    pd2 = pd.read_csv(os.path.join(path, 'Vehicle.csv'))
