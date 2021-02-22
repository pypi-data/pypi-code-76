"""
MongoDB query constructors.
"""


def create_query(statuses=None, stages=None, amend=""):
    """Dynamically create a MongoDB query with given search parameters.

    :param statuses: status(es)
    :type statuses: str or list of strs
    :param stages: stage number(s)
    :type stages: int or list of ints
    :param amend: additional query conditions
    :type amend: str
    :returns: MongoDB query
    :rtype: str
    """
    if statuses and stages is None:  # 0 is a valid stage
        query = create_status_query(statuses)
    elif not statuses and stages is not None:
        query = create_stage_query(stages)
    else:
        query = {
            "$and": [
                create_status_query(statuses),
                create_stage_query(stages)
            ]
        }

    if amend:
        query = amend_to_query(query, amend)

    return query


def create_status_query(statuses):
    if isinstance(statuses, str):
        return {"status": {"$eq": statuses}}
    elif isinstance(statuses, (list, tuple)):
        return {"$or": [{"status": {"$eq": status}} for status in statuses]}
    else:
        raise TypeError("Pass status as a string or a sequence of strings.")


def create_stage_query(stages):
    if isinstance(stages, str) and stages.isdigit():
        stages = int(stages)

    if isinstance(stages, int):
        return {"stage": {"$eq": stages}}
    elif isinstance(stages, (list, tuple)):
        return {"$or": [{"stage": {"$eq": stage}} for stage in stages]}
    else:
        raise TypeError("Pass stages as an int or a sequence of ints.")


def amend_to_query(query, amend):
    if "$and" in query:
        query["$and"].append(amend)
    else:
        query = {"$and": [query, amend]}
    return query
