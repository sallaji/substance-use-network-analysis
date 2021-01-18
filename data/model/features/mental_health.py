from data.model.features.feature import FeatureGroupInterface


class FeatureMentalHealth(FeatureGroupInterface):
    def features(self) -> dict:
        mental_health = {
            "DSTCHR30": {
                "label": "felt sad in past month",
                "question": "During the past 30 days, how often did you feel so sad or depressed that nothing could "
                            "cheer you up?",
                "options": {
                    "1": "All of the time",
                    "2": "Most of the time",
                    "3": "Some of the time",
                    "4": "A little of the time",
                    "5": "None of the time",
                    "85": "BAD DATA Logically assigned",
                    "94": "DON'T KNOW",
                    "97": "REFUSED",
                    "98": "BLANK (NO ANSWER)",
                    "99": "LEGITIMATE SKIP"
                }
            },
            "DSTNGD30": {
                "label": "felt down, no good or worthless in past month",
                "question": "During the past 30 days, how often did you feel down on yourself, no good or worthless?",
                "options": {
                    "1": "All of the time",
                    "2": "Most of the time",
                    "3": "Some of the time",
                    "4": "A little of the time",
                    "5": "None of the time",
                    "85": "BAD DATA Logically assigned",
                    "94": "DON'T KNOW",
                    "97": "REFUSED",
                    "98": "BLANK (NO ANSWER)",
                    "99": "LEGITIMATE SKIP"
                }
            },
            "DSTHOP30": {
                "label": "felt hopeless in past month",
                "question": "During the past 30 days, how often did you feel hopeless?",
                "options": {
                    "1": "All of the time",
                    "2": "Most of the time",
                    "3": "Some of the time",
                    "4": "A little of the time",
                    "5": "None of the time",
                    "85": "BAD DATA Logically assigned",
                    "94": "DON'T KNOW",
                    "97": "REFUSED",
                    "98": "BLANK (NO ANSWER)",
                    "99": "LEGITIMATE SKIP"
                },
            },
            "DSTEFF30": {
                "label": "felt like everything was an effort in past month",
                "question": "During the past 30 days, how often did you feel like everything was an effort?",
                "options": {
                    "1": "All of the time",
                    "2": "Most of the time",
                    "3": "Some of the time",
                    "4": "A little of the time",
                    "5": "None of the time",
                    "85": "BAD DATA Logically assigned",
                    "94": "DON'T KNOW",
                    "97": "REFUSED",
                    "98": "BLANK (NO ANSWER)",
                    "99": "LEGITIMATE SKIP"
                },
            }
        }
        return mental_health

    def feature_keys(self, as_labels=False) -> list:
        if as_labels:
            return [v['label'] for k, v in self.features().items()]
        return list(self.features().keys())

    def get_option_value(self, feature_value, feature_key=None, value_is_parsed=False):
        try:
            if str(feature_value).isnumeric() is False:
                raise Exception('Feature value {} is not numeric'.format(feature_value))
            ops = {
                "1": (1, "All of the time"),
                "2": (2, "Most of the time"),
                "3": (3, "Some of the time"),
                "4": (4, "A little of the time"),
                "5": (5, "None of the time"),
                "85": (985, "BAD DATA Logically assigned"),
                # 985 BAD DATA Logically assigned (i.e., usually inconsistent with other data)
                "94": (994, "DON'T KNOW"),
                "97": (997, "REFUSED"),
                "98": (998, "BLANK (NO ANSWER)"),
                "99": (999, "LEGITIMATE SKIP")  # LEGITIMATE SKIP Logically assigned
            }
            if value_is_parsed:
                ops = {str(v[0]): (int(k), v[1]) for k, v in ops.items()}
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

        # def option_label(self, feature_value, feature_key=None, value_is_parsed=True) -> str:
        #     return self.get_option_value(feature_value=feature_value, value_is_parsed=value_is_parsed)[1]

    def feature_labels(self) -> dict:
        return {k: v['label'] for k, v in self.features().items()}

    def feature_label(self, feature_key) -> str:
        return self.feature_labels()[feature_key]


