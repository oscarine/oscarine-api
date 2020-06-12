"""
`pending` is the default type.

`declined` type will be used by shops, but the order
can't be declined once the order has been accepted.

`accepted`, `delivered` type will also be used by shops.

`cancelled` type will be used by users.
"""

ORDER_STATUS_TYPES = [
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('declined', 'Declined'),
    ('cancelled', 'Cancelled'),
    ('delivered', 'Delivered'),
]
