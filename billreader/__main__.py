import json
import argparse
import os
from os import path

from billreader import (
    FileChecker, Bill,
    PROJ_ROOT, DATA_ROOT,
    log
)
from billreader.power import DominionEnergyBill
from billreader.water import FairfaxWaterBill


config_yaml = path.join(PROJ_ROOT, 'logging.yml')
logger = log.log_setup(config_yaml=config_yaml, logger_name='main')


def main():
    args = parse_cli_args()
    logger.info(f'Filepath passed: {args.filepath}')
    file_checker = FileChecker(filepath=args.filepath, bind_path=DATA_ROOT)
    try:
        provider = file_checker.determine_utility_provider()
    except ValueError:
        logger.exception()
    else:
        if provider == 'dominion_energy':
            bill = DominionEnergyBill(filepath=file_checker.filepath)
        elif provider == 'fairfax_water':
            bill = FairfaxWaterBill(filepath=file_checker.filepath)
        else:
            raise ValueError(f'Provider name not valid: {provider}')

    logger.info('Parsing bill')
    bill_data = bill.parse_bill()
    logger.info('Bill parsing complete.')

    rename_bill_file(bill=bill, bill_date=bill_data.get('bill_date'))

    write_output(bill_data=bill_data)
    return


def parse_cli_args():
    parser = argparse.ArgumentParser(description='Extract values from utility bills.')
    parser.add_argument('filepath', type=str,
                        help='Filepath of pdf')
    args = parser.parse_args()
    return args


def rename_bill_file(bill: Bill, bill_date: str):
    """Standardizes the filename."""
    old_path = bill.filepath
    new_filename = f'{bill.utility_type}_{bill_date}.pdf'
    new_path = path.join(DATA_ROOT, new_filename)
    logger.info(f'Moving {old_path} to {new_path}')
    os.rename(old_path, new_path)
    # TODO: ensure this doesn't trigger another action


def write_output(bill_data: dict):
    output_path = path.join(DATA_ROOT, 'parse_output.json')
    logger.info(f'Writing output to {output_path}.')
    add_to_output(output_path=output_path, data=bill_data)
    logger.info('Output file written.')


def add_to_output(output_path: str, data: dict):
    """Append the new data to the output file."""
    with open(output_path, 'a') as f:
        f.write('\n')
        json.dump(data, f)


if __name__ == '__main__':
    main()
