import json
import random

from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import QuerySet
from django.core import serializers
from RENCI_Ventilator.models import Configuration, Calibration, Diagnostic, Pressure, Respiration
from RENCI_Ventilator.diags import run_diagnostic


# Create your views here.
# main entry point
def index(request):
    # render the main page
    return render(request, 'RENCI_Ventilator/index.html', {})


# gets the running instances
def data_req(request):
    # define legal request types
    legal_req_types: list = ['event', 'config', 'calib', 'diags', 'update']

    # get the request type
    req_type: str = request.GET.get('type')

    # init the return data
    ret_val: str = ''

    # only legal commands can pass
    if req_type in legal_req_types:
        # create a list for the data
        settings: dict = {}

        # config details do not need a parameter, all are returned
        if req_type == 'config':
            # get the data from the database
            config_items: QuerySet = Configuration.objects.all()

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
            ret_val = json.dumps(settings)

        # config details need a parameter
        elif req_type == 'diags':
            # start the diagnostics, this will insert records into the database
            group_number = run_diagnostic()

            # get the data from the database
            diag_items: QuerySet = Diagnostic.objects.filter(grouping=group_number)

            # convert the data to json format
            ret_val = serializers.serialize('json', diag_items)

        # update a configuration or calibration entry
        elif req_type == 'update':
            legal_setting_types: list = ['config', 'calib']

            # get the setting type we will update
            setting = request.GET.get('setting')

            # was this a legitimate request
            if req_type in legal_setting_types:
                # get the params
                param = request.GET.get('param')

                # its a failure if there was no param passed for this type
                if param is None:
                    ret_val = 'Invalid or missing parameter(s).'
                else:
                    # init the table object
                    tbl_obj = None

                    # check the table type
                    if setting == 'config':
                        tbl_obj = Configuration
                    else:
                        tbl_obj = Calibration

                    # split the settings


            else:
                ret_val = 'Invalid setting request.'

        elif req_type == 'calib':
            # get the data from the database
            calib_items: QuerySet = Calibration.objects.all()

            # convert each record into a list of dicts
            for item in calib_items:
                # make the conversion
                settings.update({item.param_name: {
                        'id': item.id,
                        'param_name': item.param_name,
                        'description': item.description,
                        'value': item.value,
                        'ts': str(item.ts)
                    }})

            # convert the data to json format
            ret_val = json.dumps(settings)

        elif req_type == 'event':
            # get any params if there are any
            param = request.GET.get('param')

            # its a failure if there was no param passed for this type
            if param is None:
                ret_val = 'Invalid or missing parameter.'
            else:
                # init the table object
                tbl_obj = None

                # testing purposes only
                rnd = 0

                # get the correct table
                if param == 'Pressure':
                    tbl_obj = Pressure
                    rnd = random.randrange(40, 50, 1)
                elif param == 'Respiration':
                    tbl_obj = Respiration
                    rnd = random.randrange(10, 15, 1)

                # did we get a table object
                if tbl_obj is not None:
                    ret_val = json.dumps(rnd)
                else:
                    ret_val = 'Invalid or missing parameter.'
    else:
        ret_val = 'Invalid data request.'

    # load the response and type, no caching here
    response = HttpResponse(ret_val, content_type='application/json')
    response['Cache-Control'] = 'no-cache'

    # return the resultant JSON to the caller
    return response
