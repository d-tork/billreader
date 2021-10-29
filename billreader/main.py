from os import path
from pdfminer.high_level import extract_text

from billreader import PROJ_PATH


def main():
    sample_path_power = path.join(PROJ_PATH, 'samples', 'power_2021-10-07.pdf')
    raw_text = extract_text_from_pdf(sample_path_power)
    print(raw_text)


def extract_text_from_pdf(pdf_path):
    text = extract_text(pdf_path)
    return text


if __name__ == '__main__':
    main()