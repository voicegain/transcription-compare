

BLUE_CODE = "#00c3ff"
YELLOW_CODE = "#f7fb00"
ORANGE_CODE = "#fb7900"
RED_CODE = "#fb0000"


def create_bg_color(substitution, insertion, deletion):

    if deletion > 0:  # blue
        return "bgcolor={}".format(BLUE_CODE)
    elif substitution > 0 and insertion == 0:  # yellow
        return "bgcolor={}".format(YELLOW_CODE)
    elif substitution > 0 and insertion > 0:  # orange
        return "bgcolor={}".format(ORANGE_CODE)
    elif substitution == 0 and insertion > 0:  # red
        return "bgcolor={}".format(RED_CODE)
    else:
        return ""
