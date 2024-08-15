from tortoise.queryset import QuerySet


def apply_pagination(
    queryset: QuerySet, page: int = 1, page_size: int = 10
) -> QuerySet:
    """
    Apply pagination to a Tortoise QuerySet.

    :param queryset: The queryset to paginate.
    :param page: The page number.
    :param page_size: The size of each page.

    :return: The paginated queryset.
    """
    offset = (page - 1) * page_size
    return queryset.offset(offset).limit(page_size)
