import pandas as pd
from services.featureservice import FeatureService


@pd.api.extensions.register_series_accessor("feature")
class SeriesFeatureAccessor:
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def value_label(self):
        series_ = self._obj.copy()
        if isinstance(series_.index, pd.MultiIndex):
            return self.value_label_multiindex()
        else:
            new_series_keys = {}
            for k, v in series_.items():
                feature_value = k
                if isinstance(series_.index, pd.RangeIndex):
                    feature_value = v
                parsed_key = FeatureService() \
                    .find_feature_group_by_feature_name(feature_key=series_.name).parse_option(feature_value=feature_value,
                                                                                               feature_key=series_.name,
                                                                                               value_label=True,
                                                                                               value_is_parsed=True)
                new_series_keys[k] = parsed_key
            return series_.rename(new_series_keys)

    def value_label_multiindex(self):
        series_ = self._obj.copy()
        tuples = []
        names = series_.index.names
        for tuple in series_.index:
            tuple_obj = ()
            for idx, name in enumerate(names):
                parsed_key = FeatureService().find_feature_group_by_feature_name(feature_key=name).parse_option(
                    feature_key=name, feature_value=tuple[idx], value_label=True, value_is_parsed=True)
                tuple_obj = tuple_obj + (parsed_key,)
            tuples.append(tuple_obj)
        new_multiIndex = pd.MultiIndex.from_tuples(tuples, names=names)
        return pd.Series(series_.values, index=new_multiIndex)

    def rename(self):
        series_ = self._obj.copy()
        if isinstance(series_.index, pd.MultiIndex):
            return self.rename_multiindex()
        found_tag = FeatureService().find_feature_group_by_feature_name(feature_key=series_.name).feature_label(
            feature_key=series_.name)
        series_.name = found_tag
        return series_

    def rename_multiindex(self):
        series_ = self._obj.copy()
        names = series_.index.names
        new_names = []
        for name in names:
            new_name = FeatureService().find_feature_group_by_feature_name(feature_key=name).feature_label(
                feature_key=name)
            new_names.append(new_name)
        series_.index.names = new_names
        return series_
