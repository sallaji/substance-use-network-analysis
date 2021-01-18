import numpy as np
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt


class EverUsedDataService(object):

    def __init__(self, data_service):
        self.ds = data_service

    def ever_used_dataframe_and_chart(self, dataframe=None, features=None, title=None):
        """
        Create the interactive chart with information on ever-used substance use behaviors by age category
        :param dataframe: the dataframe containing the data necessary to create the plot
        :param features: list of required substance ever used features to be included in the chart
        :param title: The chart title
        :return: the dataframe containing the data displayed on the chart as well as the altair chart with the
                information of substances ever consumed according to the entered features
        """
        try:
            # creates a dataframe with the desired feature keys (column names) that are contained in the "ever_used"
            # feature group
            df_ = dataframe[features]

            # Replaces the feature keys of the dataframe columns with the substance names
            feature_keys_and_substances_dict = self.ds.feature_service.features[
                'ever_used'].feature_key_and_substance_value(as_labels=True)
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
                tooltip=['age category', 'substance', alt.Tooltip('proportion of people:Q', format='.1%'), 'total people',
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

    def plot_unique_substance_ever_used(self, ever_used_dataframe, substance_name):
        """
        creates a plot of the number of cases of substance ever consumed
        :param ever_used_dataframe:
        :param substance_name:
        :return:
        """
        dataframe_ = ever_used_dataframe.iloc[:-1].apply(lambda x: x.apply(lambda y: round(y * 100, 2)))
        substances_df_dict = {col: dataframe_[col].to_frame().rename(columns={col: '%'}) for col in dataframe_.columns}
        title = "Proportion of " + substance_name + " ever used with respect to the total observations for every age category"
        substance_df = substances_df_dict[substance_name]
        fig, ax = plt.subplots(1, 1, figsize=(10, 5))
        ax.set_ylabel("% with respect to all observations")
        plot_ = substance_df.plot(kind='bar', ax=ax, title=title)
        return plot_, substance_df

    def hallucinogens_df_and_chart(self, dataframe=None):
        """
        Generates a dataframe and an interactive bar chart with all hallucinogens ever consumed by the participants
        of the survey.

        :param dataframe: the main dataframe from which the specific dataframe with the selected features is derived
        :return: - A dataframe with the calculated data according to the features given as parameter
                 - The interactive altair bar chart with the data specified in the dataframe
        """
        try:
            if dataframe is None:
                raise Exception
            # returns the feature keys (column names) associated with the concrete hallucinogens contained in the
            # "ever_used" feature group
            hallucinogens_ever_used_features = self.ds.feature_service.features['ever_used'].concrete_substance_feature_keys(
                as_labels=True,
                parent_substances=[
                    'hallucinogens'])
            # contains the hallucinogen substance features retrieved from the "ever_used" feature group and the 'age'
            # demographic feature
            features = ['age category']
            features.extend(hallucinogens_ever_used_features)

            # Dataframe with the desired features and altair chart
            hallucinogens_ever_used_df, hallucinogens_ever_used_chart = self.ever_used_dataframe_and_chart(
                dataframe=dataframe,
                features=features,
                title="Hallucinogens ever used by age group")
            return hallucinogens_ever_used_df, hallucinogens_ever_used_chart
        except Exception:
            print("Please specify a main dataframe")


    def inhalants_df_and_chart(self, dataframe=None):
        """
        Generates a dataframe and an interactive bar chart with all inhalants ever consumed by the participants
        of the survey.

        :param dataframe: the main dataframe from which the specific dataframe with the selected features is derived
        :return: - A dataframe with the calculated data according to the features given as parameter
                 - The interactive altair bar chart with the data specified in the dataframe
        """
        try:
            if dataframe is None:
                raise Exception
            # returns the feature keys (column names) associated with the concrete inhalants contained in the
            # "ever_used" feature group
            inhalants_ever_used_features = self.ds.feature_service.features['ever_used'].concrete_substance_feature_keys(
                as_labels=True,
                parent_substances=[
                    'inhalants'])
            # contains the inhalant substance features retrieved from the "ever_used" feature group and the 'age'
            # demographic feature
            features = ['age category']
            features.extend(inhalants_ever_used_features)

            # Dataframe with the desired features and altair chart
            inhalants_ever_used_df, inhalants_ever_used_chart = self.ever_used_dataframe_and_chart(
                dataframe=dataframe,
                features=features,
                title="Inhalants ever used by age group")
            return inhalants_ever_used_df, inhalants_ever_used_chart
        except Exception:
            print("Please specify a main dataframe")

    def all_substances_df_and_chart(self, dataframe=None):
        """
        It generates a dataframe and an interactive bar chart with all substances ever consumed by the participants
        of the survey.

        :param dataframe: the main dataframe from which the specific dataframe with the selected features is derived
        :return: - A dataframe with the calculated data according to the features given as parameter
                 - The dynamic bar chart type altair with the data specified in the dataframe
        """
        try:
            if dataframe is None:
                raise Exception
            # accesses the "ever_used" feature group instance. This instance contains the corresponding feature list with the question
            # "have you ever used substance x"
            ever_used_feature_group = self.ds.feature_service.features['ever_used']

            # returns the keys (column names) associated with the "ever_used" feature group.
            #    if parent_substances_only = True it excludes those concrete substances that are children of a specific
            #    substance parent/category.(i.e. Concrete inhalants substances will be skipped and the  "inhalants" parent
            #    substance will be returned instead)
            ever_used_features = ever_used_feature_group.feature_keys(as_labels=True, parent_substances_only=True)
            # contains the features retrieved from the "ever_used" feature group and the 'age' demographic feature
            features = ['age category']
            features.extend(ever_used_features)

            # Dataframe with the desired features and altair chart
            ever_used_df, ever_used_chart = self.ever_used_dataframe_and_chart(dataframe=dataframe, features=features,
                                                                               title="Substances ever used by age group")
            return ever_used_df, ever_used_chart
        except Exception:
            print("Please specify a main dataframe")
