import json
import argparse
from os import path

from billreader import FileChecker, log
from billreader.power import DominionEnergyBill
from billreader.water import FairfaxWaterBill


config_yaml = path.join('/', 'bill-pdfs', 'logging.yml')
logger = log.log_setup(config_yaml=config_yaml, logger_name='main')


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

    logger.info('Parsing bill')
    bill_data = bill.parse_bill()
    logger.info('Bill parsing complete.')

    logger.info('Writing to output file.')
    add_to_output(output_path='output.json', data=bill_data)
    logger.info('Output file written.')


def add_to_output(output_path: str, data: dict):
    """Append the new data to the output file."""
    with open(output_path, 'a') as f:
        f.write('\n')
        json.dump(data, f)


if __name__ == '__main__':
    main()
