import logging
import message

log = logging.getLogger(__name__)

# When determining the movement cost, diagonal and orthogonal squares do not
# cost the same.
DIAGONAL_COST = 3
ORTHOGONAL_COST = 2

# When determining action point cost of actions for high- or low- dexterity
# actors we apply a modifier, giving a bonus to high-dexterity actors and a
# penalty to low-dexterity actors.
APMOD_HIGHDEX = -1
APMOD_LOWDEX = 1
HIGHDEX_THRESHHOLD = 2
LOWDEX_THRESHHOLD = 2


def movement_cost(delta_y, delta_x):
    """Looks up the movement cost for a particular movement.

    Each diagonal movement costs 3 AP and each orthogonal movement costs 2 AP.
    """
    normal_y = abs(delta_y)
    normal_x = abs(delta_x)
    orthogonal_squares = abs(normal_y - normal_x)
    diaganol_squares = min(normal_y, normal_x)
    return orthogonal_squares * ORTHOGONAL_COST \
        + diaganol_squares * DIAGONAL_COST


def ap_mod(ap, dex):
    """Applies dexterity modifier to action point cost for one action."""
    modified_ap = ap
    if dex < LOWDEX_THRESHHOLD:
        modified_ap = ap + APMOD_LOWDEX
    if dex > HIGHDEX_THRESHHOLD:
        log.info("Applying high-dexterity bonus")
        modified_ap = ap + APMOD_HIGHDEX
    if modified_ap < 1:
        modified_ap = 1
    return modified_ap


def attack_bite(attacker, defender):
    """Performs a bite attack by the attacker onto the defender."""
    message.add("The zombie bites you.")

# Attributes should be between 1 and 4, inclusive.
ATTRIBUTE_MAX = 4
ATTRIBUTE_MIN = 1


def is_valid_attribute(attribute):
    """Verifies if an attribute is in a valid range."""
    return (ATTRIBUTE_MIN <= attribute <= ATTRIBUTE_MAX)
