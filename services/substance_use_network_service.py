import pandas as pd
import networkx as nx
import copy


class SubstanceNetworkService(object):
    def __init__(self, data_service):
        self.ds = data_service

    def substance_network(self, dataframe=None, nrows=None, feature_group_name=None, edge_attributes=None):
        """
        :param dataframe:
        :param nrows:
        :param feature_group_name:
        :param edge_attributes:
        :return:
        """
        try:
            substance_feature_group = self.ds.feature_service.features[feature_group_name]

            substance_feature_keys = substance_feature_group.feature_keys(as_labels=True, parent_substances_only=True)

            feature_keys_substance_names = substance_feature_group.feature_key_and_substance_value(
                as_labels=True)

            if dataframe is None:
                print("Please specify a dataframe")
                raise Exception

            if nrows is not None:
                dataframe = dataframe[:nrows]
            substance_use_dataframe = dataframe[substance_feature_keys]
            substance_nodes = {}
            for feature in substance_use_dataframe.columns:
                consumers = set(substance_use_dataframe[substance_use_dataframe[feature].notnull()].index.tolist())
                substance_name = feature_keys_substance_names[feature]
                if substance_name not in substance_nodes:
                    substance_nodes[substance_name] = {}
                    substance_nodes[substance_name]['consumers'] = consumers
                    # The node attributes
                    substance_node_attributes = {}
                    substance_node_attributes.update({"substance name": substance_name})

                    age_categories = dataframe['age category'].unique()

                    # gets the feature name by substance name
                    substance_names_keys_feature_name_values = {v: k for k, v in self.ds.feature_service.features[
                        'last_30_days_use'].feature_key_and_substance_value(
                        as_labels=True).items()}

                    for age_category in age_categories:
                        average_day_use_in_past_month_age_category = round(dataframe.loc[
                                                                               (dataframe[
                                                                                    substance_names_keys_feature_name_values[
                                                                                        substance_name]] > 0) & (
                                                                                       dataframe[
                                                                                           'age category'] == age_category),
                                                                               substance_names_keys_feature_name_values[
                                                                                   substance_name]].mean(), 2)
                        if pd.isna(average_day_use_in_past_month_age_category):
                            average_day_use_in_past_month_age_category = 0
                        substance_node_attributes.update({
                            age_category + ' average day use in last month': average_day_use_in_past_month_age_category})
                    all_consumers_average_day_use_in_last_month = round(dataframe.loc[
                                                                            (dataframe[
                                                                                 substance_names_keys_feature_name_values[
                                                                                     substance_name]] > 0),
                                                                            substance_names_keys_feature_name_values[
                                                                                substance_name]].mean(), 2)
                    if pd.isna(all_consumers_average_day_use_in_last_month):
                        all_consumers_average_day_use_in_last_month = 0
                    substance_node_attributes.update({
                        'average day use in last month (all categories)': all_consumers_average_day_use_in_last_month})
                    substance_nodes[substance_name]['attributes'] = {}
                    substance_nodes[substance_name]['attributes'] = substance_node_attributes
            if edge_attributes is None:
                edge_attributes = []  # edge attrs must be a list!
                print("No specific edge attributes specified. Generating default edge attributes")
                all_feature_groups = self.ds.feature_service.features
                for feature_group in all_feature_groups.values():
                    for feature in feature_group.feature_keys(as_labels=True):
                        edge_attributes.append(feature)

            # The copy is used to identify those consumers of the only substance used in order to create the substance
            # loop edges
            substance_nodes_copy = copy.deepcopy(substance_nodes)
            traversed_substances = []
            edge_list = []

            for substance_i in substance_nodes.keys():
                for substance_j in substance_nodes.keys():
                    if substance_i != substance_j and substance_j not in traversed_substances:
                        consumers_in_i = substance_nodes[substance_i]['consumers']
                        consumers_in_j = substance_nodes[substance_j]['consumers']
                        common_consumers = consumers_in_i.intersection(consumers_in_j)

                        if len(common_consumers) > 0:
                            calculated_edges = self.calculate_edges(substance_i=substance_i, substance_j=substance_j,
                                                                    common_consumers=common_consumers,
                                                                    edge_attributes=edge_attributes,
                                                                    dataframe=dataframe)
                            edge_list.extend(calculated_edges)

                            substance_nodes_copy[substance_i]['consumers'].difference_update(common_consumers)

                traversed_substances.append(substance_i)

            for substance in substance_nodes_copy.keys():
                common_consumers = substance_nodes_copy[substance]['consumers']
                if len(substance_nodes_copy[substance]) > 0:
                    calculated_edges = self.calculate_edges(substance_i=substance, substance_j=substance,
                                                            common_consumers=common_consumers,
                                                            edge_attributes=edge_attributes,
                                                            dataframe=dataframe)
                    edge_list.extend(calculated_edges)
            substance_nodes_with_attributes_as_list = [(k, v['attributes']) for k, v in substance_nodes.items()]
            G = nx.Graph(name=feature_group_name)
            # Add the previously calculated edges
            G.add_nodes_from(substance_nodes_with_attributes_as_list)
            G.add_edges_from(edge_list)
            return G
            # return substance_nodes_with_attributes_as_list, edge_list

        except Exception:
            print("Something went wrong creating the nodes and edges for substance use")

    def calculate_edges(self, substance_i, substance_j, common_consumers, edge_attributes, dataframe):
        edges = []
        calculated_edge_attributes = {}
        if len(common_consumers) > 0:
            for feature in edge_attributes:
                edge_attribute = {}
                for consumer_id in common_consumers:
                    given_answer = dataframe[feature][consumer_id]
                    if pd.notna(given_answer):
                        attribute_label = feature + " " + str(given_answer)
                        if attribute_label in edge_attribute:
                            edge_attribute[attribute_label] += 1
                        else:
                            edge_attribute[attribute_label] = 1
                if bool(edge_attribute):
                    calculated_edge_attributes.update(edge_attribute)
            calculated_edge_attributes.update({"consumers": len(common_consumers), "weight": 1})
            edges.append((substance_i, substance_j, calculated_edge_attributes))
        return edges

# if __name__ == "__main__":
#     sns = SubstanceNetworkService()
#     dataframe = sns.ds.project_dataframe(as_labels=True, nrows=None)
#     # print(dataframe['Days of alcohol use in past month'])
#     ever_used_G = sns.substance_network(dataframe=dataframe, nrows=None, feature_group_name='ever_used',
#                                          edge_attributes=['felt down, no good or worthless in past month',
#                                                           'poverty level', 'age category'])
#     # print(nodes)
#     ns = NetworkService()
#     ns.write_gephi_file(ever_used_G, "ever_used2.gexf")
#
#     last_30d_G = sns.substance_network(dataframe=dataframe, nrows=None, feature_group_name='last_30_days_use',
#                                          edge_attributes=['felt down, no good or worthless in past month',
#                                                           'poverty level', 'age category'])
#     ns.write_gephi_file(last_30d_G, "last_30_days_use2.gexf")
#
#     # print(edges)
