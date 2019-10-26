def remove_none_from_dict(dictionary) -> dict:
    """
    :param dictionary: Dictionary from which keys whose values are
    None are to be removed.
    :return: Dictionary with no key of value None
    """
    return {k: v for k, v in dictionary.items() if v is not None}
