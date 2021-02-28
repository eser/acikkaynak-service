from graphql_relay import from_global_id


def global_id_to_model_id(object_id):
    if object_id is None:
        return None

    resolved = from_global_id(object_id)

    return resolved[1]
