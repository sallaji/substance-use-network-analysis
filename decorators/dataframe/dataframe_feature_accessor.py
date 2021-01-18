import pandas as pd
from services.featureservice import FeatureService
import numpy as np


@pd.api.extensions.register_dataframe_accessor("feature")
class DataframeFeatureAccessor:
    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    @staticmethod
    def _validate(obj):
        pass

    def parse(self, value_label=False, value_is_parsed=False):
        dataframe_ = self._obj.copy()
        for col in dataframe_.columns:
            dataframe_[col] = dataframe_[col].apply(
                lambda feature_value: FeatureService().find_feature_group_by_feature_name(feature_key=col).parse_option(
                    feature_value=feature_value, feature_key=col, value_label=value_label,
                    value_is_parsed=value_is_parsed))
        return dataframe_

    def drop_rows_with_no_substance_use_at_all_in_last_30_days(self):
        dataframe_ = self._obj.copy()
        substance_features_30d = FeatureService().features["last_30_days_use"].feature_keys(as_labels=True)
        drop_rows = []
        for idx, row in dataframe_.iterrows():
            found = []
            for feature in substance_features_30d:
                if pd.isna(row[feature]):
                    found.append(idx)
            if len(found) == len(substance_features_30d):
                drop_rows.append(idx)
        dataframe_ = dataframe_.drop(index=drop_rows)
        return dataframe_

    def drop_rows_with_invalid_data(self, features=None):
        dataframe_ = self._obj.copy()
        if features is None:
            for col in dataframe_.columns:
                dataframe_ = dataframe_[dataframe_[col].notnull()]
        else:
            for feature in features:
                dataframe_ = dataframe_[dataframe_[feature].notnull()]
        return dataframe_

    def replace_invalid_options(self):
        """
        The data must be already parsed!
        :return:
        """
        dataframe_ = self._obj.copy()
        for col in dataframe_.columns:
            dataframe_[col].mask(dataframe_[col] >= 900, -1, inplace=True)
        return dataframe_

    def labelize_features_and_options(self):
        """
        data must be already parsed
        :return:
        """
        dataframe_ = self._obj.copy()
        columns = []
        for feature_key in dataframe_.columns:
            feature_group = FeatureService().find_feature_group_by_feature_name(feature_key=feature_key)
            feature_label = feature_group.feature_label(feature_key=feature_key)
            columns.append(feature_label)
            dataframe_[feature_key] = dataframe_[feature_key].apply(
                lambda feature_value: FeatureService().find_feature_group_by_feature_name(
                    feature_key=feature_key).parse_option(
                    feature_value=feature_value, feature_key=feature_key, value_label=True,
                    value_is_parsed=True))
        dataframe_.columns = columns
        return dataframe_

    def value_label(self):
        return self.parse(value_label=True, value_is_parsed=True)
