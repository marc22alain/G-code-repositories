from Tkinter import *
import MC_defaults as MC
from SpinboxQuery_class import SpinboxQuery
from EntryQuery_class import EntryQuery

setup_queries = [{"name":"Feed rate", "type":DoubleVar, "default":MC.default_feed_rate, "input_type": EntryQuery}, \
                {"name":"Safe Z travel height", "type":DoubleVar, "default":MC.default_safe_Z, "input_type": EntryQuery}, \
                {"name":"Maximum cut per pass", "type":DoubleVar, "input_type": EntryQuery}, \
                {"name":"Cutter diameter", "type":DoubleVar, "input_type": SpinboxQuery, "values":MC.bits}]

machine_params = { "Feed rate": EntryQuery({"name":"Feed rate", "type":DoubleVar, "default":MC.default_feed_rate}), \
                   "Safe Z travel height": EntryQuery({"name":"Safe Z travel height", "type":DoubleVar, "default":MC.default_safe_Z}), \
                   "Maximum cut per pass": EntryQuery({"name":"Maximum cut per pass", "type":DoubleVar, "input_type": EntryQuery}), \
                   "Cutter diameter": SpinboxQuery({"name":"Cutter diameter", "type":DoubleVar, "values":MC.bits})}
