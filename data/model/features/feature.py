class FeatureGroupInterface:  # an informal feature interface
    def features(self) -> dict:
        """:return the corresponding feature dictionary containing all features and attributes beloging to the group"""
        pass

    def feature_keys(self) -> list:
        """:return a list containing all feature (column names) from the group"""
        pass

    def get_option_value(self, feature_value, feature_key=None, value_is_parsed=False):
        pass

    def parse_option(self, feature_value, feature_key=None, value_label=False, value_is_parsed=False) -> object:
        """:return the parsed value according to the given feature_value."""
        pass

    def feature_labels(self) -> dict:
        """:return a dictionary of key,value pairs with feature as key and label as value"""
        pass

    def feature_label(self, feature_key) -> str:
        """:return the label matching the given feature_key"""
        pass
