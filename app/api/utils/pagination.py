def pagination(query, page_size: int = 10, page_number: int = 1):
    if page_size:
        query = query.limit(page_size)
    if page_number:
        query = query.offset((page_number - 1) * page_size)
    return query
