from option_queries import *

machine_config = {
    BitDiameterQuery: 5.0,
    SafeZQuery: 80,
    FeedRateQuery: 1000
}

work_piece_config = {
    StockLengthQuery: 100,
    StockWidthQuery: 100,
    StockHeightQuery: 15
}

circ_pock_scenarios = {
    'circ_pock_config_1': {
        'name': 'circ_pock_config_1',
        'machine_config': machine_config,
        'work_piece_config': work_piece_config,
        'config': {
            PathDiameterQuery: 26.175,
            ReferenceXQuery: -50,
            ReferenceYQuery: 45,
            CutPerPassQuery: 2,
            CutDepthQuery: 1
        },
        'description': 'Makes a single pass'
    },

    'circ_pock_config_2': {
        'name': 'circ_pock_config_2',
        'machine_config': machine_config,
        'work_piece_config': work_piece_config,
        'config': {
            PathDiameterQuery: 26.175,
            ReferenceXQuery: 10,
            ReferenceYQuery: 14.5,
            CutPerPassQuery: 2,
            CutDepthQuery: 3
        },
        'description': 'Makes two passes',
        'benchmark': {
            'program': 'F1000.0 \nG90 \nG0 Z80.0 \nG91 \nG0 X10.0 Y14.5 \nG90 \nG0 Z15.0 \nG1 Z13.0 \nG4 P0.5 \n# first\nG91 \nG1 X-4.5 Y0.0 \nG17 G2 X0.0 Y0.0 I4.5 J0.0 P1 \nG1 X-4.5 Y0.0 \nG17 G2 X0.0 Y0.0 I9.0 J0.0 P1 \nG1 X-1.5875 Y0.0 \nG17 G2 X0.0 Y0.0 I10.5875 J0.0 P1 \nG0 X10.5875 Y0.0 \nG90 \nG1 Z12.0 \nG4 P0.5 \n# last\nG91 \nG1 X-4.5 Y0.0 \nG17 G2 X0.0 Y0.0 I4.5 J0.0 P1 \nG1 X-4.5 Y0.0 \nG17 G2 X0.0 Y0.0 I9.0 J0.0 P1 \nG1 X-1.5875 Y0.0 \nG17 G2 X0.0 Y0.0 I10.5875 J0.0 P1 \nG90 \nG0 Z80.0 \nG91 \nG0 X10.5875 Y0.0 \nG0 X-10.0 Y-14.5 \nG90 \nM2 \n'
        }
    },
}
