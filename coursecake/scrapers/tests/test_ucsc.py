import pytest

from ..ucsc import ucsc_scraper


TERM_ID = "2020-FALL-1"


def test_init():
    scraper = ucsc_scraper.UcscScraper("2020-FALL")

    with pytest.raises(ucsc_scraper.InvalidTermId) as e:
        ucsc_scraper.UcscScraper("1620-Fall")


def test_get_classes():
    scraper = ucsc_scraper.UcscScraper(TERM_ID)

    classes = scraper.get_classes()

    for a_class in classes:
        print(a_class)
