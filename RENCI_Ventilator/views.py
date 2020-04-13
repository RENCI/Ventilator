import json

from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import QuerySet
from django.core import serializers
from RENCI_Ventilator.models import Configuration, Calibration, Diagnostic  # , Pressure, Respiration
from RENCI_Ventilator.utils import run_diagnostic, get_respiration_data
from RENCI_Ventilator.sensor import SensorHandler

# start up the sensor handlers
sh_pressure = SensorHandler(False, 0)
sh_respiration = SensorHandler(False, 1)

# main entry point
def index(request):
    # render the main page
    return render(request, 'RENCI_Ventilator/index.html', {})


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


# gets the running instances
def data_req(request):
    # define legal request types
    legal_req_types: list = ['event', 'config', 'calib', 'diags', 'update']

    # get the request type
    req_type: str = request.GET.get('type')

    # init the return data
    ret_val: object = None

    # only legal commands can pass
    if req_type in legal_req_types:
        # config details do not need a parameter, all are returned
        if req_type == 'config':
            # get the data from the database
            ret_val = get_settings(Configuration)

        elif req_type == 'calib':
            # get the data from the database
            ret_val = get_settings(Calibration)

        # config details need a parameter
        elif req_type == 'diags':
            # start the diagnostics, this will insert records into the database
            group_number = run_diagnostic()

            # get the data from the database
            diag_items: QuerySet = Diagnostic.objects.filter(grouping=group_number)

            # convert the query set into json
            ret_val = serializers.serialize('json', diag_items)

            # convert the json to a string for posting back
            ret_val = json.loads(ret_val)

        # update a configuration or calibration entry
        elif req_type == 'update':
            legal_update_tables: list = ['config', 'calib']

            # get the setting type we will update
            table = request.GET.get('table')

            # was this a legitimate request
            if table in legal_update_tables:
                # get the params
                param = request.GET.get('param')

                # its a failure if there was no param passed for this type
                if param is None:
                    ret_val = 'Invalid or missing parameter(s).'
                else:
                    # check the table type
                    if table == 'config':
                        tbl_obj = Configuration
                    else:
                        tbl_obj = Calibration

                    # split the settings
                    settings = param.split('~')

                    # for each setting
                    for setting in settings:
                        # split param and value
                        item = setting.split('=')

                        # update the value
                        tbl_obj.objects.filter(param_name=item[0]).update(value=item[1])

                    ret_val = 'Settings saved.'
            else:
                ret_val = 'Invalid setting request.'

        elif req_type == 'event':
            # only each type of graph
            legal_params: list = ['Pressure', 'Respiration']

            # get any params if there are any
            param = request.GET.get('param')

            # we only expect either of the two types
            if param in legal_params:
                # get the correct sensor
                if param == 'Pressure':
                    # save the target DB table
                    # tbl_obj = Pressure

                    # get data from real sensor
                    sensor_value = sh_pressure.get_pressure()
                else:
                    # save the target DB table
                    # tbl_obj = Respiration

                    # get data from real sensor
                    sensor_value = sh_respiration.get_pressure()

                # save the sensor data
                ret_val = sensor_value

                # TODO: persist this data to the database

            else:
                ret_val = 'Invalid or missing event param.'

    # load the response and type, no caching here
    response = HttpResponse(json.dumps(ret_val), content_type='application/json')
    response['Cache-Control'] = 'no-cache'

    # return the resultant JSON to the caller
    return response
