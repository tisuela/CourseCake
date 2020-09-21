from enum import Enum


class UniversityName(str, Enum):
    uci = "uci"
    ucsc = "ucsc"
    calpoly = "calpoly"
    # csus = "csus"


class Term(str, Enum):
    summer_2020_1 = "2020-SUMMER-1"
    summer_2020_2 = "2020-SUMMER-2"
    fall_2020_1 = "2020-FALL"
