import json
import random

from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import QuerySet
from RENCI_Ventilator.models import Configuration, Calibration, Diagnostic, Pressure, Respiration


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
            # get any params if there are any
            param = request.GET.get('param')

            # its a failure if there was no param passed for this type
            if param is None:
                ret_val = 'Invalid or missing parameter.'
            else:
                # create the SQL. raw SQL calls using the django db model need an ID
                the_sql = ""

                # get the data, account for single quotes
                ret_val = str(Diagnostic.objects.raw(the_sql)[0].data)

        # update a configuration or calibration entry
        elif req_type == 'update':
            # get any params if there are any
            param = request.GET.get('param')

            # its a failure if there was no param passed for this type
            if param is None:
                ret_val = 'Invalid or missing parameter.'
            else:
                # init the table object
                tbl_obj = None

                # check the parameter type

                # create the SQL. raw SQL calls using the django db model need an ID
                the_sql = ""

                # get the data, account for single quotes
                ret_val = str(tbl_obj.objects.raw(the_sql)[0].data)

        elif req_type == 'calib':
            # get any params if there are any
            param = request.GET.get('param')

            # its a failure if there was no param passed for this type
            if param is None:
                ret_val = 'Invalid or missing parameter.'
            else:
                # create the SQL. raw SQL calls using the django db model need an ID
                the_sql = ""

                # get the data, account for single quotes
                ret_val = str(Calibration.objects.raw(the_sql)[0].data)

        elif req_type == 'event':
            # get any params if there are any
            param = request.GET.get('param')

            # its a failure if there was no param passed for this type
            if param is None:
                ret_val = 'Invalid or missing parameter.'
            else:
                # init the table object
                tbl_obj = None

                # get the correct table
                if param == 'Pressure':
                    tbl_obj = Pressure
                elif param == 'Respiration':
                    tbl_obj = Respiration

                # did we get a table object
                if tbl_obj is not None:
                    ret_val = json.dumps(random.randrange(0, 20, 1))
                else:
                    ret_val = 'Invalid or missing parameter.'
    else:
        ret_val = 'Invalid data request.'

    # load the response and type, no caching here
    response = HttpResponse(ret_val, content_type='application/json')
    response['Cache-Control'] = 'no-cache'

    # return the resultant JSON to the caller
    return response
