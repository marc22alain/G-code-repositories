# here we define the list of bits to choose from:
#   3.175mm = 1/8"
#   4.763mm = 3/16"
#   6.35mm = 1/4"
#   9.525mm = 3/8"
#   11.135mm = 7/16"
#   12.7mm = 1/2"
#   19.05mm = 3/4"
bits = (3.175, 4.763, 6.35, 9.525, 11.135, 12.7, 19.05)
ball_noses = (9.525, 12.7, 19.05)
default_safe_Z = 100
default_feed_rate = 1000
default_tab_width = 6.35


# the marcotypes machine's spacings between rows of locating holes
spoil_board_spacings = (0, 270 ,800, 1070)

mortisingBits = {
    '6.35': {
        'diameter': 6.35,
        'length': 40
    }
}

mortisingJig = {
    'locationHoleYcoord': 0,
    'jigCenterlineOffset': 0,
    'jigWidth': 100,
    'stileEndReference': 100,
    'railEndReference': 120,
    'railFaceReferenceOffset': 0, # offset from jig width
}
