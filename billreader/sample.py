"""
Run the script on example file included.
"""
import json
from os import path

from billreader.power import DominionEnergyBill
from billreader.water import FairfaxWaterBill

DOCKER_SAMPLE_PATH = path.join('/', 'bill-pdfs', 'samples')


def sample():
    sample_path_power = path.join(DOCKER_SAMPLE_PATH, 'power_2021-10-07.pdf')
    dominion_bill = DominionEnergyBill(filepath=sample_path_power).parse_bill()
    print(json.dumps(dominion_bill, indent=2))

    sample_path_water = path.join(DOCKER_SAMPLE_PATH, 'water_2021-09-07.pdf')
    fairfax_bill = FairfaxWaterBill(filepath=sample_path_water).parse_bill()
    print(json.dumps(fairfax_bill, indent=2))
