from alpha_features import FingerJointedSplice

machine_params = {
    'bit_diameter': 6.35,
    'safe_z': 80,
    'feed_rate': 1000
}

workpiece_params = {
    # 'stock_length': 0, ... not strictly required
    'stock_width': 41.275,  # 1.625"
    'stock_height': 7.9375  # 5/16 ""
}

cutting_params = {
    'cut_per_pass': 4,
    'finger_depth': 20,
    'fit_factor': 0
}

f = FingerJointedSplice(
    machine_params,
    workpiece_params,
    cutting_params
)

print('\n\n')
print(f.getAGCode())
print('\n\n\n\n\n\n - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n\n\n\n\n\n')
print(f.getBGCode())
print('\n\n')
