#!/usr/bin/env python3

import os

from services.featureservice import FeatureService
from services.fetch_data import FetchData
from services.ever_used_data_service import EverUsedDataService
from services.last_30_days_data_service import Last30DaysDataService
from services.demographics_data_service import DemographicsDataService
from services.mental_health_data_service import MentalHealthDataService
import pandas as pd
import decorators.dataframe.dataframe_feature_accessor
import decorators.series.series_feature_accessor
from config import ROOT_DIR
import json


class DataService(object):

    def __init__(self):
        self.feature_service = FeatureService()
        self.fetch_data = FetchData()
        self.ever_used_service = EverUsedDataService(self)
        self.last_30_days_of_use_service = Last30DaysDataService(self)
        self.demographics_service = DemographicsDataService(self)
        self.mental_health_service = MentalHealthDataService(self)
        self.dataframe_args = dict(compression='zip', sep='\t')

        self.tsv_zip_filename = ROOT_DIR + '/data/NSDUH_2019_tsv.zip'
        self.tsv_zip_filename_preprocessed = ROOT_DIR + '/data/NSDUH_2019_tsv_preprocessed.zip'
        self.tsv_zip_filename_preprocessed_as_labels = ROOT_DIR + '/data/NSDUH_2019_tsv_preprocessed_as_labels.zip'

    def read_original_tsv_file(self, nrows=None, features=None):
        """

        :param nrows: Number of rows to be read. None means all rows
        :param features: desired feature list to be read
        :return: a dataframe as a result of reading the original downloaded tsv zip file
        """
        try:
            if self.tsv_zip_filename is None:
                raise Exception('File not found')
            if not os.path.isfile(self.tsv_zip_filename):
                self.fetch_data.fetch_db_and_write_tsv_file(filepath=self.tsv_zip_filename)
            print("Reading data from dataset file...")
            df = pd.read_csv(self.tsv_zip_filename, **self.dataframe_args, nrows=nrows, usecols=features)

            print("Dataframe of original database was sucessfully read.")
            return df
        except Exception:
            print("Please specify a correct filepath")

    def project_dataframe(self, nrows=None, features=None, as_labels=False):
        """
        Reads the original database (or preprocessed file if available) for this specific project
        :param nrows: The desired number of rows to be read
        :param features: te desired features (columns to be read)
        :param as_labels: If true, the dataframe will return the feature and option names as understandable english
        :return: a dataframe containing the requested features and rows
        """
        try:
            if features is None:
                if as_labels:
                    features = self.feature_service.get_feature_key_list(as_labels=as_labels)
                else:
                    features = self.feature_service.get_feature_key_list()
            if as_labels:
                if not os.path.isfile(self.tsv_zip_filename_preprocessed_as_labels):
                    print(
                        "no pre-processed as label database file found\n\n  Creating a preprocessed as label database file...")
                    df = self.read_preprocessed_datafile(nrows=None)
                    df = df.feature.labelize_features_and_options()

                    df.to_csv(self.tsv_zip_filename_preprocessed_as_labels, **self.dataframe_args)
                return pd.read_csv(self.tsv_zip_filename_preprocessed_as_labels, **self.dataframe_args,
                                   usecols=features,
                                   nrows=nrows)
            else:
                return self.read_preprocessed_datafile(nrows=nrows)
        except Exception:
            print("an error has ocurre while reading the project dataframe ")

    def read_preprocessed_datafile(self, nrows=None):
        """
        Reads (and writes if necessary) the preprocessed datafile containing the features required for this specific project
        :param nrows:  Number of rows to be read. If None then all rows will be read
        :return:  The corresponding DataFrame containing the preprocessed data
        """
        features = self.feature_service.get_feature_key_list(as_labels=False)
        if not os.path.isfile(self.tsv_zip_filename_preprocessed):
            print("no pre-processed database file found\n\n  Creating a preprocessed database file...")
            df = self.read_original_tsv_file(nrows=None, features=features)
            if 'POVERTY3' in df.columns:
                df['POVERTY3'] = df['POVERTY3'].astype('Int64')
                df['POVERTY3'] = df['POVERTY3'].fillna(999)

            df = df.feature.parse()
            df = df.feature.replace_invalid_options()
            print("writing original data to zip file")
            df.to_csv(self.tsv_zip_filename_preprocessed, **self.dataframe_args)
        return pd.read_csv(self.tsv_zip_filename_preprocessed, **self.dataframe_args, usecols=features,
                           nrows=nrows, dtype='Int32')

    def ever_used_dataframe_and_chart(self, dataframe=None, features=None, title=None):
        return self.ever_used_service.ever_used_dataframe_and_chart(dataframe=dataframe, features=features, title=title)

    def people_to_json(self, nrows=None, features=None, use_data_labels=False,
                       skip_invalid_data=False, dataframe=None):
        """
        Generates a json of people. Each person object contains its respective feature attributes
        :param nrows: limits the number of people to be extracted from the database
        :param features: the features to create the person's attributes
        :param use_data_labels: if true the keys and values of the json object are populated with
                                the corresponding labels
        :param skip_invalid_data: if true it removes attributes with invalid data
        :param dataframe the data frame containing all the required attributes
        :return: a json object of people, each with his/her given attributes
        """
        # returns the dataframe with the answer given by each participant for each of the above mentioned features
        if dataframe is None:
            df = self.project_dataframe(features=features, nrows=nrows)
        else:
            df = dataframe.copy()
            if features is not None:
                df = df[features]
        if skip_invalid_data:
            df = df.feature.replace_invalid_options()
        if use_data_labels:
            df = df.feature.labelize_features_and_options()
        index_str_list = [str(i) for i in df.index]
        df['id'] = index_str_list
        df.set_index('id')
        result = df.to_json(orient="index")
        parsed_nodes = json.loads(result)
        parsed_nodes_without_empty_values = {}
        for parsed_node_key, parsed_node_attributes in parsed_nodes.items():
            if parsed_node_key not in parsed_nodes_without_empty_values:
                parsed_nodes_without_empty_values[parsed_node_key] = {}
            for attribute_key, attribute_value in parsed_node_attributes.items():
                if attribute_key == 'id':
                    continue
                if attribute_value != '':
                    parsed_nodes_without_empty_values[parsed_node_key][attribute_key] = attribute_value
        return parsed_nodes_without_empty_values.copy()

    def write_dataframe_as_csv(self, dataframe, filename):
        """
        writes the dataframe data to a csv file stored in the data directory
        :param dataframe: The convertible dataframe
        :param filename: the name of the resulting csv file (without file extension)
        """
        dataframe.to_csv(ROOT_DIR + '/data/' + filename + '.csv', sep=',', encoding='utf-8')


# this is code: dear python, please calculate the average of DSTCHR30, DSTNGD30, DSTHOP30, DSTEFF30. THANK YOU.
