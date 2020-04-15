/**
 * utility functions used in the configuration, rendering and data gathering
 */

// sends a request for diagnostics
function sendDiagRequest()
{
    d3.json('http://localhost:8000/dataReq?type=diags', function(error, diagData)
    {
        // get a control handle
        let control = $('#diagnosticResults');

        // start the tests
        let msg = 'Diagnostics initiated, Please wait...';

        // set the message
        control.val(msg);

        // did we get some valid data
        if(error == null && diagData.length > 0)
        {
            // loop through the data
            diagData.forEach(
                // for each item returned
                function(item) {
                    msg = msg + '\n' + item.fields.ts + ' - test:' + item.fields.test_name + ', description:' + item.fields.description + ', result:' + item.fields.result;
                }
            );

            // send out the final message
            control.val(msg);
        }
        // send out an error message
        else
            control.val(msg + '\n Error performing diagnostics.');
    });
}


// saves the slider control settings
function saveSetting(table)
{
    // build up the query string
    let qs = '&table=' + table + '&param=';

    // init the target control
    let msgTarget = null;

    // put in the specific params for this area
    if (table === 'config')
    {
        qs = qs + 'pressure=' + $('#pressureRange').val() + '~' + 'respiration=' + $('#respirationRange').val() + '~' + 'demomode=' + ($('#demomode').is(":checked") + 0);
        msgTarget = $('#saveConfigMsg');
    }
    else
    {
        qs = qs + 'sensor1=' + $('#sensor1Range').val() + '~' + 'sensor2=' + $('#sensor2Range').val();
        msgTarget = $('#saveCalibMsg');
    }

    d3.json('http://localhost:8000/dataReq?type=update' + qs, function(error, result)
    {
        if(error != null) {
            msgTarget.text('Error saving.');
            msgTarget.addClass("error");
        }
        else {
            msgTarget.text(result);
            msgTarget.addClass("pass");
        }

        // show/hide the message
        msgTarget.show(500);
        msgTarget.hide(3000);
   });
}

// loads the UI with settings from the database
function load_settings()
{
    // load up the various configuration items
    d3.json('http://localhost:8000/dataReq?type=config', function(error, configData)
    {
        // The pressure slider handler
        const pressureValueSpan = $('.pressureValueSpan');
        const p_value = $('#pressureRange');
        pressureValueSpan.html(p_value.val());
        p_value.on('input change', () => {pressureValueSpan.html(p_value.val());});

        // set the initial pressure value
        p_value.val(configData.pressure.value);
        pressureValueSpan.html(p_value.val());

        // the respiration slider handler
        const respirationValueSpan = $('.respirationValueSpan');
        const r_value = $('#respirationRange');
        respirationValueSpan.html(r_value.val());
        r_value.on('input change', () => {
            respirationValueSpan.html(r_value.val());
        });

        // set the initial respiration value
        r_value.val(configData.respiration.value);
        respirationValueSpan.html(r_value.val());

        // set the demo mode flag and present the message
        $("#demomode").prop('checked', configData.demomode.value);
        demoMessage();
    });

    // load up the various configuration items
    d3.json('http://localhost:8000/dataReq?type=calib', function(error, calibData)
    {
        // the sensor 1 slider handler
        const sensor1ValueSpan = $('.sensor1ValueSpan');
        const s1_value = $('#sensor1Range');
        sensor1ValueSpan.html(s1_value.val());
        s1_value.on('input change', () => {
            sensor1ValueSpan.html(s1_value.val());
        });

        // set the initial sensor 1 value
        s1_value.val(calibData.sensor1.value);
        sensor1ValueSpan.html(s1_value.val());

        // the sensor 2 slider handler
        const sensor2ValueSpan = $('.sensor2ValueSpan');
        const s2_value = $('#sensor2Range');
        sensor2ValueSpan.html(s2_value.val());
        s2_value.on('input change', () => {
            sensor2ValueSpan.html(s2_value.val());

        });

        // set the initial sensor 1 value
        s2_value.val(calibData.sensor2.value);
        sensor2ValueSpan.html(s2_value.val());
    });
}

// global flag for pausing the wave monitor
let monitorPause = 0;

// toggles the monitor data retrieval
function togglePause()
{
    let theBtn = $('#pause');

    // if we are running
    if(monitorPause === 0)
    {
        // set flag to pause
        monitorPause = 1;

        // update the view
        theBtn.removeClass("btn-success");
        theBtn.addClass("btn-danger");
        theBtn.html('Paused');
    }
    else
    {
        // set flag to run
        monitorPause = 0;

        // update the view
        theBtn.removeClass("btn-danger");
        theBtn.addClass("btn-success");
        theBtn.html('Pause');
    }
}

// displays if we are in demo mode
function demoMessage()
{
    let chk_val = $('#demomode').is(":checked");

    if(chk_val === true)
    {
        $('#demoModeMsg').html('DEMO MODE')
    }
    else
    {
        $('#demoModeMsg').html('')
    }
}