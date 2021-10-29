from os import path
import json

from billreader import PROJ_PATH
from billreader.power import DominionEnergyBill


def main():
    sample_path_power = path.join(PROJ_PATH, 'samples', 'power_2021-10-07.pdf')
    dominion_bill = DominionEnergyBill(filepath=sample_path_power).parse_bill()
    print(json.dumps(dominion_bill, indent=2))


if __name__ == '__main__':
    main()
