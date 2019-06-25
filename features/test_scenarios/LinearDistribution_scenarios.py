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
        'name': 'ldist_config_1',
        'machine_config': machine_config,
        'work_piece_config': work_piece_config,
        'config': {
            GeometricFeatureQuery: 'CircularGroove',
            DeltaXQuery: 1.2,
            DeltaYQuery: 2.375,
            NumRepeatQuery: 3
        },
        'description': 'Makes a single pass with CircularGroove',
        'child_features': {
            CircularGroove: {
                PathDiameterQuery: 6.175,
                ReferenceXQuery: 0,
                ReferenceYQuery: 0,
                CutPerPassQuery: 2,
                CutDepthQuery: 1
            }
        }
    },
    'ldist_config_2': {
        'name': 'ldist_config_2',
        'machine_config': machine_config,
        'work_piece_config': work_piece_config,
        'config': {
            GeometricFeatureQuery: 'Peck',
            ReferenceXQuery: 3.75,
            ReferenceYQuery: 3.75,
            DeltaXQuery: 1.2,
            DeltaYQuery: 2.375,
            NumRepeatQuery: 3
        },
        'description': 'Makes a single pass with Peck',
        'child_features': {
            Peck: {
                ReferenceXQuery: 0,
                ReferenceYQuery: 0,
                CutDepthQuery: 7.23
            }
        },
        'benchmark': {
            'num_drawn_entities': {
                'XY': {
                    'oval': 3,
                    'rectangle': 1  # includes workpiece
                },
                'YZ': {
                    'oval': 0,
                    'rectangle': 4  # includes workpiece
                },
                'XZ': {
                    'oval': 0,
                    'rectangle': 4  # includes workpiece
                }
            }
        }
    },
    'ldist_config_3': {
        'name': 'ldist_config_3',
        'machine_config': machine_config,
        'work_piece_config': work_piece_config,
        'config': {
            GeometricFeatureQuery: 'CircularGroove',
            DeltaXQuery: -1.2,
            DeltaYQuery: -2.375,
            NumRepeatQuery: 3
        },
        'description': 'Makes a two passes with CircularGroove',
        'child_features': {
            CircularGroove: {
                PathDiameterQuery: 16.3175,
                ReferenceXQuery: 0,
                ReferenceYQuery: 0,
                CutPerPassQuery: 2.5,
                CutDepthQuery: 3
            }
        }
    }
}

bug_fix_1 = {}
bug_fix_1.update(ldist_scenarios['ldist_config_2'])
bug_fix_1['name'] = 'ldist_bug_fix_1'
bug_fix_1['description'] = 'Challenges whether LinearDistribution deletes child entities on view change'
bug_fix_1['test-drawing-pre-instructions']= {
    'YZ': [
        'feature_manager.features[0].features[0].option_queries[CutDepthQuery].setValue(6)',
        'feature_manager.features[0].features[0].didUpdateQueries()'
    ],
    'XZ': [
        'feature_manager.features[0].features[0].option_queries[CutDepthQuery].setValue(8)',
        'feature_manager.features[0].features[0].didUpdateQueries()'
    ]
}

ldist_scenarios['ldist_bug_fix_1'] = bug_fix_1
