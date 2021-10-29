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

    def get_elements_from_page(self, page_num: int=1) -> list:
        """Break down page elements, pages indexed starting at 1."""
        elements = [x for x in self.pages[page_num - 1]]
        return elements

    def parse_bill(self):
        raise NotImplementedError('Should be defined in child class.')
