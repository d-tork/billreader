from pdfminer.high_level import extract_pages


class Bill(object):
    """Parent container for PDF bills."""
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.pages = self._get_pages()

    def _get_pages(self) -> list:
        """Parse page layouts from PDF."""
        page_layout = extract_pages(self.filepath)
        pages = [x for x in page_layout]
        return pages

    def get_specific_element_from_page(self, element_num: int, **kwargs) -> str:
        page = self._get_all_elements_from_page(**kwargs)
        bill_element = self._get_raw_bill_element(page=page, element_num=element_num)
        return bill_element

    def _get_all_elements_from_page(self, page_num: int=1) -> list:
        """Break down page elements, pages indexed starting at 1."""
        elements = [x for x in self.pages[page_num - 1]]
        return elements

    @staticmethod
    def _get_raw_bill_element(page, element_num: int) -> str:
        """Get a bill text element at a specific loci.

        Element assumed to be a pdfminer.layout.LTText* type.
        """
        element = page[element_num].get_text()
        return element

    def parse_bill(self):
        raise NotImplementedError('Should be defined in child class.')
