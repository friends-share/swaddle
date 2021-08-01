from src.storage.cache.store import AppStore, ClusterDataStore, CommandStore, \
    GroupedDataStore

app_store = AppStore()
cluster_data_store = ClusterDataStore()
cmd_store = CommandStore()
grouped_data_store = GroupedDataStore()
