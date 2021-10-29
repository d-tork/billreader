import re
from datetime import datetime

from billreader import Bill


class FairfaxWater(Bill):
    provider = 'Fairfax Water'
    date_input_format = '%m/%d/%y'
    date_output_format = '%Y-%m-%d'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.raw_bill_text = self._get_text_from_page()

    def parse_bill(self) -> dict:
        """Collect all relevant bill elements in a dictionary."""
        bill_data = {
            'provider': self.provider,
            'bill_date': self._get_bill_date(),
            'amount': self._get_bill_amount(),
            'due_date': self._get_bill_due_date()
        }
        return bill_data

    def _get_bill_date(self) -> str:
        """Get date bill was issued."""
        bill_date_pattern = r'BillingDate(\d{2}\/\d{2}\/\d{2})'
        raw_bill_date = self._extract_pattern_from_full_text(patt=bill_date_pattern)
        bill_date = self._clean_bill_date(raw_bill_date=raw_bill_date)
        formatted_bill_date = bill_date.strftime(self.date_output_format)
        return formatted_bill_date

    def _clean_bill_date(self, raw_bill_date: str) -> datetime:
        """Convert raw bill date to a datetime object."""
        stripped = raw_bill_date.strip()
        parsed = datetime.strptime(stripped, self.date_input_format).date()
        return parsed

    def _get_bill_amount(self) -> str:
        """Get total bill amount."""
        bill_amt_pattern = r'TotalAmountDue\$(\d+\.\d{2})'
        raw_bill_amt = self._extract_pattern_from_full_text(patt=bill_amt_pattern)
        bill_amt_cents = self._clean_bill_amount(raw_bill_amt=raw_bill_amt)
        bill_amt_usd = bill_amt_cents / 100
        bill_amt_formatted = f'{bill_amt_usd:.2f}'
        return bill_amt_formatted

    def _extract_pattern_from_full_text(self, patt: str) -> str:
        """Get a heading-value pair from the raw text string.

        Args:
            patt: Raw regex pattern to match both title and value, with one capture group.
        """
        match = re.search(patt, self.raw_bill_text)
        if match:
            raw_value = match.group(1)
        else:
            raise ValueError('Total amount could not be parsed from full text.')
        return raw_value

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
        due_date_pattern = r'DueDate(\d{2}\/\d{2}\/\d{2})'
        raw_due_date = self._extract_pattern_from_full_text(patt=due_date_pattern)
        due_date = self._clean_bill_date(raw_bill_date=raw_due_date)
        formatted_due_date = due_date.strftime(self.date_output_format)
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
