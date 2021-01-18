import networkx as nx
from services.dataservice import DataService
from config import ROOT_DIR


class PeopleNetworkService(object):

    def __init__(self, data_service):
        self.ds = data_service

    def people_network(self, dataframe, include_zero_substances_used_relationships=False,
                       include_nodes_with_zero_substances_used=False):
        df_ = dataframe[(dataframe['race'] == 'NonHisp Native Am/AK Native')
                        | (dataframe['race'] == 'NonHisp Native HI/Other Pac Isl')]
        depression_index = self.ds.mental_health_service.calculate_depression_index(dataframe=df_)
        feature_groups = self.ds.feature_service.features
        last_30d_substance_features = feature_groups['last_30_days_use'].feature_keys(as_labels=True)
        demographic_features = feature_groups['demographics'].feature_keys(as_labels=True)
        demographic_features.remove('age')
        mental_health_features = feature_groups['mental_health'].feature_keys(as_labels=True)
        wanted_attributes = demographic_features + last_30d_substance_features + mental_health_features
        # Reduces the dataframe with the wanted attributes only
        df_ = df_[wanted_attributes]
        df_['depression index'] = depression_index
        # remove nan depression values
        df_ = df_[df_['depression index'].notna()]
        # df_ = df_[df_['poverty level'] != 'Replacing nan']
        for feature in last_30d_substance_features:
            df_[feature] = df_[feature].fillna(0)
            df_[feature] = df_[feature].astype('int32')

        df_ = df_.drop(columns=[col for col in last_30d_substance_features if df_[col].sum() == 0])
        participant_nodes = {}
        for i in df_.index:
            node_attributes = df_.loc[i].to_dict()
            substances_used_features = [feature for feature in last_30d_substance_features if
                                        feature in node_attributes.keys() and node_attributes[feature] > 0]
            if include_nodes_with_zero_substances_used is False and len(substances_used_features) == 0:
                continue
            else:
                total_days_of_substances_used = sum(
                    [node_attributes[feature] for feature in substances_used_features])
                node_attributes.update(
                    {'total days': int(total_days_of_substances_used),
                     'total substances': len(substances_used_features)})
                participant_nodes.update({str(i): node_attributes})

        participant_edges = self.people_network_relationships(participant_nodes,
                                                              include_zero_substances_used_relationships=include_zero_substances_used_relationships)
        participant_nodes_list = [(node_id, node_attrs) for node_id, node_attrs in participant_nodes.items()]
        G = nx.Graph()
        G.add_nodes_from(participant_nodes_list)
        G.add_edges_from(participant_edges)

        return G

    def people_network_relationships(self, participant_nodes=None,
                                     include_zero_substances_used_relationships=False):
        last_30d_feature_group = self.ds.feature_service.features['last_30_days_use']
        last_30d_substance_features = last_30d_feature_group.feature_keys(as_labels=True)
        substance_name_by_feature_keys = last_30d_feature_group.feature_key_and_substance_value(as_labels=True)
        edges = []
        traversed_nodes = []
        for participant_i in participant_nodes.keys():

            total_substances_used_i = participant_nodes[participant_i]['total substances']

            for participant_j in participant_nodes.keys():
                total_substances_used_j = participant_nodes[participant_j]['total substances']
                if participant_i != participant_j and participant_j not in traversed_nodes:
                    if total_substances_used_i == 0 and total_substances_used_j == 0 and include_zero_substances_used_relationships:
                        edges.append((participant_i, participant_j, {"substance use relationship": False, "weight": 1}))
                    else:
                        common_substance_use_days = 0
                        common_substances = 0
                        common_substance_names = []
                        edge_attributes = {}
                        for feature in last_30d_substance_features:
                            if feature in participant_nodes[participant_i].keys() and feature in participant_nodes[
                                participant_j].keys():
                                days_of_use_i = participant_nodes[participant_i][feature]
                                days_of_use_j = participant_nodes[participant_j][feature]
                                if (days_of_use_i > 0 and days_of_use_j > 0):
                                    common_substance_use_days += min(days_of_use_j, days_of_use_i)
                                    common_substances += 1
                                    common_substance_names.append(substance_name_by_feature_keys[feature])
                        if common_substance_use_days > 0 and common_substances > 0:
                            common_substance_names_attributes = {substance: substance for substance in
                                                                 common_substance_names}
                            edge_attributes.update({"common substance use days": common_substance_use_days,
                                                    "substance use relationship": True,
                                                    "weight": 1,
                                                    "number of common substances": common_substances})
                            edge_attributes.update(common_substance_names_attributes)
                            edges.append((participant_i, participant_j, edge_attributes))
            traversed_nodes.append(participant_i)
        return edges

    def write_gephi_file(self, G, filename):
        nx.write_gexf(G, ROOT_DIR + "/data/" + filename)


if __name__ == "__main__":
    ds = DataService()
    ns = PeopleNetworkService(data_service=ds)
    last_30d_feature_group = ds.feature_service.features['last_30_days_use'].feature_keys(as_labels=True)
    G = ns.people_network(dataframe=ds.project_dataframe(as_labels=True),
                          include_zero_substances_used_relationships=False,
                          include_nodes_with_zero_substances_used=False)
    ns.write_gephi_file(G, "people_network2.gexf")
