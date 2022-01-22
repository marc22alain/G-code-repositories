from alpha_features import FingerJointedSplice

machine_params = {
    'bit_diameter': 6.35,
    'safe_z': 80,
    'feed_rate': 1000
}
"""
# for good splices
workpiece_params = {
    # 'stock_length': 0, ... not strictly required
    'stock_width': 41.275,  # 1.625"
    'stock_height': 7.9375  # 5/16 ""
}

# 'fit_factor': .175 somewhat splits the difference between top and bottom
# .2mm to .5mm difference total width
cutting_params = {
    'cut_per_pass': 4,
    'finger_depth': 20,  # includes the radii at both ends
    'fit_factor': - .175
}
"""

# for hidden finger joint
# get the hiding feature by setting Z zero at 2mm above the actual table
workpiece_params = {
    # 'stock_length': 0, ... not strictly required
    'stock_width': 20,  # 1.625"
    'stock_height': 19.2  # 5/16 ""
}

cutting_params = {
    'cut_per_pass': 4,
    'finger_depth': 26.35,  # includes the radii at both ends
    'fit_factor': - .175  # starting with the fit factor that works for splices
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
