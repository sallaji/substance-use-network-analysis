from data.model.features.feature import FeatureGroupInterface
import numpy as np


class FeatureEverUsed(FeatureGroupInterface):
    def features(self) -> dict:
        ever_used = {
            "CIGEVER": {
                "substance": "cigarette",
                "label": "cigarette ever used",
                "question": "Have you ever smoked part or all of a cigarette?",
                "options": {
                    "1": "yes",
                    "2": "no",
                }
            },
            "ALCEVER": {
                "substance": "alcohol",
                "label": "alcohol ever used",
                "question": "Have you ever, even once, had a drink of any type of "
                            "alcoholic beverage? Please do not include times when you "
                            "only had a sip or two from a drink. ",
                "options": {
                    "1": "yes",
                    "2": "no",
                    "85": "BAD DATA Logically assigned",
                    "94": "DON'T KNOW",
                    "97": "REFUSED"
                }
            },
            "MJEVER": {
                "substance": "marijuana",
                "label": "marijuana ever used",
                "question": "Have you ever, even once, used marijuana or hashish?",
                "options": {
                    "1": "yes",
                    "2": "no",
                    "94": "DON'T KNOW",
                    "97": "REFUSED"
                }
            },
            "COCEVER": {
                "substance": "cocaine",
                "label": "cocaine ever used",
                "question": "Have you ever, even once, used any form of cocaine?",
                "options": {
                    "1": "yes",
                    "2": "no",
                    "94": "DON'T KNOW",
                    "97": "REFUSED"
                }
            },
            "CRKEVER": {
                "substance": "crack",
                "label": "crack ever used",
                "question": "Have you ever, even once, used 'crack'?",
                "options": {
                    "1": "yes",
                    "2": "no",
                    "91": "NEVER USED (COCEVER=2)",
                    "94": "DON'T KNOW",
                    "97": "REFUSED",
                    "98": "BLANK (NO ANSWER)"
                }
            },
            "HEREVER": {
                "substance": "heroin",
                "label": "heroin ever used",
                "question": "Have you ever, even once, used heroin?",
                "options": {
                    "1": "yes",
                    "2": "no",
                    "94": "DON'T KNOW",
                    "97": "REFUSED",
                }
            },
            "LSD": {
                "substance": "acid",
                "label": "acid ever used",
                "parent": "hallucinogens",
                "question": "Have you ever, even once, used LSD, also called 'acid'?",
                "options": {
                    "1": "Yes",
                    "2": "No",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",
                    "94": "DON'T KNOW",
                    "97": "REFUSED"
                }
            },
            "PCP": {
                "substance": "phencyclidine",
                "label": "phencyclidine ever used",
                "parent": "hallucinogens",
                "question": "Have you ever, even once, used PCP, also called 'angel dust' or phencyclidine?",
                "options": {
                    "1": "Yes",
                    "2": "No",
                    "3": "Yes LOGICALLY ASSIGNED",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",
                    "94": "DON'T KNOW",
                    "97": "REFUSED"
                }
            },
            "PEYOTE": {
                "substance": "peyote",
                "label": "peyote ever used",
                "parent": "hallucinogens",
                "question": "Have you ever, even once, used peyote?",
                "options": {
                    "1": "Yes",
                    "2": "No",
                    "3": "Yes LOGICALLY ASSIGNED",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",
                    "94": "DON'T KNOW",
                    "97": "REFUSED"
                }
            },
            "MESC": {
                "substance": "mescaline",
                "label": "mescaline ever used",
                "parent": "hallucinogens",
                "question": "Have you ever, even once, used mescaline?",
                "options": {
                    "1": "Yes",
                    "2": "No",
                    "3": "Yes LOGICALLY ASSIGNED",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",
                    "94": "DON'T KNOW",
                    "97": "REFUSED"
                }
            },
            "PSILCY": {
                "substance": "mushrooms",
                "label": "mushrooms ever used",
                "parent": "hallucinogens",
                "question": "Have you ever, even once, used psilocybin, found in mushrooms?",
                "options": {
                    "1": "Yes",
                    "2": "No",
                    "3": "Yes LOGICALLY ASSIGNED",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",
                    "94": "DON'T KNOW",
                    "97": "REFUSED"
                }
            },
            "ECSTMOLLY": {
                "substance": "ecstasy",
                "label": "ecstasy ever used",
                "parent": "hallucinogens",
                "question": "Have you ever, even once, used 'Ecstasy' or 'Molly,' also known as MDMA?",
                "options": {
                    "1": "Yes",
                    "2": "No",
                    "3": "Yes LOGICALLY ASSIGNED",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",
                    "94": "DON'T KNOW",
                    "97": "REFUSED"
                }
            },
            "KETMINESK": {
                "substance": "Ketamine",
                "label": "Ketamine ever used",
                "parent": "hallucinogens",
                "question": "Have you ever, even once, used Ketamine, also called 'Special K' or 'Super K'?",
                "options": {
                    "1": "Yes",
                    "2": "No",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",
                    "94": "DON'T KNOW",
                    "97": "REFUSED"
                }
            },
            "DMTAMTFXY": {
                "substance": "dimethyltryptamine",
                "label": "dimethyltryptamine ever used",
                "parent": "hallucinogens",
                "question": "Have you ever, even once, used any of the following: \nDMT, also called dimethyltryptamine"
                            ",\nAMT, also called alpha-methyltryptamine, or \nFoxy, also called 5-MeO-DIPT?",
                "options": {
                    "1": "Yes",
                    "2": "No",
                    "3": "Yes LOGICALLY ASSIGNED",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",
                    "94": "DON'T KNOW",
                    "97": "REFUSED"
                }
            },
            "SALVIADIV": {
                "substance": "salvia divinorum",
                "label": "salvia divinorum ever used",
                "parent": "hallucinogens",
                "question": "Have you ever, even once, used Salvia divinorum?",
                "options": {
                    "1": "Yes",
                    "2": "No",
                    "3": "Yes LOGICALLY ASSIGNED",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",
                    "94": "DON'T KNOW",
                    "97": "REFUSED"
                }
            },
            "HALLUCOTH": {
                "substance": "other hallucinogens",
                "label": "other hallucinogens ever used",
                "parent": "hallucinogens",
                "question": "Have you ever, even once used any other hallucinogens besides the ones that have been "
                            "listed?",
                "options": {
                    "1": "Yes",
                    "2": "No",
                    "5": "Yes (specific hallucinogen unknown) LOG ASSN",  # special var :)
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",
                    "94": "DON'T KNOW",
                    "97": "REFUSED"
                }
            },
            "AMYLNIT": {
                "substance": "poppers",
                "label": "poppers ever used",
                "parent": "inhalants",
                "question": "Have you ever, even once, inhaled amyl nitrite, 'poppers,' locker room odorizers, or "
                            "'rush' for kicks or to get high?",
                "options": {
                    "1": "yes",
                    "2": "no",
                    "3": "Yes LOGICALLY ASSIGNED",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",
                    "94": "DON'T KNOW",
                    "97": "REFUSED"
                }
            },
            "CLEFLU": {
                "substance": "cleaning fluid",
                "label": "cleaning fluid ever used",
                "parent": "inhalants",
                "question": "Have you ever, even once, inhaled correction fluid, degreaser, or cleaning fluid for"
                            " kicks or to get high?",
                "options": {
                    "1": "yes",
                    "2": "no",
                    "3": "Yes LOGICALLY ASSIGNED",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",
                    "94": "DON'T KNOW",
                    "97": "REFUSED"
                }
            },
            "GAS": {
                "substance": "gasoline or lighter fluid",
                "label": "gasoline or lighter fluid ever used",
                "parent": "inhalants",
                "question": "Have you ever, even once, inhaled gasoline or lighter fluid for kicks or to get high?",
                "options": {
                    "1": "yes",
                    "2": "no",
                    "3": "Yes LOGICALLY ASSIGNED",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",
                    "94": "DON'T KNOW",
                    "97": "REFUSED"
                }
            },
            "GLUE": {
                "substance": "glue",
                "label": "glue ever used",
                "parent": "inhalants",
                "question": "Have you ever, even once, inhaled glue, shoe polish, or toluene for kicks or to get"
                            " high?",
                "options": {
                    "1": "yes",
                    "2": "no",
                    "3": "Yes LOGICALLY ASSIGNED",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",
                    "94": "DON'T KNOW",
                    "97": "REFUSED"
                }
            },
            "ETHER": {
                "substance": "anesthetics",
                "label": "anesthetics ever used",
                "parent": "inhalants",
                "question": "Have you ever, even once, inhaled halothane, ether, or other anesthetics for kicks "
                            "or to get high?",
                "options": {
                    "1": "yes",
                    "2": "no",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",
                    "94": "DON'T KNOW",
                    "97": "REFUSED"
                }
            },
            "SOLVENT": {
                "substance": "paint solvent",
                "label": "paint solvent ever used",
                "parent": "inhalants",
                "question": "Have you ever, even once, inhaled lacquer thinner or other paint solvents for kicks "
                            "or to get high?",
                "options": {
                    "1": "yes",
                    "2": "no",
                    "3": "Yes LOGICALLY ASSIGNED",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",
                    "94": "DON'T KNOW",
                    "97": "REFUSED"
                }
            },
            "LGAS": {
                "substance": "lighter gases",
                "label": "lighter gases ever used",
                "parent": "inhalants",
                "question": "Have you ever, even once, inhaled lighter gases, such as butane or propane for kicks"
                            " or to get high?",
                "options": {
                    "1": "yes",
                    "2": "no",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",
                    "94": "DON'T KNOW",
                    "97": "REFUSED"
                }
            },
            "NITOXID": {
                "substance": "nitrous oxide",
                "label": "nitrous oxide ever used",
                "parent": "inhalants",
                "question": "Have you ever, even once, inhaled nitrous oxide or 'whippits' for kicks or to get "
                            "high?",
                "options": {
                    "1": "yes",
                    "2": "no",
                    "3": "Yes LOGICALLY ASSIGNED",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",
                    "94": "DON'T KNOW",
                    "97": "REFUSED"
                }
            },
            "FELTMARKR": {
                "substance": "magic markers",
                "label": "magic markers ever used",
                "parent": "inhalants",
                "question": "Have you ever, even once, inhaled felt-tip pens, felt-tip markers, or magic markers "
                            "for kicks or to get high?",
                "options": {
                    "1": "yes",
                    "2": "no",
                    "3": "Yes LOGICALLY ASSIGNED",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",
                    "94": "DON'T KNOW",
                    "97": "REFUSED"
                }
            },
            "SPPAINT": {
                "substance": "spray paints",
                "label": "spray paints ever used",
                "parent": "inhalants",
                "question": "Have you ever, even once, inhaled spray paints for kicks or to get high?",
                "options": {
                    "1": "yes",
                    "2": "no",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",
                    "94": "DON'T KNOW",
                    "97": "REFUSED"
                }
            },
            "AIRDUSTER": {
                "substance": "keyboard cleaner",
                "label": "keyboard cleaner ever used",
                "parent": "inhalants",
                "question": "Have you ever, even once, inhaled computer keyboard cleaner, also known as air duster,"
                            " for kicks or to get high?",
                "options": {
                    "1": "yes",
                    "2": "no",
                    "3": "Yes LOGICALLY ASSIGNED",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",
                    "94": "DON'T KNOW",
                    "97": "REFUSED"
                }
            },
            "OTHAEROS": {
                "substance": "other aerosols",
                "label": "other aerosols ever used",
                "parent": "inhalants",
                "question": "Have you ever, even once, inhaled some other aerosol spray for kicks or to get high?",
                "options": {
                    "1": "yes",
                    "2": "no",
                    "3": "Yes LOGICALLY ASSIGNED",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",
                    "94": "DON'T KNOW",
                    "97": "REFUSED"
                }
            },
            "INHALOTH": {
                "substance": "other inhalants",
                "label": "other inhalants ever used",
                "parent": "inhalants",
                "question": "Have you ever, even once used any other inhalants for kicks or to get high besides "
                            "the ones that have been listed?",
                "options": {
                    "1": "yes",
                    "2": "no",
                    "85": "BAD DATA Logically assigned",
                    "91": "NEVER USED",
                    "94": "DON'T KNOW",
                    "97": "REFUSED"
                }
            },
            "METHAMEVR": {
                "substance": "methamphetamine",
                "label": "methamphetamine ever used",
                "question": "Have you ever, even once, used methamphetamine?",
                "options": {
                    "1": "yes",
                    "2": "No",
                    "94": "DON'T KNOW",
                    "97": "REFUSED",
                }
            },
            # This is meant for all hallucinogens
            "HALLUCEVR": {
                "substance": "hallucinogens",
                "label": "hallucinogens ever used",
                "children": True,
                "question": "Have you ever, even once, used any hallucinogen?",
                "options": {
                    "1": "yes",
                    "91": "NEVER USED",
                    "97": "REFUSED",
                    "98": "BLANK (NO ANSWER)"
                }
            },
            "INHALEVER": {
                "substance": "inhalants",
                "label": "inhalants ever used",
                "children": True,
                "question": "Have you ever, even once, used any inhalant?",
                "options": {
                    "1": "yes",
                    "91": "NEVER USED",
                    "97": "REFUSED",
                    "98": "BLANK (NO ANSWER)"
                }
            },
            "PNRNMLIF": {  # any not directed by a doctor
                "substance": "pain relievers",
                "label": "pain relievers ever used",
                "question": "Have you ever, even once, used any prescription pain reliever?",
                "options": {
                    "1": "yes",
                    "2": "no",
                    "5": "Yes LOGICALLY ASSIGNED (from skip pattern)",
                    "94": "DON'T KNOW",
                    "97": "REFUSED",
                    "98": "BLANK (NO ANSWER)"
                }
            },
            "TRQANYLIF": {
                "substance": "tranquilizers",
                "label": "tranquilizers ever used",
                "question": "Have you ever, even once, used any tranquilizer?",
                "options": {
                    "1": "yes",
                    "2": "no",
                    "5": "Yes LOGICALLY ASSIGNED (from skip pattern)",
                    "94": "DON'T KNOW",
                    "97": "REFUSED",
                    "98": "BLANK (NO ANSWER)"
                }
            },
            "STMANYLIF": {
                "substance": "stimulants",
                "label": "stimulants ever used",
                "question": "Have you ever, even once, used stimulants?",
                "options": {
                    "1": "yes",
                    "2": "no",
                    "5": "Yes LOGICALLY ASSIGNED (from skip pattern)",
                    "94": "DON'T KNOW",
                    "97": "REFUSED",
                    "98": "BLANK (NO ANSWER)"
                }
            },
            "SEDANYLIF": {
                "substance": "sedatives",
                "label": "sedatives ever used",
                "question": "Have you ever, even once, used sedatives?",
                "options": {
                    "1": "yes",
                    "2": "no",
                    "5": "Yes LOGICALLY ASSIGNED (from skip pattern)",
                    "94": "DON'T KNOW",
                    "97": "REFUSED",
                    "98": "BLANK (NO ANSWER)"
                }
            }
        }
        return ever_used

    def feature_keys(self, as_labels=False, parent_substances_only=False) -> list:
        """
        :param as_labels: if true, returns the value of the label contained in each feature instead of the original feature key
        :return: a list of all available feature keys
        """
        if as_labels:
            if parent_substances_only:
                return [v['label'] for _, v in self.features().items() if 'parent' not in v.keys()]
            else:
                return [v['label'] for _, v in self.features().items()]
        else:
            if parent_substances_only:
                return [k for k,v in self.features().items() if 'parent' not in v.keys()]
            else:
                return [k for k,_ in self.features().items()]

    def concrete_substance_feature_keys(self, as_labels=False,
                                        parent_substances=None) -> list:
        """
        selects the features that belong to a parent substance, i.e. substances that belong to the specified category.
        (example. LCD is a substance of the category hallucinogens)
        :param as_labels: if true, instead of the original feature key the value of the label corresponding to each selected feature is returned
        :param parent_substances: the name of the parent substances (e.g., inhalants) from which you want to return
        the list of specific substances to which they belong
        :return: a list with the selected features according to the given parameters
        """
        if parent_substances is None:
            parent_substances = ['hallucinogens', 'inhalants']
        features_ = []
        for feature_key, v in self.features().items():
            parent = "parent"
            if parent in v.keys():
                for parent_substance in parent_substances:
                    if v[parent] == parent_substance:
                        if as_labels:
                            features_.append(v['label'])
                        else:
                            features_.append(feature_key)
        return features_

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

            ops = {
                "1": (1, "yes"),
                "2": (991, "no"),  # NEVER USED [DRUG(s) OF INTEREST] Logically assigned
                "3": (1, "yes"),  # "Yes LOGICALLY ASSIGNED"
                "5": (1, "yes"),  # Yes LOGICALLY ASSIGNED
                "85": (985, "BAD DATA Logically assigned"),
                # BAD DATA Logically assigned (i.e., usually inconsistent with other data)
                "94": (994, "DON'T KNOW"),
                "97": (997, "REFUSED"),
                "98": (998, "BLANK (NO ANSWER)"),
                "91": (991, "no"),  # NEVER USED [DRUG(s) OF INTEREST] Logically assigned

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


if __name__ == "__main__":
    mu = 8.
    sigma = 2.5
    x = mu + np.random.randn(10000) * sigma
    print(np.random.randn(10000))
