from option_queries import *
from features import *

machine_config = {
    BitDiameterQuery: 6.35,
    SafeZQuery: 80,
    FeedRateQuery: 1000
}

work_piece_config = {
    StockLengthQuery: 100,
    StockWidthQuery: 100,
    StockHeightQuery: 15
}


ldist_scenarios = {
    'ldist_config_1': {
        'name': 'odcg_config_1',
        'machine_config': machine_config,
        'work_piece_config': work_piece_config,
        'config': {
            GeometricFeatureQuery: 'CircularGroove',
            DeltaXQuery: 1.2,
            DeltaYQuery: 2.375,
            NumRepeatQuery: 3
        },
        'description': 'Makes a single pass',
        'child_features': {
            CircularGroove: {
                PathDiameterQuery: 6.175,
                ReferenceXQuery: 0,
                ReferenceYQuery: 0,
                CutPerPassQuery: 2,
                CutDepthQuery: 1
            }
        }
    }
}
