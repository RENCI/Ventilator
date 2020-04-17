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
            // load up what was returned from the sensors
            msg = msg + '\n' + diagData;
        }
        // send out an error message
        else
            msg = msg + '\nError performing diagnostics.';

        // send out the final message
        control.val(msg + '\nDiagnostics complete.');
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
        qs = qs + 'pcirc=' + $('#pCircRange').val() + '~' + 'px=' + $('#pxRange').val() + '~' + 'respiration=' + $('#respirationRange').val() + '~' + 'demomode=' + ($('#demomode').is(":checked") + 0);
        msgTarget = $('#saveConfigMsg');

        // show/hide the demo message
        demoMessage();
    }
    else
    {
        qs = qs + 'sensor0=' + $('#sensor0Range').val();
        msgTarget = $('#saveCalibMsg');
    }

    d3.json('http://localhost:8000/dataReq?type=update' + qs, function(error, result)
    {
        // show an error is we got one
        if(error != null)
        {
            msgTarget.text('Error saving.');
            msgTarget.addClass("error");
        }
        else
        {
            msgTarget.text(result);
            msgTarget.addClass("pass");
        }

        // show/hide the message
        msgTarget.show(500);
        msgTarget.hide(2000);
   });
}

// loads the UI with settings from the database
function load_settings()
{
    // load up the various configuration items
    d3.json('http://localhost:8000/dataReq?type=config', function(error, configData)
    {
        // get the pressure config setting and split it into max/min values
        val = configData.pcirc.value
        r = val.split(',')

        // load configuration sliders
        $("#pCircRange").slider({min: -5, max: 50, value: [Number(r[0]), Number(r[1])]});
        $("#pCircRangeVals").text('(' + $("#pCircRange").slider('getValue') + ')');
        $("#pCircRange").on("slide", function(slideEvt) { $("#pCircRangeVals").text('(' + slideEvt.value + ')'); });

        // get the pressure config setting and split it into max/min values
        val = configData.px.value
        r = val.split(',')

        // load configuration sliders
        $("#pxRange").slider({min: -5, max: 50, value: [Number(r[0]), Number(r[1])]});
        $("#pxRangeVals").text('(' + $("#pxRange").slider('getValue') + ')');
        $("#pxRange").on("slide", function(slideEvt) { $("#pxRangeVals").text('(' + slideEvt.value + ')'); });

        // get the pressure config setting and split it into max/min values
        val = configData.respiration.value
        r = val.split(',')

        $("#respirationRange").slider({min: 0, max: 20, value: [Number(r[0]), Number(r[1])]});
        $("#respirationRangeVals").text('(' + $("#respirationRange").slider('getValue') + ')');
        $("#respirationRange").on("slide", function(slideEvt) { $("#respirationRangeVals").text('(' + slideEvt.value + ')'); });

        // set the demo mode flag and present the message
        $("#demomode").prop('checked', Number(configData.demomode.value));

        // update the demo message on the ui
        demoMessage();
    });

    // load up the various configuration items
    d3.json('http://localhost:8000/dataReq?type=calib', function(error, calibData)
    {
        // the sensor 0 slider handler
        const sensor0ValueSpan = $('.sensor0ValueSpan');
        const s0_value = $('#sensor0Range');
        sensor0ValueSpan.html(s0_value.val());
        s0_value.on('input change', () => {
            sensor0ValueSpan.html(s0_value.val());
        });

        // set the initial sensor 1 value
        s0_value.val(calibData.sensor0.value);
        sensor0ValueSpan.html(s0_value.val());
    });
}

// global flag for pausing the wave monitor
let monitorPause = 0;

// toggles the monitor data retrieval
function togglePause()
{
    // get a handle to the pause button
    let theBtn = $('#pause');

    // if we are running
    if(monitorPause === 0)
    {
        // set flag to pause
        monitorPause = 1;

        // update the view of the button
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