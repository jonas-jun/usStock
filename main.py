import copy
from sconf import Config
from utils import pprint_config
from estimator import getTargetPrice

if __name__ == "__main__":
    # load format file
    cfg = "format.yaml"
    cfg = Config(cfg)
    print(">> initialized data")
    pprint_config(cfg)
    data = copy.deepcopy(cfg)
    # build estimator
    data = getTargetPrice(data=data)
    # estimating
    print("\n\n>> Calculating...")
    data.calc_all()
    pprint_config(data.data)
