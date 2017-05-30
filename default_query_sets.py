import MC_defaults as MC


# setup_queries = [{"name":"Feed rate", "type":"double", "default":MC.default_feed_rate, "input_type": "entry"}, \
#                 {"name":"Safe Z travel height", "type":"double", "default":MC.default_safe_Z, "input_type": "entry"}, \
#                 {"name":"Maximum cut per pass", "type":"double", "input_type": "entry"}, \
#                 {"name":"Cutter diameter", "type":"double", "input_type": "spinbox", "values":MC.bits}]

# machine_params = { "Feed rate": EntryQuery({"name":"Feed rate", "type":DoubleVar, "default":MC.default_feed_rate}), \
#                    "Safe Z travel height": EntryQuery({"name":"Safe Z travel height", "type":DoubleVar, "default":MC.default_safe_Z}), \
#                    "Maximum cut per pass": EntryQuery({"name":"Maximum cut per pass", "type":DoubleVar, "input_type": EntryQuery}), \
#                    "Cutter diameter": SpinboxQuery({"name":"Cutter diameter", "type":DoubleVar, "values":MC.bits})}


def makeSetupQueries(data_types, query_types):
    EntryQuery = query_types["entry"]
    SpinboxQuery = query_types["spinbox"]
    double_type = data_types["double"]
    machine_params = { "Feed rate": EntryQuery({"name":"Feed rate", "type":DoubleVar, "default":MC.default_feed_rate}), \
                   "Safe Z travel height": EntryQuery({"name":"Safe Z travel height", "type":DoubleVar, "default":MC.default_safe_Z}), \
                   "Maximum cut per pass": EntryQuery({"name":"Maximum cut per pass", "type":DoubleVar, "input_type": EntryQuery}), \
                   "Cutter diameter": SpinboxQuery({"name":"Cutter diameter", "type":DoubleVar, "values":MC.bits})}
    return machine_params

def makeSquareStockQueries(data_types, query_types):
    EntryQuery = query_types["entry"]
    double_type = data_types["double"]
    stock_params = { "Stock Length - X": EntryQuery({"name":"Stock Length - X", "type":double_type}),
                    "Stock Width - Y": EntryQuery({"name":"Stock Width - Y", "type":double_type}),
                    "Stock Height - Z": EntryQuery({"name":"Stock Height - Z", "type":double_type})}
    return stock_params
