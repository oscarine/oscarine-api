from starlette.requests import Request


def get_db(request: Request):
    return request.state.db


def clone_db_model(model):
    """
    To create the clone of sqlalchemy model.

    Primary key data (like `id`) will not be copied to the cloned model.

    https://stackoverflow.com/a/55991358/10305905

    Parameters
    ----------
    `model` : Sqlalchemy model
    """
    # Ensure the model’s data is loaded before copying.
    model.id
    table = model.__table__
    # Non primary key columns.
    non_pk_columns = [k for k in table.columns.keys() if k not in table.primary_key]
    data = {c: getattr(model, c) for c in non_pk_columns}
    clone = model.__class__(**data)
    return clone
