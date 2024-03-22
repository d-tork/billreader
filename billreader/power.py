import re
import os
import yaml
from datetime import datetime, date

from billreader import Bill


class DominionEnergyBill(Bill):
    provider = 'Dominion Energy'
    utility_type = 'power'
    date_input_format = '%b %d, %Y'
    date_output_format = '%Y-%m-%d'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version_data = self._get_version_from_config()

    def parse_bill(self) -> dict:
        """Collect all relevant bill elements in a dictionary."""
        bill_data = {
            'provider': self.provider,
            'type': self.utility_type,
            'bill_date': self._get_bill_date(),
            'amount': self._get_bill_amount(),
            'due_date': self._get_bill_due_date()
        }
        return bill_data

    def _get_version_from_config(self) -> dict:
        """Lookup PDF version element numbers using a date reference from file."""
        reference_date = self._get_date_from_full_text()
        config_path = os.environ.get('CONFIG_FILE')
        try:
            with open(config_path, 'r') as f:
                versions = yaml.safe_load(f).get('dominion_energy').get('versions')
        except TypeError:
            self.logger.exception("Config location came back as 'None', have you set the DB_CONFIG env variable?")
            raise
        viable_versions = [x for x in versions.keys() if reference_date >= x]
        self.logger.debug(f'Viable version configs: {len(viable_versions)}')
        max_viable_version = versions.get(max(viable_versions))
        self.logger.info(f'Acquired version data: {max(viable_versions)}')
        return max_viable_version

    def _get_date_from_full_text(self) -> date:
        """Get a date reference from full text for determining version."""
        self.logger.info("Getting a date from full text in order to lookup provider's PDF revision")
        dump_location = '/tmp/full_pdf_text'
        with open(dump_location, 'r') as f:
            full_pdf_text = f.read()
        date_pattern = r'\w{3,} \d{1,2}, \d{4}'
        date_matches = re.findall(date_pattern, full_pdf_text)
        self.logger.info(f'Found {len(date_matches)} matches for dates in full text.')
        parsed_dates = []
        for match in date_matches:
            try:
                parsed_date = datetime.strptime(match, self.date_input_format)
            except ValueError:
                err_msg = f"Date match '{match}' is not parseable according to format '{self.date_input_format}'"
                self.logger.warning(err_msg)
            else:
                self.logger.debug(f'Parsed date: {parsed_date}')
                parsed_dates.append(parsed_date)
        earliest_date = min(parsed_dates).date()
        self.logger.info(f'Using earliest date: {earliest_date}')
        return earliest_date

    def _get_bill_date(self) -> str:
        """Get date bill was issued."""
        self.logger.info('Getting bill date')
        bill_date_element_page = self.version_data.get('bill_page')
        bill_date_element_number = self.version_data.get('bill_date_element')
        raw_bill_date = self.get_specific_element_from_page(
            element_num=bill_date_element_number, page_num=bill_date_element_page)
        bill_date = self._clean_bill_date(raw_bill_date=raw_bill_date)
        formatted_bill_date = bill_date.strftime(self.date_output_format)
        self.logger.info('Bill date retrieved and formatted')
        self.logger.info(formatted_bill_date)
        return formatted_bill_date

    def _clean_bill_date(self, raw_bill_date: str) -> date:
        """Convert raw bill date to a date object."""
        stripped = raw_bill_date.strip()
        segregated = stripped.split('\n')[0]
        parsed = datetime.strptime(segregated, self.date_input_format).date()
        return parsed

    def _get_bill_amount(self) -> str:
        """Get total bill amount."""
        self.logger.info('Getting bill amount')
        bill_amt_element_page = self.version_data.get('bill_page')
        bill_amt_element_number = self.version_data.get('bill_amt_element')
        raw_bill_amt = self.get_specific_element_from_page(
            element_num=bill_amt_element_number, page_num=bill_amt_element_page)
        bill_amt_cents = self._clean_bill_amount(raw_bill_amt=raw_bill_amt)
        bill_amt_usd = bill_amt_cents / 100
        bill_amt_formatted = f'{bill_amt_usd:.2f}'
        self.logger.info('Bill amount retrieved')
        self.logger.info(bill_amt_formatted)
        return bill_amt_formatted

    @staticmethod
    def _clean_bill_amount(raw_bill_amt: str) -> int:
        """Convert raw bill amount to integer (US cents)."""
        digit_pattern = r'\d'
        all_digits_in_amt = re.findall(digit_pattern, raw_bill_amt)
        combined_digits = ''.join(all_digits_in_amt)
        amt_in_cents = int(combined_digits)
        return amt_in_cents

    def _get_bill_due_date(self) -> str:
        """Get date bill is due."""
        self.logger.info('Getting bill due date')
        bill_duedate_element_num = self.version_data.get('bill_duedate_element')
        due_date_raw = self.get_specific_element_from_page(element_num=bill_duedate_element_num)
        try:
            due_date_parsed = self._parse_date_from_field(due_date_raw)
        except ValueError:
            self.logger.exception(f'Date pattern not found in field {bill_duedate_element_num}')
            raise
        due_date = self._clean_bill_date(raw_bill_date=due_date_parsed)
        formatted_due_date = due_date.strftime(self.date_output_format)
        self.logger.info('Due date retrieved')
        self.logger.info(formatted_due_date)
        return formatted_due_date

    @staticmethod
    def _parse_date_from_field(s: str) -> str:
        """Get date string out of larger string."""
        bill_duedate_pattern = r'\w{3,} \d{1,2}, \d{4}'
        match = re.search(bill_duedate_pattern, s)
        if match:
            return match.group(0)
        else:
            raise ValueError(f"Date pattern not found in string: '{s}'")
