import numpy as np
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt


class Last30DaysDataService(object):
    """
    service class that implements the expected functionality for the analysis of features related to substance use in the last 30 days
    """

    def __init__(self, data_service):
        self.ds = data_service

    def last_30d_used_dataframe_and_chart(self, dataframe=None, features=None, title=None):
        """
        Create the interactive chart with information on substance used in past month behaviors by age category
        :param dataframe: the dataframe containing the data necessary to create the plot
        :param features: list of required substance ever used features to be included in the chart
        :param title: The chart title
        :return: the dataframe containing the data displayed on the chart as well as the altair chart with the
                information of substances consumed in last 30 days according to the entered features
        """
        try:
            # creates a dataframe with the desired feature keys (column names) that are contained in the "last_30_days_use"
            # feature group
            df_ = dataframe[features]

            # Replaces the feature keys of the dataframe columns with the substance names
            feature_keys_and_substances_dict = self.ds.feature_service.features[
                'last_30_days_use'].feature_key_and_substance_value(as_labels=True)
            df_ = df_.rename(columns=feature_keys_and_substances_dict)

            # gets the total number of people by age category
            number_of_observations = df_['age category'].value_counts()
            number_of_observations.loc['All ages'] = number_of_observations.sum()

            df_ = df_.groupby(by=['age category']).count()
            df_.loc['All ages'] = df_.sum()

            # calculates the proportion of people who have consumed a substance X with respect to the total
            # of observations by age category
            for col in df_.columns:
                for row in df_.index:
                    df_.loc[row, col] = df_.loc[row, col] / number_of_observations.loc[row]
            df_['total people'] = number_of_observations

            # displays each input data in a separate row so that it can be plotted with altair
            data_by_row = []
            for row in df_.index:
                for col in df_.columns:
                    if col != 'total people':
                        proportion_of_people = df_.at[row, col]
                        total_people = df_.at[row, 'total people']
                        data_by_row.append(
                            {'age category': row,
                             'substance': col,
                             'proportion of people': proportion_of_people,
                             'total people': total_people,
                             'positive cases': round(total_people * proportion_of_people)
                             })

            df_by_row = pd.DataFrame(data_by_row)

            # Selectable age groups
            options = np.insert(df_by_row['age category'].unique(), 0, None)
            labels = np.insert(df_by_row['age category'].unique(), 0, 'Age groups stacked')
            input_dropdown = alt.binding_select(options=options, labels=labels)
            selection = alt.selection_single(fields=['age category'], bind=input_dropdown, name='Select by ')
            color = alt.condition(selection,
                                  alt.Color('age category:N', legend=None),
                                  alt.value('lightgray'))

            chart = alt.Chart(df_by_row).mark_bar().encode(
                x=alt.X('substance', sort="-y"),
                y=alt.Y('proportion of people:Q'),
                color='age category:N',
                tooltip=['age category', 'substance', alt.Tooltip('proportion of people:Q', format='.1%'),
                         'total people',
                         'positive cases']
            ).add_selection(
                selection
            ).transform_filter(
                selection
            ).properties(
                width=750,
                height=400,
                title=title
            )
            return df_, chart
        except Exception:
            print("Please specify a dataframe, a list of features and a chart title")

    def all_substances_df_and_chart(self, dataframe=None):
        """
        It generates a dataframe and an interactive bar chart with all substances consumed in last 30 days by the participants
        of the survey.

        :param dataframe: the main dataframe from which the specific dataframe with the selected features is derived
        :return: - A dataframe with the calculated data according to the features given as parameter
                 - The dynamic bar chart type altair with the data specified in the dataframe
        """
        try:
            if dataframe is None:
                raise Exception
            # accesses the "last_30_days_use" feature group instance. This instance contains the corresponding
            # feature list with the question
            # "How many days have you used substance x in past month"
            last_30_days_use_feature_group = self.ds.feature_service.features['last_30_days_use']

            # returns the keys (column names) associated with the "last_30_days_use" feature group.
            last_30_days_use_features = last_30_days_use_feature_group.feature_keys(as_labels=True)
            # contains the features retrieved from the "last_30_days_use" feature group and the 'age' demographic feature
            features = ['age category']
            features.extend(last_30_days_use_features)

            # Dataframe with the desired features and altair chart
            last_30_days_use_df, last_30_days_use_chart = self.last_30d_used_dataframe_and_chart(dataframe=dataframe,
                                                                                                 features=features,
                                                                                                 title="Substances used in last 30 days by age group")
            return last_30_days_use_df, last_30_days_use_chart
        except Exception:
            print("Please specify a main dataframe")
