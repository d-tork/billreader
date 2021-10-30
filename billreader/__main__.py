import json
import argparse

from billreader import FileChecker
from billreader.power import DominionEnergyBill
from billreader.water import FairfaxWaterBill


def parse_cli_args():
    parser = argparse.ArgumentParser(description='Extract values from utility bills.')
    parser.add_argument('filepath', type=str,
                        help='Filepath of pdf')
    args = parser.parse_args()
    return args


def main():
    args = parse_cli_args()
    print(f'Filepath passed: {args.filepath}')
    provider = FileChecker(filepath=args.filepath).determine_utility_provider()
    if provider == 'dominion_energy':
        bill = DominionEnergyBill(filepath=args.filepath)
    elif provider == 'fairfax_water':
        bill = FairfaxWaterBill(filepath=args.filepath)
    else:
        raise ValueError(f'Provider name not valid: {provider}')
    bill_data = bill.parse_bill()
    add_to_output(output_path='output.json', data=bill_data)


def add_to_output(output_path: str, data: dict):
    """Append the new data to the output file."""
    with open(output_path, 'a') as f:
        f.write('\n')
        json.dump(data, f)


if __name__ == '__main__':
    main()
