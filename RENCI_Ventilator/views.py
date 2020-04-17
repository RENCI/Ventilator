import json
import pandas as pandas
import numpy as numpy

from django.shortcuts import render
from django.http import HttpResponse
from RENCI_Ventilator.models import Configuration, Calibration
from RENCI_Ventilator.utils import get_settings
from RENCI_Ventilator.sensor import SensorHandler

# init a couple global params for the sensors
sh_pressure_1 = None
sh_pressure_2 = None


# main entry point
def index(request):
    # get the global variables for the sensor devices
    global sh_pressure_1
    global sh_pressure_2

    # start up the sensor handlers
    sh_pressure_1 = SensorHandler(SensorHandler.SENSOR_0)
    sh_pressure_2 = SensorHandler(SensorHandler.SENSOR_1)

    # render the main page
    return render(request, 'RENCI_Ventilator/index.html', {})


# gets the running instances
def data_req(request):
    # get the global variables for the sensor devices
    global sh_pressure_1
    global sh_pressure_2

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
            sh_pressure_0 = SensorHandler(0)

            sh0_test = sh_pressure_0.get_diagnostics()
            sh1_test = sh_pressure_1.get_diagnostics()
            sh2_test = sh_pressure_2.get_diagnostics()

            # convert the json to a string for posting back
            ret_val = f'{sh0_test}\n{sh1_test}\n{sh2_test}\n'

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
            legal_params: list = ['1', '2']

            # get any params if there are any
            param = request.GET.get('param')

            # we only expect either of the two types
            if param in legal_params:
                try:
                    # param 2 means get the pressure sensor data for the 2 sensors
                    if param == '2':
                        # get the pressure data
                        sensor_value = [sh_pressure_1.get_pressure(), sh_pressure_2.get_pressure()]
                    # param 1 gets the respiration data
                    else:
                        # get the sensor pressure history data
                        resp_data = sh_pressure_1.get_pressure_history()

                        # if there no variance in the data it must be a flat line
                        if numpy.var(resp_data) > 1.0:
                            # get the last set of pressure data points (up to a minute)
                            df = pandas.DataFrame({'value': resp_data})

                            # find all the local minimums over the range of pressure data points
                            df['loc_min'] = df.value[(df.value.shift(1) < df.value) & (df.value.shift(-1) < df.value)]

                            # get all points that indicate a minimum was found
                            df['if_min'] = numpy.where(df['loc_min'].isna(), False, True)

                            # get the count of mimimums (breating rate)
                            sensor_value = len(df[df['if_min'] == True])

                            # if there were minima found
                            if sensor_value <= 0:
                                sensor_value = 0
                            # max out at 20
                            elif sensor_value > 20:
                                sensor_value = 20
                        # must be a flat line
                        else:
                            sensor_value = 0

                    # save the sensor data
                    ret_val = sensor_value

                except Exception as e:
                    ret_val = f'Exception: {e}'
                    op_status = 500
            else:
                ret_val = 'Invalid or missing event param.'
                op_status = 400

    # load the response and type, no caching here
    response = HttpResponse(json.dumps(ret_val), content_type='application/json', status=op_status)
    response['Cache-Control'] = 'no-cache'

    # return the resultant JSON to the caller
    return response
