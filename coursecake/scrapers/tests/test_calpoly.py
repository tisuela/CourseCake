import pytest

from ..scraper import InvalidTermId
from ..calpoly import calpoly_scraper


TERM_ID = "2020-FALL-1"


def test_init():
    scraper = calpoly_scraper.CalpolyScraper(TERM_ID)

    assert scraper.term_code == "2208"

    with pytest.raises(InvalidTermId) as e:
        scraper = calpoly_scraper.CalpolyScraper("1800-FALL-1")


def test_scraper():
    scraper = calpoly_scraper.CalpolyScraper(TERM_ID)
    scraper.get_classes(testing=True)

    print(f"courses = {len(scraper.courses)}")
    print(f"classes = {len(scraper.classes)}")

    assert len(scraper.courses) > 10
    assert len(scraper.classes) > 11
