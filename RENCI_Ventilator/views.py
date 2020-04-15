import json

from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import QuerySet
from django.core import serializers
from RENCI_Ventilator.models import Configuration, Calibration, Diagnostic  # , Pressure, Respiration
from RENCI_Ventilator.utils import run_diagnostic, get_settings
from RENCI_Ventilator.sensor import SensorHandler
import pandas as pd
import numpy as np

# init a couple global params for the sensors
sh_pressure = None


# main entry point
def index(request):
    # create global variables for the devices
    global sh_pressure

    # start up the sensor handlers
    sh_pressure = SensorHandler(SensorHandler.SENSOR_0)

    # render the main page
    return render(request, 'RENCI_Ventilator/index.html', {})


# gets the running instances
def data_req(request):
    # init the return status
    op_status = 200

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
                    op_status = 400
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
                op_status = 400

        elif req_type == 'event':
            # only each type of graph
            legal_params: list = ['Pressure', 'Respiration']

            # get any params if there are any
            param = request.GET.get('param')

            # we only expect either of the two types
            if param in legal_params:
                try:
                    global sh_pressure

                    # get the correct sensor
                    if param == 'Pressure':
                        # get the pressure data
                        sensor_value = sh_pressure.get_pressure()
                    else:
                        # get the respiration data
                        resp_data = sh_pressure.get_pressure_history()

                        # find the peaks
                        df = pd.DataFrame({'value': resp_data})

                        df['loc_min'] = df.value[(df.value.shift(1) > df.value) & (df.value.shift(-1) > df.value)]

                        df['if_A'] = np.where(df['loc_min'].isna(), False, True)

                        # return the count of peaks
                        sensor_value = ((len(resp_data)/240)*60)/len(df[df['if_A']==True])

                    # save the sensor data
                    ret_val = sensor_value

                # TODO: persist this data to the database?

                except Exception as e:
                    ret_val = e
                    op_status = 500
            else:
                ret_val = 'Invalid or missing event param.'
                op_status = 400

    # load the response and type, no caching here
    response = HttpResponse(json.dumps(ret_val), content_type='application/json', status=op_status)
    response['Cache-Control'] = 'no-cache'

    # return the resultant JSON to the caller
    return response
