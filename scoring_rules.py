# From NFHS individual tournament scoring rules
def get_advancement_points(round_name):
    """Returns advancement points based on the round type."""
    if any(x in round_name for x in ["Champ.", "Quarterfinal", "Semifinal"]):
        return 2.0
    elif "Cons." in round_name:
        return 1.0
    return 0.0

def get_bonus_points(win_method):
    """Returns bonus points based on the method of victory."""
    method = win_method.lower()
    if "fall" in method and "tech" not in method:
        return 2.0
    if any(x in method for x in ["forfeit", "default", "disqualification"]):
        return 2.0
    if "tech fall" in method:
        return 1.5
    if "major decision" in method:
        return 1.0
    return 0.0

def get_placement_points(round_name):
    """Returns a tuple of placement points: (winner_points, loser_points)."""
    if "1st Place Match" in round_name:
        return 16.0, 12.0
    elif "3rd Place Match" in round_name:
        return 10.0, 9.0
    elif "5th Place Match" in round_name:
        return 7.0, 6.0
    
    # Not a placement match
    return 0.0, 0.0