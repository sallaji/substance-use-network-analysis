import numpy as np
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt


class DemographicsDataService(object):

    def __init__(self, data_service):
        self.ds = data_service

    def age_by_sex_df_and_chart(self, dataframe=None):
        """
        creates an altair chart with demographic data (age category and sex ) of the people who are part of the survey.
        :param dataframe:
        :return:
        """
        try:
            if dataframe is None:
                print("Dataframe for demographics cannot be None")
                raise Exception
            demographics_features = self.ds.feature_service.features['demographics'].feature_keys(as_labels=True)
            demographics = dataframe[demographics_features]
            age_by_sex = demographics.groupby(by=['age category', 'sex'])['sex'].size().reset_index(name="people")
            chart = alt.Chart(age_by_sex).mark_bar().encode(
                column=alt.Column('age category', header=alt.Header(labelAngle=-90, labelAlign='right')),
                x=alt.X('sex', title='', axis=alt.Axis(labels=False)),
                y=alt.Y('people:Q'),
                tooltip=['age category', 'sex', 'people'],
                color=alt.Color('sex', scale=alt.Scale(range=['#B12020', '#2051B1']))
            ).properties(
                width=50,
                height=300,
                title='Number of people by age category and sex'
            )
            return age_by_sex, chart
        except Exception:
            print("An error occured while calculating the age by sex df and chart")

    def race_by_sex_df_and_chart(self, dataframe=None):
        """
        creates an altair chart with demographic data  (race and sex) of the people who are part of the survey.
        :param dataframe:
        :return:
        """
        try:
            if dataframe is None:
                print("Dataframe for demographics cannot be None")
                raise Exception
            demographics_features = self.ds.feature_service.features['demographics'].feature_keys(as_labels=True)
            demographics = dataframe[demographics_features]
            race_by_sex = demographics.groupby(by=['race', 'sex'])['sex'].size().reset_index(name="people")
            chart = alt.Chart(race_by_sex).mark_bar().encode(
                column=alt.Column('race', header=alt.Header(labelAngle=-90, labelAlign='right')),
                x=alt.X('sex', title='', axis=alt.Axis(labels=False)),
                y=alt.Y('people:Q'),
                tooltip=['race', 'sex', 'people'],
                color=alt.Color('sex', scale=alt.Scale(range=['#B12020', '#2051B1']))
            ).properties(
                width=50,
                height=300,
                title='Number of people by race and sex'
            )
            return race_by_sex, chart
        except Exception:
            print("An error occured while calculating the age by sex df and chart")

    def overall_health_by_sex_df_and_chart(self, dataframe=None):
        """
        creates an altair chart with demographic data (health and sex) of the people who are part of the survey.
        :param dataframe:
        :return:
        """
        try:
            if dataframe is None:
                print("Dataframe for demographics cannot be None")
                raise Exception
            demographics_features = self.ds.feature_service.features['demographics'].feature_keys(as_labels=True)
            demographics = dataframe[demographics_features]
            sorted_categories = ["Excellent", "Very good", "Good", "Fair", "Poor"]
            overall_health_by_sex = demographics.groupby(by=['health', 'sex'])['sex'].size().reset_index(name="people")
            overall_health_by_sex['health'] = pd.Categorical(overall_health_by_sex['health'], sorted_categories)
            overall_health_by_sex = overall_health_by_sex.sort_values('health').reset_index(drop=True)
            chart = alt.Chart(overall_health_by_sex).mark_bar().encode(
                column=alt.Column('health', header=alt.Header(labelAngle=-90, labelAlign='right'),
                                  sort=sorted_categories),
                x=alt.X('sex', title='', axis=alt.Axis(labels=False)),
                y=alt.Y('people:Q'),
                tooltip=['health', 'sex', 'people'],
                color=alt.Color('sex', scale=alt.Scale(range=['#B12020', '#2051B1']))
            ).properties(
                width=50,
                height=300,
                title='Number of people by overall health and sex'
            )
            return overall_health_by_sex, chart
        except Exception:
            print("An error occured while calculating the age by sex df and chart")
