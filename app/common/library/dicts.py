def create_dict_for_attributes(**kwargs):
    new_dict = {}

    for key, value in kwargs.items():
        if value is not None:
            new_dict[key] = value  # .replace("_", " ")

    return new_dict
