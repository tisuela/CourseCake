# Data provider is a student-made REST API: SlugSurvival
# https://slugsurvival.com/explain/opensource
import requests

from ..scraper import Scraper
import .constants

class UcscScraper(Scraper):

    class InvalidTermId(Exception):
        def __init__(self, term_id: str, encoded_term_id: str):
            self.term_id = term_id
            self.encoded_term_id = encoded_term_id

        def __str__(self):

            return f"Invalid Term Id, {self.term_id}" + \
                    f" Encoded Term Id, {self.encoded_term_id} did not" + \
                    " match with any term name found in SlugSurvival"


    def __init__(self, term_id: str = "2020-FALL-1"):
        self.term_id = term_id
        self.encoded_term_id = self._encode_term_id(term_id)


    def _encode_term_id(self, term_id: str):
        '''
        Encodes the term_id so we can match it with a term code
        in SlugSurvival's endpoints
        '''
        term_info = term_id.split("-")
        encoded = term_info[0] + term_info[1] + "QUARTER"
        return encoded

    def _get_terms(self, encoded_term_id: str):
        term_response = requests.get(constants.TERMS_API_URL)
        terms = term_response.json()

        for term in terms:
            if term["name"].upper() == encoded_term_id.upper():
                return term["code"]

        raise InvalidTermId(self.term_id, encoded_term_id)
