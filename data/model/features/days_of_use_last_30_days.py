from data.model.features.feature import FeatureGroupInterface
import numpy as np


class FeatureDaysOfUseLast30Days(FeatureGroupInterface):

    # def day_interval(self, feature_key, feature_value, number_of_intervals):

    def features(self) -> dict:
        last_30_days_use = {
            "CGR30USE": {
                "substance": "cigarette",
                "label": "Days of cigarette use in past month",
                "question": "During the past 30 days, that is since [DATEFILL], on how many "
                            "days did you smoke part or all of a cigar?",
                "options": {
                    "RANGE": "1 - 30",
                    "91": "NEVER USED",
                    "93": "DID NOT USE IN THE PAST 30 DAYS",
                    "94": "DON'T KNOW",
                    "97": "REFUSED",
                    "98": "BLANK (NO ANSWER)",
                }
            },
            "ALCDAYS": {
                "substance": "alcohol",
                "label": "Days of alcohol use in past month",
                "question": "Think specifically about the past 30 days, from "
                            "[DATEFILL], up to and including today. During the past "
                            "30 days, on how many days did you drink one or more "
                            "drinks of an alcoholic beverage?",
                "options": {
                    "RANGE": "1 - 30",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",
                    "93": "DID NOT USE IN THE PAST 30 DAYS",
                    "94": "DON'T KNOW",
                    "97": "REFUSED",
                    "98": "BLANK (NO ANSWER)"
                }
            },
            "MJDAY30A": {
                "substance": "marijuana",
                "label": "Days of marijuana use in past month",
                "question": "Think specifically about the past 30 days, from [DATEFILL]"
                            " up to and including today. During the past 30 days, on "
                            "how many days did you use marijuana or hashish?",
                "options": {
                    "RANGE": "1 - 30",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",
                    "93": "DID NOT USE IN THE PAST 30 DAYS",
                    "94": "DON'T KNOW",
                    "97": "REFUSED",
                    "98": "BLANK (NO ANSWER)"
                }
            },

            "COCUS30A": {
                "substance": "cocaine",
                "label": "Days of cocaine use in past month",
                "question": "Think specifically about the past 30 days, from [DATEFILL]"
                            " up to and including today. During the past 30 days, on "
                            "how many days did you use cocaine?",
                "options": {
                    "RANGE": "1 - 30",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",
                    "93": "DID NOT USE IN THE PAST 30 DAYS",
                    "94": "DON'T KNOW",
                    "97": "REFUSED",
                    "98": "BLANK (NO ANSWER)"
                }
            },
            "CRKUS30A": {
                "substance": "crack",
                "label": "Days of crack use in past month",
                "question": "Think specifically about the past 30 days, from "
                            "[DATEFILL] up to and including today. During the past 30 "
                            "days, on how many days did you use 'crack'?",
                "options": {
                    "RANGE": "1 - 30",
                    "91": "NEVER USED",
                    "93": "DID NOT USE IN THE PAST 30 DAYS",
                    "97": "REFUSED",
                    "98": "BLANK (NO ANSWER)"
                }
            },
            "HER30USE": {
                "substance": "heroin",
                "label": "Days of heroin use in past month",
                "question": "Think specifically about the past 30 days, from [DATEFILL] up to and"
                            " including today. During the past 30 days, on how many days did you "
                            "use heroin?",
                "options": {
                    "RANGE": "1 - 30",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",
                    "93": "DID NOT USE IN THE PAST 30 DAYS",
                    "97": "REFUSED",
                    "98": "BLANK (NO ANSWER)"
                }
            },
            "HALLUC30N": {
                "substance": "hallucinogens",
                "label": "Days of hallucinogens use in past month",
                "question": "Think specifically about the past 30 days, from [DATEFILL] up to and including today. "
                            "During the past 30 days, on how many days did you use [LSFILL]?",
                "options": {
                    "RANGE": "1 - 30",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED HALLUCINOGENS",
                    "93": "DID NOT USE HALLUCINOGENS IN THE PAST 30 DAYS",
                    "94": "DON'T KNOW",
                    "97": "REFUSED",
                    "98": "BLANK (NO ANSWER)",
                }
            },
            "INHAL30N": {
                "substance": "inhalants",
                "label": "Days of inhalants use in past month",
                "question": "Think specifically about the past 30 days, from [DATEFILL] up to and including today. "
                            "During the past 30 days, on how many days did you use any inhalant for kicks or "
                            "to get high?",
                "options": {
                    "RANGE": "1 - 30",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",
                    "93": "DID NOT USE IN THE PAST 30 DAYS",
                    "94": "DON'T KNOW",
                    "97": "REFUSED",
                    "98": "BLANK (NO ANSWER)",
                }
            },
            "METHAM30N": {
                "substance": "methamphetamine",
                "label": "Days of methamphetamine use in past month",
                "question": "Think specifically about the past 30 days, from [DATEFILL] up to and including today."
                            " During the past 30 days, on how many days did you use methamphetamine?",
                "options": {
                    "RANGE": "1 - 30",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",
                    "94": "DON'T KNOW",
                    "93": "DID NOT USE IN THE PAST 30 DAYS",
                    "97": "REFUSED",
                    "98": "BLANK (NO ANSWER)"
                }
            },

            "PNRNM30FQ": {
                "substance": "pain relievers",
                "label": "Days of pain relievers misuse in past month",
                "question": "question",
                "options": {
                    "RANGE": "1 - 30",
                    "83": "did not use in past 12 months",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",  # never misused
                    "94": "DON'T KNOW",
                    "93": "DID NOT USE IN THE PAST 30 DAYS",
                    "97": "REFUSED",
                    "98": "BLANK (NO ANSWER)"
                }
            },
            "TRQNM30FQ": {
                "substance": "tranquilizers",
                "label": "Days of tranquilizers misuse in past month",
                "question": "question",
                "options": {
                    "RANGE": "1 - 30",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",  # never misused
                    "94": "DON'T KNOW",
                    "93": "DID NOT USE IN THE PAST 30 DAYS",
                    "97": "REFUSED",
                    "98": "BLANK (NO ANSWER)"
                }
            },
            "STMNM30FQ": {
                "substance": "stimulants",
                "label": "Days of stimulants misuse in past month",
                "question": "",
                "options": {
                    "RANGE": "1 - 30",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",  # never misused
                    "94": "DON'T KNOW",
                    "93": "DID NOT USE IN THE PAST 30 DAYS",
                    "97": "REFUSED",
                    "98": "BLANK (NO ANSWER)"
                }
            },
            "SEDNM30FQ": {
                "substance": "sedatives",
                "label": "Days of sedatives misuse in past month",
                "question": "",
                "options": {
                    "RANGE": "1 - 30",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",  # never misused
                    "94": "DON'T KNOW",
                    "93": "DID NOT USE IN THE PAST 30 DAYS",
                    "97": "REFUSED",
                    "98": "BLANK (NO ANSWER)"
                }
            }
        }
        return last_30_days_use

    def feature_keys(self, as_labels=False, parent_substances_only=True) -> list:
        if as_labels:
            return [v['label'] for k, v in self.features().items()]
        return list(self.features().keys())

    def feature_key_and_substance_value(self, as_labels=False):
        """
        creates a dictionary with the names of the features as a key and the name of the substance as a value
        :param as_labels: if true, the dictionary keys will correspond to the value of the label contained in each feature
        :return: a dictionary with feature names and the substances to which they belong as a value
        """
        dict_ = {}
        for feature_key, feature_value in self.features().items():
            if as_labels:
                dict_.update({feature_value['label']: feature_value['substance']})
            else:
                dict_.update({feature_key: feature_value['substance']})
        return dict_

    def get_option_value(self, feature_value, feature_key=None, value_is_parsed=False):
        try:
            if str(feature_value).isnumeric() is False:
                raise Exception('Feature value {} is not numeric'.format(feature_value))
            feature_number = int(feature_value)
            ops = {
                # "RANGE": "1-30",
                "83": (993, "DID NOT USE IN THE PAST 12 MONTHS"),
                "85": (985, "BAD DATA Logically assigned"),
                # BAD DATA Logically assigned (i.e., usually inconsistent with other data)
                "91": (991, "Never used"),  # NEVER USED [DRUG(s) OF INTEREST] Logically assigned
                "93": (993, "DID NOT USE IN THE PAST 30 DAYS"),
                "94": (994, "DON\'T KNOW"),
                "97": (997, "REFUSED"),
                "98": (998, "BLANK (NO ANSWER)")
            }
            if value_is_parsed:
                ops = {str(v[0]): (int(k), v[1]) for k, v in ops.items()}
            if 1 <= feature_number <= 30:
                # return tuple((feature_value, "Days {}".format(feature_value)))
                return tuple((feature_value, feature_number))
            else:
                return ops[str(feature_value)]
        except Exception:
            print("An error occured while parsing the value {}".format(feature_value))

    def parse_option(self, feature_value, feature_key=None, value_label=False, value_is_parsed=False) -> object:
        """:return the parsed value according to the given feature_value."""
        if feature_value == -1:
            if value_label:
                return ""
            return feature_value
        else:
            parsed_value = self.get_option_value(feature_value=feature_value, value_is_parsed=value_is_parsed)
            if value_label:
                return parsed_value[1]
            return parsed_value[0]

    def feature_labels(self) -> dict:
        return {k: v['label'] for k, v in self.features().items()}

    def feature_label(self, feature_key) -> str:
        return self.feature_labels()[feature_key]
