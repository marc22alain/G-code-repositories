import MC_defaults as MC


def makeSetupQueries(data_types, query_types):
    EntryQuery = query_types["entry"]
    SpinboxQuery = query_types["spinbox"]
    double_type = data_types["double"]
    machine_params = { "Feed rate": EntryQuery({"name":"Feed rate", "type":double_type, "default":MC.default_feed_rate}), \
                   "Safe Z travel height": EntryQuery({"name":"Safe Z travel height", "type":double_type, "default":MC.default_safe_Z}), \
                   "Maximum cut per pass": EntryQuery({"name":"Maximum cut per pass", "type":double_type, "input_type": EntryQuery}), \
                   "Cutter diameter": SpinboxQuery({"name":"Cutter diameter", "type":double_type, "values":MC.bits})}
    return machine_params

def makeSquareStockQueries(data_types, query_types):
    EntryQuery = query_types["entry"]
    double_type = data_types["double"]
    stock_params = { "Stock Length - X": EntryQuery({"name":"Stock Length - X", "type":double_type}),
                    "Stock Width - Y": EntryQuery({"name":"Stock Width - Y", "type":double_type}),
                    "Stock Height - Z": EntryQuery({"name":"Stock Height - Z", "type":double_type})}
    return stock_params
