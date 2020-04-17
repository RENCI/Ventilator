from django.db.models import QuerySet


# gets the list of settings for the type passed
def get_settings(obj) -> dict:
    # get the data
    config_items: QuerySet = obj.objects.all()

    # create a list for the data
    settings: dict = {}

    # convert each record into a list of dicts
    for item in config_items:
        # make the conversion
        settings.update({item.param_name: {
            'id': item.id,
            'param_name': item.param_name,
            'description': item.description,
            'value': item.value,
            'ts': str(item.ts)
        }})

    # convert the data to json format
    return settings
