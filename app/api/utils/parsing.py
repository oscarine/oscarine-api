def convert_cost_units(items):
    """To convert cost_unit choice type to it's
        value. For example, for each item's cost_unit
        tuple (type="per-packet", value="Per Packet")
        will be converted to a `str` "Per Packet".
    """
    for item in items:
        item.cost_unit = item.cost_unit.value
    return items
