
from MachinedGeometry_class import MachinedGeometry
from default_query_sets import makeSetupQueries, makeSquareStockQueries
import simple_generators as G

# We need a better repository for all this data:
from FeatureDistributor_class import FeatureDistributor
from LinearDistributionFunction_class import LinearDistributionFunction
from Dado_class import Dado
features = { "dado": Dado }
distribution_functions = { "linear distribution": LinearDistributionFunction }


class DistributedFeature(MachinedGeometry):
    # class variables:
    name = "Repeated Feature"
    version = "0.9"
    implements_toolpass_view = False

    def __init__(self):
        pass

    # This is far too repetitive; it should be enough to provide the specials by querying the feature:
    #   [{"name":"Delta - X", "type":double_type},
    #    {"name":"Delta - Y", "type":double_type}]
    # Although this leaves a gap for reducing the standard queries ... the feature can ignore irrelevant input, but the user
    # may be forced to provide it anyway. Perhaps validity checks can be more helpful ?
    def makeQueries(self, data_types, query_types):
        EntryQuery = query_types["entry"]
        double_type = data_types["double"]
        integer_type = data_types["integer"]
        string_type = data_types["string"]
        SpinboxQuery = query_types["spinbox"]
        # Ideally, we would have separators to isolate the function input values
        # ... can we include separators in self.entry_queries ?
        # ! new thing ! the entry view must change as the features and functions are chosen
        # ! must rethink ! user won't want to lose input provided for other parameters, such as stock or bit
        self.selected_feature_param = SpinboxQuery({"name":"Feature", "type":string_type, "values":("dado",)})
        self.selected_function_param = SpinboxQuery({"name":"Distribution Function", "type":string_type, "values":("linear distribution",)})
        self.num_repetitions_param = EntryQuery({"name":"Number of Repetitions", "type":integer_type})
        # What we need to abstract:
        self.x_delta_param = EntryQuery({"name":"Delta - X", "type":double_type})
        self.y_delta_param = EntryQuery({"name":"Delta - Y", "type":double_type})

        self.machine_params = makeSetupQueries(data_types, query_types)
        stock_params = makeSquareStockQueries(data_types, query_types)
        self.stock_height_param = stock_params["Stock Height - Z"]
        # Also must be abstracted:
        self.params = [self.stock_height_param, self.x_delta_param, self.y_delta_param]
        self.entry_queries = self.machine_params.values() + self.params

    # This is a silly method: all implementations do the same thing, so don't make it abstract.
    def getDataQueries(self):
        return self.entry_queries

    def getGeometry(self):
        self.assertValid()
        if not self.feature_distributor:
            self.feature_distributor = FeatureDistributor(self.selected_feature, self.selected_function, self.num_repetitions)

        feed_rate = self.machine_params["Feed rate"].getValue()
        safe_Z = self.machine_params["Safe Z travel height"].getValue()

        g_code = G.startProgram(feed_rate)
        g_code += G.G.set_ABS_mode()
        g_code += G.G.G0_Z(safe_Z)
        g_code += self.feature_distributor.generateCode()
        g_code += G.end_program()
        return g_code

    def assertValid(self):
        pass

    def generateGcode(self):
        self.assertValid()
        if not self.feature_distributor:
            self.feature_distributor = FeatureDistributor(self.selected_feature, self.selected_function, self.num_repetitions)
        return self.feature_distributor.generateCode()

    def getToolPasses(self):
        pass

    def getViewSpaceInit(self):
        pass



df = DistributedFeature()

from Tkinter import *
from SpinboxQuery_class import SpinboxQuery
from EntryQuery_class import EntryQuery
data_types = {
    "string": StringVar,
    "double": DoubleVar,
    "boolean": BooleanVar,
    "integer": IntVar
}
query_types = {
    "spinbox": SpinboxQuery,
    "entry": EntryQuery
}
df.makeQueries(data_types, query_types)
