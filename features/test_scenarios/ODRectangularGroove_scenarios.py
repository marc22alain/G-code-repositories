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

odrect_scenarios = {
    'odrect_config_1': {
        'name': 'odrect_config_1',
        'machine_config': machine_config,
        'work_piece_config': work_piece_config,
        'config': {
            ReferenceXQuery: 50,
            ReferenceYQuery: 45,
            SideXQuery: 4.185,
            SideYQuery: 3.25,
            CutPerPassQuery: 2,
            CutDepthQuery: 1
        },
        'description': 'Makes a single pass'
    },

    'odrect_config_2': {
        'name': 'odrect_config_2',
        'machine_config': machine_config,
        'work_piece_config': work_piece_config,
        'config': {
            ReferenceXQuery: 50,
            ReferenceYQuery: 45,
            SideXQuery: 4.185,
            SideYQuery: 3.25,
            CutPerPassQuery: 2,
            CutDepthQuery: 3
        },
        'description': 'Makes two passes',
        'benchmark': {
            'program': 'F1000.0 \nG90 \nG0 Z80.0 \nG91 \nG0 X50.0 Y45.0 \nG0 X1.0825 Y1.55 \nG90 \nG0 Z15.0 \nG1 Z13.0 \nG4 P0.5 \n# first\nG91 \nG1 X0.0 Y-3.1 \nG1 X-2.165 Y0.0 \nG1 X0.0 Y3.1 \nG1 X2.165 Y0.0 \nG90 \nG1 Z12.0 \nG4 P0.5 \n# last\nG91 \nG1 X0.0 Y-3.1 \nG1 X-2.165 Y0.0 \nG1 X0.0 Y3.1 \nG1 X2.165 Y0.0 \nG90 \nG0 Z80.0 \nG91 \nG0 X-1.0825 Y-1.55 \nG0 X-50.0 Y-45.0 \nG90 \nM2 \n'
        }
    }
}
