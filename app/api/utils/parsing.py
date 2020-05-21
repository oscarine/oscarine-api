def remove_none_from_dict(dictionary) -> dict:
    """
    :param dictionary: Dictionary from which keys whose values are
    None are to be removed.
    :return: Dictionary with no key of value None
    """
    return {k: v for k, v in dictionary.items() if v is not None}


def convert_cost_units(items):
    """To convert cost_unit choice type to it's
        value. For example, for each item's cost_unit
        tuple (type="per-packet", value="Per Packet")
        will be converted to a `str` "Per Packet".
    """
    for item in items:
        item.cost_unit = item.cost_unit.value
    return items
