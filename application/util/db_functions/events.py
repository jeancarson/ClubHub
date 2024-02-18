from main import Row, query_db


def upcoming_events() -> list[Row] | None:
    """
    Returns a list of rows from the events table
    """

    # Add trigger to removed expired events?

    return query_db("SELECT * FROM events")

