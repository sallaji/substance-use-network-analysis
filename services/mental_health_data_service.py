import numpy as np
import pandas as pd


class MentalHealthDataService(object):

    def __init__(self, data_service):
        self.ds = data_service

    def substance_use_depression_index_correlations(self, dataframe, methods=None):
        dataframe_ = dataframe.copy()
        # create index bb

        if methods is None:
            methods = ['pearson', 'spearman', 'kendall']
        try:
            if dataframe is None:
                print("Please give a valid dataframe")

        except Exception:
            print("Something went wrong when calculating the substance use depression index correlations")

    def calculate_depression_index(self, dataframe):
        """
        Calculates the depression index according to the four mental health features
        :param dataframe: The labelized dataframe containing the answers given by the participants for each required
        mental health feature
        :return: a pandas.Series object containing the calculated depression index for each observation
        """
        try:
            if dataframe is None:
                print("Please specify a dataframe")
                raise Exception

            # Creates a copy for AVOIDING MUTATIONS!!
            dataframe_ = dataframe.copy()
            # The labelized options will be recoded for average calculation capability
            options = {
                "All of the time": 4,
                "Most of the time": 3,
                "Some of the time": 2,
                "A little of the time": 1,
                "None of the time": 0,
            }

            def parse_option(option):
                """
                Parses the option to its corresponding integer value if the participant's answer is included in the
                options dictionary keys
                :param option: the participants given answer
                :return: the parsed option if option is key of options, otherwise the old option value will be returned
                """
                if option in options.keys():
                    return options[option]
                else:
                    return option

            for column in dataframe_.columns:
                dataframe_[column] = dataframe_[column].apply(lambda x: parse_option(x))

            mental_health_feature_labels = self.ds.feature_service.features['mental_health'].feature_keys(
                as_labels=True)  # Access to all mental_health features contained in the group

            dataframe_ = dataframe_[mental_health_feature_labels]  # creates a df with the wanted features only
            return dataframe_.mean(axis=1)  # calculates the average by row
        except Exception:
            print("An error has occured while trying to calculate the depression index")
