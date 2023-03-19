import re
from datetime import datetime

from billreader import Bill


class DominionEnergyBill(Bill):
    provider = 'Dominion Energy'
    utility_type = 'power'
    date_input_format = '%b %d, %Y'
    date_output_format = '%Y-%m-%d'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

    def _get_bill_date(self) -> str:
        """Get date bill was issued."""
        self.logger.info('Getting bill date')
        bill_date_element_page = 1
        bill_date_element_number = 0
        raw_bill_date = self.get_specific_element_from_page(
            element_num=bill_date_element_number, page_num=bill_date_element_page)
        bill_date = self._clean_bill_date(raw_bill_date=raw_bill_date)
        formatted_bill_date = bill_date.strftime(self.date_output_format)
        self.logger.info('Bill date retrieved and formatted')
        return formatted_bill_date

    def _clean_bill_date(self, raw_bill_date: str) -> datetime:
        """Convert raw bill date to a datetime object."""
        stripped = raw_bill_date.strip()
        parsed = datetime.strptime(stripped, self.date_input_format).date()
        return parsed

    def _get_bill_amount(self) -> str:
        """Get total bill amount."""
        self.logger.info('Getting bill amount')
        bill_amt_element_page = 1
        bill_amt_element_number = 18
        raw_bill_amt = self.get_specific_element_from_page(
            element_num=bill_amt_element_number, page_num=bill_amt_element_page)
        bill_amt_cents = self._clean_bill_amount(raw_bill_amt=raw_bill_amt)
        bill_amt_usd = bill_amt_cents / 100
        bill_amt_formatted = f'{bill_amt_usd:.2f}'
        self.logger.info('Bill amount retrieved')
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
        bill_duedate_element_num = 12
        due_date_raw = self.get_specific_element_from_page(element_num=bill_duedate_element_num)
        try:
            due_date_parsed = self._parse_date_from_field(due_date_raw)
        except ValueError:
            raise ValueError(f'Date pattern not found in field {bill_duedate_element_num}')
        due_date = self._clean_bill_date(raw_bill_date=due_date_parsed)
        formatted_due_date = due_date.strftime(self.date_output_format)
        self.logger.info('Due date retrieved')
        return formatted_due_date

    @staticmethod
    def _parse_date_from_field(s: str) -> str:
        """Get date string out of larger string."""
        bill_duedate_pattern = r'\w{3} \d{2}, \d{4}'
        match = re.search(bill_duedate_pattern, s)
        if match:
            return match.group(0)
        else:
            raise ValueError(f"Date pattern not found in string: '{s}'")
