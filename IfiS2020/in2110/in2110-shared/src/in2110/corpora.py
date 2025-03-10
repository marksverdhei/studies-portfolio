import os
from pathlib import Path
from .norec import Norec
from .nak import NAK


IN2110_PATH = Path(os.environ['IN2110_PATH'])
DATA_PATH = IN2110_PATH / "data"
NOREC_DATA = DATA_PATH / "norec.zip"
NOREC_METADATA = DATA_PATH / "norec-metadata.json"

NAK_10_NN = DATA_PATH / "avis-10.s.gz"

norec = Norec(NOREC_DATA, NOREC_METADATA)
aviskorpus_10_nn = NAK(NAK_10_NN)
