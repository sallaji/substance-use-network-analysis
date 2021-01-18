from data.model.features.feature import FeatureGroupInterface
import numpy as np


class FeatureAgeFirstUse(FeatureGroupInterface):
    """
    AGE CATEGORIES:

    infancy and toddlerhood: 18mo-3ys
    early childhood:3-5ys
    middle childhood: 5-11ys
    adolescence: 12-17ys
    emerging adulthood: 18-25ys
    early adulthood: 26-35ys
    mature/middle adulthood: 36-65ys
    late adulthood: 65+ ys


    """

    def features(self) -> dict:
        """:return the corresponding feature dictionary containing all features and attributes beloging to the group"""
        age_first_use = {
            "CIGTRY": {
                "substance": "cigarette",
                "label": "cigarette first use age",
                "question": "How old were you the first time you smoked part or all "
                            "of a cigarette?",
                "options": {
                    "RANGE": "1-65",
                    "985": "BAD DATA Logically assigned",
                    "991": "NEVER USED",
                    "994": "DON\'T KNOW",
                    "997": "REFUSED"
                }
            },
            "ALCTRY": {
                "substance": "alcohol",
                "label": "alcohol first use age",
                "question": "Think about the first time you had a drink of an "
                            "alcoholic beverage. How old were you the first time you "
                            "had a drink of an alcoholic beverage? Please do not "
                            "include any time when you only had a sip or two from "
                            "a drink.",
                "options": {
                    "RANGE": "1-69",
                    "985": "BAD DATA Logically assigned",
                    "991": "NEVER USED",
                    "994": "DON\'T KNOW",
                    "997": "REFUSED",
                    "998": "BLANK (NO ANSWER)"
                }
            },
            "MJAGE": {
                "substance": "marijuana",
                "label": "marijuana first use age",
                "question": "How old were you the first time you used marijuana or hashish?",
                "options": {
                    "RANGE": "1-82",
                    "985": "BAD DATA Logically assigned",
                    "991": "NEVER USED",
                    "994": "DON\'T KNOW",
                    "997": "REFUSED",
                    "998": "BLANK (NO ANSWER)"
                }
            },
            "COCAGE": {
                "substance": "cocaine",
                "label": "cocaine first use age",
                "question": "How old were you the first time you used cocaine, "
                            "in any form?",
                "options": {
                    "RANGE": "1-72",
                    "985": "BAD DATA Logically assigned",
                    "991": "NEVER USED",
                    "994": "DON\'T KNOW",
                    "997": "REFUSED",
                    "998": "BLANK (NO ANSWER)"
                }
            },
            "CRKAGE": {
                "substance": "crack",
                "label": "crack first use age",
                "question": "How old were you the first time you used 'crack'?",
                "options": {
                    "RANGE": "5-64",
                    "991": "NEVER USED",
                    "994": "DON\'T KNOW",
                    "997": "REFUSED",
                    "998": "BLANK (NO ANSWER)"
                }
            },
            "HERAGE": {
                "substance": "heroin",
                "label": "heroin first use age",
                "question": "How old were you the first time you used heroin?",
                "options": {
                    "RANGE": "2-70",
                    "985": "BAD DATA Logically assigned",
                    "991": "NEVER USED",
                    "994": "DON\'T KNOW",
                    "997": "REFUSED",
                    "998": "BLANK (NO ANSWER)"
                }
            },
            "HALLUCAGE": {
                "substance": "hallucinogens",
                "label": "hallucinogens first use age",
                "question": "How old were you the first time you used [LSFILL]?",
                "options": {
                    "RANGE": "1-73",
                    "985": "BAD DATA Logically assigned",
                    "991": "NEVER USED",
                    "994": "DON\'T KNOW",
                    "997": "REFUSED",
                    "998": "BLANK (NO ANSWER)"
                }
            },
            "INHALAGE": {
                "substance": "inhalants",
                "label": "inhalants first use age",
                "question": "How old were you the first time you used any inhalant for kicks or to get high?",
                "options": {
                    "RANGE": "1-60",
                    "985": "BAD DATA Logically assigned",
                    "991": "NEVER USED",
                    "994": "DON\'T KNOW",
                    "997": "REFUSED",
                    "998": "BLANK (NO ANSWER)"
                }
            },
            "METHAMAGE": {
                "substance": "methamphetamine",
                "label": "methamphetamine first use age",
                "question": "How old were you the first time you used methamphetamine?",
                "options": {
                    "RANGE": "1-70",
                    "985": "BAD DATA Logically assigned",
                    "991": "NEVER USED",
                    "994": "DON\'T KNOW",
                    "997": "REFUSED",
                    "998": "BLANK (NO ANSWER)"
                }
            }
        }
        return age_first_use

    def feature_keys(self, as_labels=False) -> list:
        if as_labels:
            return [v['label'] for k,v in self.features().items()]
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
                # "RANGE": "2-70",
                "985": (985, "BAD DATA Logically assigned"), # BAD DATA Logically assigned (i.e., usually inconsistent with other data)
                "991": (991, "Never used"), # NEVER USED [DRUG(s) OF INTEREST] Logically assigned
                "994": (994, "DON\'T KNOW"),
                "997": (997, "REFUSED"),
                "998": (998, "BLANK (NO ANSWER)")
            }
            if value_is_parsed:
                ops = {str(v[0]): (int(k), v[1]) for k, v in ops.items()}
            if 0 <= feature_number <= 985:
                # return tuple((feature_value, "Age {}".format(feature_value)))
                return tuple((feature_value, str(feature_value)))
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
