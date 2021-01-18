from data.model.features.feature import FeatureGroupInterface
import numpy as np


class FeatureDemographics(FeatureGroupInterface):  # an informal feature interface
    def features(self) -> dict:
        """:return the corresponding feature dictionary containing all features and attributes beloging to the group"""
        demographics = {
            "AGE2": {
                "label": "age",
                "description": "After a respondent has entered his/her birthdate in the first part of the questionnaire, "
                               "he/she has multiple opportunities to change his/her age in response to consistency checks "
                               "throughout the questionnaire. It is therefore possible for the age recorded by the "
                               "respondent at the beginning of the questionnaire to be different than the age at the "
                               "end of the questionnaire. The final age variable is determined using these two "
                               "constituent age variables, in addition to the age calculated from the raw birthdate and "
                               "the final edited interview date, the age entered in the questionnaire roster "
                               "(if it exists), and the pre-interview screener age.",
                "options": {
                    "1": "Respondent is 12 years old",
                    "2": "Respondent is 13 years old",
                    "3": "Respondent is 14 years old",
                    "4": "Respondent is 15 years old",
                    "5": "Respondent is 16 years old",
                    "6": "Respondent is 17 years old",
                    "7": "Respondent is 18 years old",
                    "8": "Respondent is 19 years old",
                    "9": "Respondent is 20 years old",
                    "10": "Respondent is 21 years old",
                    "11": "Respondent is 22 or 23 years old",
                    "12": "Respondent is 24 or 25 years old",
                    "13": "Respondent is between 26 and 29 years old",
                    "14": "Respondent is between 30 and 34 years old",
                    "15": "Respondent is between 35 and 49 years old",
                    "16": "Respondent is between 50 and 64 years old",
                    "17": "Respondent is 65 years old or older",
                }
            },
            "CATAG6": {
                "label": "age category",
                "description": "After a respondent has entered his/her birthdate in the first part of the questionnaire, "
                               "he/she has multiple opportunities to change his/her age in response to consistency checks "
                               "throughout the questionnaire. It is therefore possible for the age recorded by the "
                               "respondent at the beginning of the questionnaire to be different than the age at the "
                               "end of the questionnaire. The final age variable is determined using these two "
                               "constituent age variables, in addition to the age calculated from the raw birthdate and "
                               "the final edited interview date, the age entered in the questionnaire roster "
                               "(if it exists), and the pre-interview screener age.",
                "options": {
                    "1": "Respondent is between 12 and 17 Years Old",
                    "2": "Respondent is between 18 and 25 Years Old",
                    "3": "Respondent is between 26 and 34 Years Old",
                    "4": "Respondent is between 35 and 49 Years Old",
                    "5": "Respondent is between 50 and 64 Years Old",
                    "6": "Respondent is 65 or Older"
                }
            },

            "HEALTH": {
                "label": "health",
                "question": "This question is about your overall health. Would you say your health in general is "
                            "excellent, very good, good, fair, or poor?",
                "options": {
                    "1": "Excellent",
                    "2": "Very good",
                    "3": "Good",
                    "4": "Fair",
                    "5": "Poor",
                    "94": " DON'T KNOW",
                    "97": " REFUSED",
                }
            },
            "IRSEX": {
                "label": "sex",
                "description": "Beginning with the 2002 survey, missing values for the gender question (QD01) were no "
                               "longer permitted. Thus, no imputation was required. This variable has the prefix 'IR', "
                               "which stands for 'Imputation Revised', only for the sake of consistency with data sets"
                               " from earlier surveys.",
                "options": {
                    "1": "Male",
                    "2": "Female"
                }
            },

            "IRWRKSTAT18": {
                "label": "employment status",
                "description": "(IMPUTED EMPLOYMENT) IRWRKSTAT18 is a recode of IRWRKSTAT and AGE2. Respondents aged "
                               "12-17 are assigned a skip code, regardless of their answers to the employment status"
                               " questions.",
                "options": {
                    "1": "Employed full time",
                    "2": "Employed part time",
                    "3": "Unemployed",
                    "4": "Other (incl. not in labor force)",
                    "99": " 12-17 year olds",
                }
            },

            "NEWRACE2": {
                "label": "race",
                "description": "Race recoded in 7 levels",
                "options": {
                    "1": "NonHisp White",
                    "2": "NonHisp Black/Afr Am",
                    "3": "NonHisp Native Am/AK Native",
                    "4": "NonHisp Native HI/Other Pac Isl",
                    "5": "NonHisp Asian",
                    "6": "NonHisp more than one race",
                    "7": "Hispanic"
                }
            },
            "POVERTY3": {
                "label": "poverty level",
                "options": {
                    "1": "Living in Poverty",
                    "2": "Income Up to 2X Fed Pov Thresh",
                    "3": "Income More Than 2X Fed Pov Thresh"
                }
            }
        }
        return demographics

    def feature_keys(self, as_labels=False) -> list:
        if as_labels:
            return [v['label'] for k, v in self.features().items()]
        return list(self.features().keys())

    def get_option_value(self, feature_value=None, feature_key=None, value_is_parsed=False):
        try:
            if str(feature_value).isnumeric() is False:
                raise Exception('Feature value {} is not numeric'.format(feature_value))
            demographics = {
                "CATAG6": {
                    "1": (1, "12 - 17 Years Old"),
                    "2": (2, "18 - 25 Years Old"),
                    "3": (3, "26 - 34 Years Old"),
                    "4": (4, "35 - 49 Years Old"),
                    "5": (5, "50 - 64 Years Old"),
                    "6": (6, "65 or Older"),
                },
                "AGE2": {
                    "1": (1, "12 years old"),
                    "2": (2, "13 years old"),
                    "3": (3, "14 years old"),
                    "4": (4, "15 years old"),
                    "5": (5, "16 years old"),
                    "6": (6, "17 years old"),
                    "7": (7, "18 years old"),
                    "8": (8, "19 years old"),
                    "9": (9, "20 years old"),
                    "10": (10, "21 years old"),
                    "11": (11, "22 or 23 years old"),
                    "12": (12, "24 or 25 years old"),
                    "13": (13, "between 26 and 29 years old"),
                    "14": (14, "between 30 and 34 years old"),
                    "15": (15, "between 35 and 49 years old"),
                    "16": (16, "between 50 and 64 years old"),
                    "17": (17, "65 years old or older"),
                },
                "HEALTH": {
                    "1": (1, "Excellent"),
                    "2": (2, "Very good"),
                    "3": (3, "Good"),
                    "4": (4, "Fair"),
                    "5": (5, "Poor"),
                    "94": (994, " DON'T KNOW"),
                    "97": (997, " REFUSED"),
                },
                "IRSEX": {
                    "1": (1, "Male"),
                    "2": (0, "Female"),
                },
                "IRWRKSTAT18": {
                    "1": (1, "Employed full time"),
                    "2": (2, "Employed part time"),
                    "3": (3, "Unemployed"),
                    "4": (4, "Other (incl. not in labor force)"),
                    "99": (99, " 12-17 year olds"),
                },
                "NEWRACE2": {
                    "1": (1, "NonHisp White"),
                    "2": (2, "NonHisp Black/Afr Am"),
                    "3": (3, "NonHisp Native Am/AK Native"),
                    "4": (4, "NonHisp Native HI/Other Pac Isl"),
                    "5": (5, "NonHisp Asian"),
                    "6": (6, "NonHisp more than one race"),
                    "7": (7, "Hispanic"),
                },
                "POVERTY3": {
                    "1": (1, "Living in Poverty"),
                    "2": (2, "Income Up to 2X Fed Pov Thresh"),
                    "3": (3, "Income More Than 2X Fed Pov Thresh"),
                    "999": (999, "is nan"),
                }
            }

            if value_is_parsed:
                demographics = {f_k: {str(v[0]): (int(k), v[1]) for k, v in f_v.items()} for f_k, f_v in
                                demographics.items()}
            return demographics[str(feature_key)][str(feature_value)]
        except Exception:
            print("An error occured while parsing the value {} of feature {} in demographics".format(feature_value,
                                                                                                     feature_key))

    def parse_option(self, feature_value, feature_key=None, value_label=False, value_is_parsed=False) -> object:
        """:return the parsed value according to the given feature_value."""
        import pandas as pd
        if feature_value == -1 or pd.isna(feature_value):
            if value_label:
                return ""
            return feature_value
        else:
            parsed_value = self.get_option_value(feature_value=feature_value, feature_key=feature_key,
                                                 value_is_parsed=value_is_parsed)
            if value_label:
                return parsed_value[1]
            return parsed_value[0]

    def feature_labels(self) -> dict:
        return {k: v['label'] for k, v in self.features().items()}

    def feature_label(self, feature_key) -> str:
        return self.feature_labels()[feature_key]


if __name__ == "__main__":
    demo = FeatureDemographics()
    print("a1".isnumeric())
