from option_queries import *

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

peck_scenarios = {
    'peck_config_1': {
        'name': 'peck_config_1',
        'machine_config': machine_config,
        'work_piece_config': work_piece_config,
        'config': {
            ReferenceXQuery: 50,
            ReferenceYQuery: 45,
            CutDepthQuery: 11.35
        },
        'description': 'Makes a single peck',
        'benchmark': {
            'num_drawn_entities': {
                'XY': {
                    'oval': 1,
                    'rectangle': 1  # includes workpiece
                },
                'YZ': {
                    'oval': 0,
                    'rectangle': 2  # includes workpiece
                },
                'XZ': {
                    'oval': 0,
                    'rectangle': 2  # includes workpiece
                }
            }
        }
    },
}

bug_fix_1 = {}
bug_fix_1.update(peck_scenarios['peck_config_1'])
bug_fix_1['name'] = 'peck_bug_fix_1'
bug_fix_1['description'] = 'Challenges whether GemoetricFeature creates new drawing_class child on work_piece change (it shouldn\'t).'
bug_fix_1['test-drawing-post-instructions']= {
    'XY': [
        'feature_manager.features[0].drawGeometry()'
    ]
}

peck_scenarios['peck_bug_fix_1'] = bug_fix_1
