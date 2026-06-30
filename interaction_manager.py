MIN_SCROLL_SPEED=0.08
MIN_PAN_SPEED=0.12
MIN_PINCH_SPEED=0.01
PAGE="page_jump_mode"
READ="read_mode"
ASK="query_mode"

# Gives which gesture and motion gives which command
def get_command(gesture, motion, mode, num_act):

    # x and y directions
    x_direction = motion["x_direction"]
    y_direction = motion["y_direction"]

    # x and y Velocities
    x_velocity = motion["x_velocity"]
    y_velocity = motion["y_velocity"]

    # extracting pinch distance change and velocity
    pinch_distance = motion["pinch_distance"]
    pinch_velocity = motion["pinch_velocity"]


    # For Open Palm Gesture — Moving side by side
    if gesture == "5_opalm" and mode != PAGE and (x_velocity > MIN_PAN_SPEED or x_velocity < -1*MIN_PAN_SPEED):
        if x_direction == "right":
            return "move_right"

        elif x_direction == "left":
            return "move_left"


    # For Index-Middle Gesture — Scrolling
    elif gesture == "2_ind" and mode != PAGE and (y_velocity > MIN_SCROLL_SPEED or y_velocity < -1*MIN_SCROLL_SPEED):

        if y_direction == "up":
            return "scroll_down"

        elif y_direction == "down":
            return "scroll_up"


    # For Pinch Gesture — Zooming in and out
    elif gesture == "pinch" and mode != PAGE and (pinch_velocity > MIN_PINCH_SPEED or pinch_velocity < -1*MIN_PINCH_SPEED):

        if pinch_distance > 0:
            return "zoom_in"

        elif pinch_distance < 0:
            return "zoom_out"


    # For Italian Pinch Gesture — Changing opacity
    elif gesture == "italian_pinch" and (y_velocity > MIN_PAN_SPEED or y_velocity < -1*MIN_PAN_SPEED):

        if y_direction == "up":
            return "increase_opacity"

        elif y_direction == "down":
            return "decrease_opacity"

    
    # For Fist Gesture — Selecting the mode
    elif gesture == "fist" and (y_velocity < MIN_PAN_SPEED and y_velocity > -1*MIN_PAN_SPEED and x_velocity < MIN_PAN_SPEED and x_velocity > -1*MIN_PAN_SPEED):
        return "show_mode_selector"


# "hide_mode_selector" do something
# "increase_opacity" do something
# do something about page jump in app.js in line 330 important
# "close_menu", "open_query", "close_page_jump" do something


    # # When to use gesture fist to select
    # elif gesture == "fist" and (y_velocity > 0.08 or y_velocity < -1*0.08 or x_velocity > 0.08 or x_velocity < -1*0.08):


    #     if abs(y_velocity) > abs(x_velocity) and y_direction == "up":
    #         return "menu"

    #     elif abs(y_velocity) > abs(x_velocity) and y_direction == "down":
    #         return READ

    #     elif abs(y_velocity) < abs(x_velocity) and x_direction == "right":
    #         return ASK
        
    #     elif abs(y_velocity) < abs(x_velocity) and x_direction == "left":
    #         return PAGE
    

    # For Thumbs down Gesture — Selecting the mode
    elif gesture == "thumbs_down":
        return "cancel"


    # For Thumbs up Gesture — Selecting the mode  
    elif gesture == "6_tup" and (mode != PAGE or not num_act):
        return "confirm"
    

    # For returning 6
    elif gesture == "6_tup" and mode == PAGE and num_act:
        return "6"

    elif gesture in {"0", "1", "2_ind", "3", "4", "5_opalm", "7", "8", "9"} and mode == PAGE:

        return gesture


    return None