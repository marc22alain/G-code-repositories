from MachinedGeometry_class import MachinedGeometry
from Tkinter import *
from SpinboxQuery_class import SpinboxQuery
from EntryQuery_class import EntryQuery


class RoundBottomedDado(MachinedGeometry):
    data_query_defs =  [{"name":"Stock Width", "type":DoubleVar, "input_type": EntryQuery}, \
                        {"name":"Stock Height", "type":DoubleVar, "input_type": EntryQuery}, \
                        {"name":"Stock Length", "type":DoubleVar, "input_type": EntryQuery}, \
                        {"name":"Bottom Radius", "type":DoubleVar, "input_type": EntryQuery}]

    name = "Round Bottomed Dado"
    version = "0.9"

    def __init__(self):
        self.entry_queries = self._makeEntryQueries()

    def getDataQueries(self):
        return self.entry_queries

    def getGeometry(self, data):
        self.assertValid(data)
        return {}

    def assertValid(self, data):
        pass

    def _makeEntryQueries(self):
        entry_queries = []
        for query in self.data_query_defs:
            entry_queries.append(query["input_type"](query))
        return entry_queries
