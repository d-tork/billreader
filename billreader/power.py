import re
from datetime import datetime
from pdfminer.layout import LTTextBoxHorizontal

from billreader import Bill


class DominionEnergyBill(Bill):
    date_input_format = '%b %d, %Y'
    date_output_format = '%Y-%m-%d'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse_bill(self) -> dict:
        """Collect all relevant bill elements in a dictionary."""
        bill_data = {
            'bill_date': self._get_bill_date(),
            'amount': self._get_bill_amount()
        }
        return bill_data

    def _get_bill_date(self) -> str:
        """Get date bill was issued."""
        bill_date_element_page = 1
        bill_date_element_number = 0
        bill_date_page = self.get_elements_from_page(page_num=bill_date_element_page)
        raw_bill_date = self._get_raw_bill_element(
            page=bill_date_page, element_num=bill_date_element_number)
        bill_date = self._clean_bill_date(raw_bill_date=raw_bill_date)
        formatted_bill_date = bill_date.strftime(self.date_output_format)
        return formatted_bill_date

    @staticmethod
    def _get_raw_bill_element(page, element_num: int) -> str:
        """Get a bill text element at a specific loci.

        Element assumed to be a pdfminer.layout.LTText* type.
        """
        element = page[element_num].get_text()
        return element

    def _clean_bill_date(self, raw_bill_date: str) -> datetime:
        """Convert raw bill date to a datetime object."""
        stripped = raw_bill_date.strip()
        parsed = datetime.strptime(stripped, self.date_input_format).date()
        return parsed

    def _get_bill_amount(self) -> float:
        """Get total bill amount."""
        bill_amt_element_page = 1
        bill_amt_element_number = 18
        bill_amt_page = self.get_elements_from_page(page_num=bill_amt_element_page)
        raw_bill_amt = self._get_raw_bill_element(
            page=bill_amt_page, element_num=bill_amt_element_number)
        bill_amt_cents = self._clean_bill_amount(raw_bill_amt=raw_bill_amt)
        bill_amt_usd = bill_amt_cents / 100
        bill_amt_formatted = f'{bill_amt_usd:.2f}'
        return bill_amt_formatted

    def _clean_bill_amount(self, raw_bill_amt: str) -> int:
        """Convert raw bill amount to integer (US cents)."""
        digit_pattern = r'\d'
        all_digits_in_amt = re.findall(digit_pattern, raw_bill_amt)
        combined_digits = ''.join(all_digits_in_amt)
        amt_in_cents = int(combined_digits)
        return amt_in_cents
