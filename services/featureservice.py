#!/usr/bin/env python3

from data.model.features import *


class FeatureService(object):
    """
    class of service that contains as an attribute the groups of available features.
    """
    def __init__(self):
        # A dictionary with all available feature groups
        self.features = dict(
            age_first_use=FeatureAgeFirstUse(),
            ever_used=FeatureEverUsed(),
            demographics=FeatureDemographics(),
            last_30_days_use=FeatureDaysOfUseLast30Days(),
            mental_health=FeatureMentalHealth()
        )

    def get_feature_key_list(self, feature_groups=None, as_labels=False):
        """
        Return the list of available features for this project
        :param feature_groups: (Optional) if true it returns the feature list only for the specified feature group
        :param as_labels: Return feature list as understandable English phrases
        :return: a list of features
        """
        try:
            grouped = []
            if feature_groups is None:
                for (k, v) in self.features.items():
                    grouped += v.feature_keys(as_labels=as_labels)
            else:
                for feature_group in feature_groups:
                    if feature_group not in self.features:
                        raise KeyError('There is no a feature group called {}'.format(feature_group))
                    grouped += self.features[feature_group]
            return grouped
        except KeyError:
            print("Incorrect feature group name")
            raise

    def find_feature_group_by_feature_name(self, feature_key, as_labels=False):
        try:
            feature_group_found = False
            for feature_group_key in self.features.keys():
                feature_group_found = feature_key in self.features[feature_group_key].feature_keys(as_labels=as_labels)
                if feature_group_found:
                    return self.features[feature_group_key]
            if feature_group_found is False:
                raise Exception(
                    'Could not find feature group by feature_key: {}.'.format(feature_key))
        except Exception:
            print("An error occurred while trying to find the feature group")
            raise

    def parse_feature_option(self, feature_key, feature_value, value_label=None, value_is_parsed=False):
        feature_group = self.find_feature_group_by_feature_name(feature_key)
        return feature_group.parse_option(feature_value=feature_value,
                                          feature_key=feature_key,
                                          value_label=value_label,
                                          value_is_parsed=value_is_parsed)
