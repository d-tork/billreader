from os import path
import logging

from pdfminer.high_level import extract_pages, extract_text


class Bill(object):
    """Parent container for PDF bills."""
    def __init__(self, filepath: str):
        self.logger = logging.getLogger(f'{__name__}.{type(self).__name__}')
        self.filepath = filepath
        self.pages = self._get_pages()

    def _get_pages(self) -> list:
        """Parse page layouts from PDF."""
        self.logger.info('Extracting pages from PDF')
        page_layout = extract_pages(self.filepath)
        pages = [x for x in page_layout]
        self.logger.info('Pages extracted')
        return pages

    def get_specific_element_from_page(self, element_num: int, **kwargs) -> str:
        self.logger.debug(f'Getting element {element_num} from page')
        page = self._get_all_elements_from_page(**kwargs)
        bill_element = self._get_raw_bill_element(page=page, element_num=element_num)
        self.logger.debug('Element retrieved')
        return bill_element

    def _get_all_elements_from_page(self, page_num: int=1) -> list:
        """Break down page elements, pages indexed starting at 1."""
        elements = [x for x in self.pages[page_num - 1]]
        return elements

    def _get_text_from_page(self) -> str:
        """Get full text from PDF.

        Use when elements can't be parsed.
        """
        self.logger.info('Extracting full text from PDF')
        full_text = extract_text(self.filepath)
        self.logger.info('Text extracted')
        return full_text

    @staticmethod
    def _get_raw_bill_element(page, element_num: int) -> str:
        """Get a bill text element at a specific loci.

        Element assumed to be a pdfminer.layout.LTText* type.
        """
        element = page[element_num].get_text()
        return element

    def parse_bill(self):
        raise NotImplementedError('Should be defined in child class.')


class FileChecker(object):
    """Determines what kind of utility bill was passed as a PDF."""
    def __init__(self, filepath: str, bind_path: str):
        self.logger = logging.getLogger(f'{__name__}.{type(self).__name__}')
        self.filepath = self._create_internal_docker_path(
            full_filepath=filepath, bind_path=bind_path)

    @staticmethod
    def _create_internal_docker_path(full_filepath: str, bind_path: str) -> str:
        """Create the filepath that refers to the bind mount within the container.

        macOS Automator will send a full macOS location (/Users/me/Documents/Utilities/...pdf)
        but the container needs a path pointing to somewhere on its own filesystem, which
        will be mounted via bind mount.

        Args:
            filepath: Full path to file on Docker host.
            bind_path: Path to bind mount in Docker container.
        """
        filename = path.basename(full_filepath)
        new_path = path.join(bind_path, filename)
        return new_path

    def determine_utility_provider(self) -> str:
        """Scan the contents to choose which parser to use.

        Returns:
            'fairfax_water' or 'dominion_energy'
        """
        self.logger.info('Creating bill instance to check for provider')
        bill = Bill(filepath=self.filepath)
        full_pdf_text = bill._get_text_from_page().lower()
        self.logger.info('Full text extracted')
        if 'fairfaxwater' in full_pdf_text:
            self.logger.info('Fairfax Water keyword found')
            return 'fairfax_water'
        elif 'dominion' in full_pdf_text:
            self.logger.info('Dominion Energy keyword found')
            return 'dominion_energy'
        else:
            raise ValueError('No relevant keywords detected in PDF')
