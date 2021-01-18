from services.substance_use_network_service import SubstanceNetworkService
from services.people_network_service import PeopleNetworkService
import networkx as nx
from config import ROOT_DIR
import pandas as pd
import matplotlib.pyplot as plt


class NetworkService(object):
    """

    """

    def __init__(self, data_service):
        self.ds = data_service
        self.substance_network_service = SubstanceNetworkService(self.ds)
        self.people_network_service = PeopleNetworkService(self.ds)
        self.nx = nx

    def write_gephi_file(self, G, filename):
        nx.write_gexf(G, ROOT_DIR + "/data/" + filename)

    def draw_weighted_network(self, graph, weight_name='consumers', title='', labels=True):
        """

        :param graph:
        :param weight_name:
        :param title:
        :return:
        """
        G = graph
        fig, ax = plt.subplots(1, 1, figsize=(20, 20))
        pos = nx.spring_layout(G)
        d = dict(G.degree(weight=weight_name))
        # nx.draw_networkx_nodes(G, pos, node_color='lightsteelblue',
        #                        node_size=[60000 * (v / sum(d.values())) for v in d.values()], alpha=0.5)

        nx.draw_networkx_nodes(G, pos, node_color=['lightsteelblue' if v != 0 else 'salmon' for v in d.values()],
                               node_size=[60000 * ((0.1 + v) / sum(d.values())) for v in d.values()], alpha=0.5)

        G_weights = [data[weight_name] for (i, j, data) in G.edges(data=True) if weight_name in data]
        G_weights_unique = list(set(G_weights))
        for weight in G_weights_unique:
            weighted_edges = [(node1, node2) for (node1, node2, edge_attr) in G.edges(data=True) if
                              weight_name in edge_attr and edge_attr[weight_name] == weight]
            width = weight * 5 * len(list(G.nodes())) / sum(G_weights)
            nx.draw_networkx_edges(G, pos, edgelist=weighted_edges, width=width, alpha=0.8)
            if labels:
                nx.draw_networkx_labels(G, pos={k: ([v[0], v[1]]) for k, v in pos.items()}, font_size=16)
        ax.set_title(title)
        ax.axis("off")

    def substance_predictions(self, dataframe, predicted_links_df):
        last_30_d_feature_group = self.ds.feature_service.features['last_30_days_use']
        last_30_d_features = last_30_d_feature_group.feature_keys(as_labels=True)
        substance_feature_keys_and_names_as_values = last_30_d_feature_group.feature_key_and_substance_value(
            as_labels=True)
        prediction_strings = []
        for idx_row in predicted_links_df.index:
            row = predicted_links_df.loc[idx_row]
            consumer_a = int(row.iloc[0])
            consumer_b = int(row.iloc[1])
            prediction_value = row.iloc[2]
            algorithm = row.index[2]
            # Substances to be likely consumed by person a in the future (those substances already consumed by b)
            predicted_consumption_for_a = [substance_feature_keys_and_names_as_values[feature] for feature in
                                           list(dataframe[last_30_d_features].loc[consumer_b].dropna().index.values)]
            # Substances to be likely consumed by person b in the future (those substances already consumed by a)
            predicted_consumption_for_b = [substance_feature_keys_and_names_as_values[feature] for feature in
                                           list(dataframe[last_30_d_features].loc[consumer_a].dropna().index.values)]
            string = "Predicted substances for:\n  - Consumer id {}: {}\n  - Consumer id {}: {}\n  - {}: {}".format(
                consumer_a,
                predicted_consumption_for_a,
                consumer_b,
                predicted_consumption_for_b,
                algorithm, prediction_value)
            prediction_strings.append(string)
        return prediction_strings

    def substance_ever_used_network(self, dataframe):
        G_ = self.substance_network_service.substance_network(dataframe=dataframe, nrows=None,
                                                              feature_group_name='ever_used',
                                                              edge_attributes=[
                                                                  'felt down, no good or worthless in past month',
                                                                  'poverty level', 'age category'])
        return G_

    def substance_used_in_last_30d_network(self, dataframe):
        G_ = self.substance_network_service.substance_network(dataframe=dataframe, nrows=None,
                                                              feature_group_name='last_30_days_use',
                                                              edge_attributes=[
                                                                  'felt down, no good or worthless in past month',
                                                                  'poverty level', 'age category'])
        return G_

    def substance_centralities(self, substance_network_graph, weight='consumers'):
        G = substance_network_graph
        df_ = pd.DataFrame(dict(
            degree=dict(G.degree()),
            weighted_degree=dict(G.degree(weight=weight)),
            degree_normalized=nx.degree_centrality(G),
            eigenvector_centrality=nx.eigenvector_centrality(G),
            closeness_centrality=nx.closeness_centrality(G),
            betweenness_centrality=nx.betweenness_centrality(G),
            cluster_coefficient=nx.clustering(G),
            weighted_cluster_coefficient=nx.clustering(G, weight=weight)
        ))
        return df_.sort_values(by=['weighted_degree'], ascending=False)

    def people_network(self, dataframe, include_zero_substances_used_relationships=False,
                       include_nodes_with_zero_substances_used=False):
        G_ = self.people_network_service.people_network(dataframe=dataframe,
                                                        include_zero_substances_used_relationships=include_zero_substances_used_relationships,
                                                        include_nodes_with_zero_substances_used=include_nodes_with_zero_substances_used)
        return G_

# if __name__ == "__main__":
