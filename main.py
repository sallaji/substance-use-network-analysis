if __name__ == "__main__":
    from services.networkservice import NetworkService
    from services.dataservice import DataService

    ns = NetworkService(DataService())

    # Accesses the preprocessed dataset by calling the dataService instance inside the networkService class
    dataframe = ns.ds.project_dataframe(nrows=2)
    print('===Preprocessed database (Version 1)===\n\n', dataframe.head())
    print(dataframe.shape)

    # Accesses the preprocessed dataset with data features transformed into understandable english language
    # Keep in mind that almost all of the available functionality works based on this variant!
    dataframe = ns.ds.project_dataframe(as_labels=True)
    print('===The (MAIN) preprocessed database (Version 2)===\n\n', dataframe.head())
    print(dataframe.shape)

    # Accesses the substances used in last 30 days networkx graph
    used_in_last_30_days_graph = ns.substance_used_in_last_30d_network(dataframe=dataframe)
    print('\n', ns.nx.info(used_in_last_30_days_graph), '\n')

    # Accesses the substance ever used networkx graph
    ever_used_graph = ns.substance_ever_used_network(dataframe=dataframe)
    print(ns.nx.info(ever_used_graph), '\n')

    # Accesses the people networkx graph
    people_graph = ns.people_network(dataframe=dataframe)
    print(ns.nx.info(people_graph), '\n')

    # Accesses the demographics feature group (this is analogue to the rest of available feature groups:
    #   Other available feature groups= [ever_used, last_30_days_use, mental_health]
    demographic_features = ns.ds.feature_service.features['demographics'].feature_keys(as_labels=True)
    print(demographic_features)

    # Now the dataframe can be reduced by simply passing the retrieved features as parameters
    print(dataframe[demographic_features].head(2))
