// RectifiedDrive PID graph
var drivesetpoint = new TimeSeries();
var driveactual = new TimeSeries();
var drive_smoothie = new SmoothieChart({
    grid: {
        strokeStyle: 'rgb(255, 255, 255)', fillStyle: 'rgb(0, 0, 0)',
        lineWidth: 1, millisPerLine: 1000, verticalSections: 10,
    },
    labels: {fillStyle: 'rgb(255, 255, 0)'},
    maxValue: 100, minValue: -100
});
drive_smoothie.addTimeSeries(drivesetpoint,
    {strokeStyle: 'rgb(100, 255, 100)', lineWidth: 2});
drive_smoothie.addTimeSeries(driveactual,
    {strokeStyle: 'rgb(255, 100, 100)', lineWidth: 2});
drive_smoothie.streamTo(document.getElementById("drivegraph"));

// drive-to-rod PID graph
var rodsetpoint = new TimeSeries();
var rodactual = new TimeSeries();
var rod_smoothie = new SmoothieChart({
    grid: {
        strokeStyle: 'rgb(255, 255, 255)', fillStyle: 'rgb(0, 0, 0)',
        lineWidth: 1, millisPerLine: 1000, verticalSections: 10,
    },
    labels: {fillStyle: 'rgb(255, 255, 0)'},
    maxValue: 1, minValue: 0
});
rod_smoothie.addTimeSeries(rodsetpoint,
    {strokeStyle: 'rgb(100, 255, 100)', lineWidth: 2});
rod_smoothie.addTimeSeries(rodactual,
    {strokeStyle: 'rgb(255, 100, 100)', lineWidth: 2});
rod_smoothie.streamTo(document.getElementById("rodgraph"));

// Define UI elements
var ui = {
    timer: document.getElementById('timer'),
    robotState: document.getElementById('robot-state'),
    gyro: {
        container: document.getElementById('gyro'),
        val: 0,
        offset: 0,
        visualVal: 0,
        arm: document.getElementById('gyro-arm'),
        number: document.getElementById('gyro-number')
    },
    navx: {
        connected: document.getElementById('navx-connected'),
        calibrating: document.getElementById('navx-calibrating'),
        //angle: document.getElementById('navx-angle'),
        yaw: document.getElementById('navx-yaw')
    },
    sonar: {
        front: document.getElementById('sonar-front'),
        back: document.getElementById('sonar-back')
    },
    robotDiagram: {
        arm: document.getElementById('robot-arm')
    },
    forwardCommand: {
        button: document.getElementById('forward-button')
    },
    turnCommand: {
        button: document.getElementById('turn-right-button')
    },
    getNT: {
        button: document.getElementById('get-nt-button')
    },
    tuning: {
        list: document.getElementById('tuning'),
        button: document.getElementById('tuning-button'),
        name: document.getElementById('name'),
        value: document.getElementById('value'),
        set: document.getElementById('set'),
        get: document.getElementById('get')
    },
    autoSelect: document.getElementById('auto-select'),
    gears: {
        left: document.getElementById('gear1'),
        right: document.getElementById('gear2')
    },
    outputs: {
        left: document.getElementById('left-output'),
        right: document.getElementById('right-output')
    },
    pneumatic: document.getElementById('pneumatic'),
    camera: {
        minh: document.getElementById('minh'),
        mins: document.getElementById('mins'),
        minv: document.getElementById('minv'),
        maxh: document.getElementById('maxh'),
        maxs: document.getElementById('maxs'),
        maxv: document.getElementById('maxv')
    },
    rod: {
        kp: document.getElementById('rodp'),
        ki: document.getElementById('rodi'),
        kd: document.getElementById('rodd'),
        kf: document.getElementById('rodf'),
        ktolerance: document.getElementById('rodtolerance')
    },
    drive: {
        kp: document.getElementById('drivep'),
        ki: document.getElementById('drivei'),
        kd: document.getElementById('drived'),
        kf: document.getElementById('drivef'),
        ktolerance: document.getElementById('drivetolerance')
    }
};

// Sets function to be called on NetworkTables connect. Commented out because it's usually not necessary.
// NetworkTables.addWsConnectionListener(onNetworkTablesConnection, true);
// Sets function to be called when robot dis/connects
NetworkTables.addRobotConnectionListener(onRobotConnection, true);
// Sets function to be called when any NetworkTables key/value changes
NetworkTables.addGlobalListener(onValueChanged, true);


function onRobotConnection(connected) {
    var state = connected ? 'Robot connected!' : 'Robot disconnected.';
    console.log(state);
    ui.robotState.innerHTML = state;
}

function onValueChanged(key, value, isNew) {
    // Sometimes, NetworkTables will pass booleans as strings. This corrects for that.
    if (value == 'true') {
        value = true;
    } else if (value == 'false') {
        value = false;
    }

    // This switch statement chooses which UI element to update when a NetworkTables variable changes.
    switch (key) {
        case '/SmartDashboard/navX/isConnected':
            ui.navx.connected.innerHTML = value;
            break;
        case '/SmartDashboard/navX/isCalibrating':
            ui.navx.calibrating.innerHTML = value;
            break;
        case '/SmartDashboard/navX/yaw': // Gyro rotation
            // update gyro diagram
            ui.gyro.val = value;
            ui.gyro.visualVal = Math.floor(ui.gyro.val - ui.gyro.offset);
            if (ui.gyro.visualVal < 0) { // Corrects for negative values
                ui.gyro.visualVal += 360;
            }
            ui.gyro.arm.style.transform = ('rotate(' + ui.gyro.visualVal + 'deg)');
            ui.gyro.number.innerHTML = ui.gyro.visualVal + 'º';

            // update yaw value
            ui.navx.yaw.innerHTML = value;
            break;
        case '/SmartDashboard/sonar/front':
            ui.sonar.front.innerHTML = Math.round(value * 100) / 100.0;
            break;
        case '/SmartDashboard/sonar/back':
            ui.sonar.back.innerHTML = Math.round(value * 100) / 100.0;
            break;
        case '/SmartDashboard/forwardCommand':
            // This button moves the robot forward for 1 second.
            if (value) { // If function is active:
                // Add active class to button.
                ui.forwardCommand.button.className = 'active';
                //ui.forwardCommand.readout.innerHTML = "Moving forward...";
            } else { // Otherwise
                // Take it off
                ui.fowardCommand.button.className = '';
                //ui.forwardCommand.readout.innerHTML = "Forward command not being sent.";
            }
            break;
        case '/SmartDashboard/turnCommand':
            // This button turns the robot right 90 degrees.
            if (value) {
                ui.forwardCommand.button.classNmae = 'active';
            } else {
                ui.forwardCommand.button.className = '';
            }
            break;
        case '/SmartDashboard/timeRunning':
            // When this NetworkTables variable is true, the timer will start.
            // You shouldn't need to touch this code, but it's documented anyway in case you do.
            var s = 135;
            if (value) {
                // Make sure timer is reset to black when it starts
                ui.timer.style.color = 'white';
                // Function below adjusts time left every second
                var countdown = setInterval(function () {
                    s--; // Subtract one second
                    // Minutes (m) is equal to the total seconds divided by sixty with the decimal removed.
                    var m = Math.floor(s / 60);
                    // Create seconds number that will actually be displayed after minutes are subtracted
                    var visualS = (s % 60);

                    // Add leading zero if seconds is one digit long, for proper time formatting.
                    visualS = visualS < 10 ? '0' + visualS : visualS;

                    if (s < 0) {
                        // Stop countdown when timer reaches zero
                        clearTimeout(countdown);
                        return;
                    } else if (s <= 15) {
                        // Flash timer if less than 15 seconds left
                        ui.timer.style.color = (s % 2 === 0) ? '#FF3030' : 'transparent';
                    } else if (s <= 30) {
                        // Solid red timer when less than 30 seconds left.
                        ui.timer.style.color = '#FF3030';
                    }
                    ui.timer.innerHTML = m + ':' + visualS;
                }, 1000);
            } else {
                s = 135;
            }
            NetworkTables.setValue(key, false);
            break;
        case '/SmartDashboard/leftOutput':
            ui.outputs.left.innerHTML = Math.round(-value * 100);
            var period = 2.5 - Math.abs((parseInt(ui.outputs.left.innerHTML) + parseInt(ui.outputs.right.innerHTML)) / 100.0);
            ui.gears.left.style.animation = "barrelRoll " + period + "s infinite linear"
            ui.gears.right.style.animation = "invertBarrelRoll " + period + "s infinite linear"
            break;
        case '/SmartDashboard/rightOutput':
            ui.outputs.right.innerHTML = Math.round(value * 100);
            var period = 2.5 - Math.abs((parseInt(ui.outputs.left.innerHTML) + parseInt(ui.outputs.right.innerHTML)) / 100.0);
            ui.gears.left.style.animation = "barrelRoll " + period + "s infinite linear"
            ui.gears.right.style.animation = "invertBarrelRoll " + period + "s infinite linear"
            break;
        case '/SmartDashboard/pneumatic':
            if (value)
                ui.pneumatic.innerHTML = "Out";
            else
                ui.pneumatic.innerHTML = "In";
            break;
        case '/SmartDashboard/autonomous/options': // Load list of prewritten autonomous modes
            // Clear previous list
            while (ui.autoSelect.firstChild) {
                ui.autoSelect.removeChild(ui.autoSelect.firstChild);
            }
            // Make an option for each autonomous mode and put it in the selector
            for (i = 0; i < value.length; i++) {
                var option = document.createElement('option');
                option.innerHTML = value[i];
                ui.autoSelect.appendChild(option);
            }
            // Set value to the already-selected mode. If there is none, nothing will happen.
            ui.autoSelect.value = NetworkTables.getValue('/SmartDashboard/currentlySelectedMode');
            break;
        case '/SmartDashboard/autonomous/selected':
            ui.autoSelect.value = value;
            break;

        // for tuning RectifiedDrive
        case '/SmartDashboard/drive/setpoint':
            drivesetpoint.append(new Date().getTime(), value);
            break;
        case '/SmartDashboard/drive/actual':
            driveactual.append(new Date().getTime(), value);
            break;

        // for tuning drive-to-rod
        case '/SmartDashboard/rod/actual':
            rodsetpoint.append(new Date().getTime(), 0.5);
            rodactual.append(new Date().getTime(), value);
            break;
    }

    // The following code manages tuning section of the interface.
    // This section displays a list of all NetworkTables variables (that start with /SmartDashboard/) and allows you to directly manipulate them.
    var propName = key.substring(16, key.length);
    // Check if value is new and doesn't have a spot on the list yet
    if (isNew && !document.getElementsByName(propName)[0]) {
        // Make sure name starts with /SmartDashboard/. Properties that don't are technical and don't need to be shown on the list.
        if (key.substring(0, 16) === '/SmartDashboard/') {
            // Make a new div for this value
            var div = document.createElement('div'); // Make div
            ui.tuning.list.appendChild(div); // Add the div to the page

            var p = document.createElement('p'); // Make a <p> to display the name of the property
            p.innerHTML = propName; // Make content of <p> have the name of the NetworkTables value
            div.appendChild(p); // Put <p> in div

            var input = document.createElement('input'); // Create input
            input.name = propName; // Make its name property be the name of the NetworkTables value
            input.value = value; // Set
            // The following statement figures out which data type the variable is.
            // If it's a boolean, it will make the input be a checkbox. If it's a number,
            // it will make it a number chooser with up and down arrows in the box. Otherwise, it will make it a textbox.
            if (value === true || value === false) { // Is it a boolean value?
                input.type = 'checkbox';
                input.checked = value; // value property doesn't work on checkboxes, we'll need to use the checked property instead
            } else if (!isNaN(value)) { // Is the value not not a number? Great!
                input.type = 'number';
            } else { // Just use a text if there's no better manipulation method
                input.type = 'text';
            }
            // Create listener for value of input being modified
            input.onchange = function () {
                switch (input.type) { // Figure out how to pass data based on data type
                    case 'checkbox':
                        // For booleans, send bool of whether or not checkbox is checked
                        NetworkTables.setValue(key, input.checked);
                        break;
                    case 'number':
                        // For number values, send value of input as an int.
                        NetworkTables.setValue(key, parseInt(input.value));
                        break;
                    case 'text':
                        // For normal text values, just send the value.
                        NetworkTables.setValue(key, input.value);
                        break;
                }
            };
            // Put the input into the div.
            div.appendChild(input);
        }
    } else { // If the value is not new
        // Find already-existing input for changing this variable
        var oldInput = document.getElementsByName(propName)[0];
        if (oldInput) { // If there is one (there should be, unless something is wrong)
            if (oldInput.type === 'checkbox') { // Figure out what data type it is and update it in the list
                oldInput.checked = value;
            } else {
                oldInput.value = value;
            }
        } else {
            console.log('Error: Non-new variable ' + key + ' not present in tuning list!');
        }
    }
}

// The rest of the doc is listeners for UI elements being clicked on
ui.forwardCommand.button.onclick = function () {
    NetworkTables.setValue('/SmartDashboard/forwardCommand', true);
};

ui.turnCommand.button.onclick = function () {
    NetworkTables.setValue('/SmartDashboard/turnCommand', true);
};

ui.camera.minh.onchange = function () {
    NetworkTables.setValue('/SmartDashboard/camera/minh', parseFloat(ui.camera.minh.value));
};
ui.camera.mins.onchange = function () {
    NetworkTables.setValue('/SmartDashboard/camera/mins', parseFloat(ui.camera.mins.value));
};
ui.camera.minv.onchange = function () {
    NetworkTables.setValue('/SmartDashboard/camera/minv', parseFloat(ui.camera.minv.value));
};
ui.camera.maxh.onchange = function () {
    NetworkTables.setValue('/SmartDashboard/camera/maxh', parseFloat(ui.camera.maxh.value));
};
ui.camera.maxs.onchange = function () {
    NetworkTables.setValue('/SmartDashboard/camera/maxs', parseFloat(ui.camera.maxs.value));
};
ui.camera.maxv.onchange = function () {
    NetworkTables.setValue('/SmartDashboard/camera/maxv', parseFloat(ui.camera.maxv.value));
};

ui.rod.kp.onchange = function () {
    NetworkTables.setValue('/SmartDashboard/rod/kp', parseFloat(ui.rod.kp.value));
};
ui.rod.ki.onchange = function () {
    NetworkTables.setValue('/SmartDashboard/rod/ki', parseFloat(ui.rod.ki.value));
};
ui.rod.kd.onchange = function () {
    NetworkTables.setValue('/SmartDashboard/rod/kd', parseFloat(ui.rod.kd.value));
};
ui.rod.kf.onchange = function () {
    NetworkTables.setValue('/SmartDashboard/rod/kf', parseFloat(ui.rod.kf.value));
};
ui.rod.ktolerance.onchange = function () {
    NetworkTables.setValue('/SmartDashboard/rod/ktolerance', parseFloat(ui.rod.ktolerance.value));
};

ui.drive.kp.onchange = function () {
    NetworkTables.setValue('/SmartDashboard/drive/kp', parseFloat(ui.drive.kp.value));
};
ui.drive.ki.onchange = function () {
    NetworkTables.setValue('/SmartDashboard/drive/ki', parseFloat(ui.drive.ki.value));
};
ui.drive.kd.onchange = function () {
    NetworkTables.setValue('/SmartDashboard/drive/kd', parseFloat(ui.drive.kd.value));
};
ui.drive.kf.onchange = function () {
    NetworkTables.setValue('/SmartDashboard/drive/kf', parseFloat(ui.drive.kf.value));
};
ui.drive.ktolerance.onchange = function () {
    NetworkTables.setValue('/SmartDashboard/drive/ktolerance', parseFloat(ui.drive.ktolerance.value));
};

// Reset gyro value to 0 on click
ui.gyro.container.onclick = function () {
    // Store previous gyro val, will now be subtracted from val for callibration
    ui.gyro.offset = ui.gyro.val;
    // Trigger the gyro to recalculate value.
    onValueChanged('/SmartDashboard/drive/navX/yaw', ui.gyro.val);
};

// Open tuning section when button is clicked
ui.tuning.button.onclick = function () {
    if (ui.tuning.list.style.display === 'none') {
        ui.tuning.list.style.display = 'block';
    } else {
        ui.tuning.list.style.display = 'none';
    }
};

// Manages get and set buttons at the top of the tuning pane
ui.tuning.set.onclick = function () {
    // Make sure the inputs have content, if they do update the NT value
    if (ui.tuning.name.value && ui.tuning.value.value) {
        NetworkTables.setValue('/SmartDashboard/' + ui.tuning.name.value, ui.tuning.value.value);
    }
};
ui.tuning.get.onclick = function () {
    ui.tuning.value.value = NetworkTables.getValue(ui.tuning.name.value);
};

// Update NetworkTables when autonomous selector is changed
ui.autoSelect.onchange = function () {
    NetworkTables.setValue('/SmartDashboard/autonomous/selected', this.value);
};

ui.getNT.button.onclick = function () {
    // get NetworkTables values
    ui.camera.minh.value = NetworkTables.getValue('/SmartDashboard/camera/minh');
    console.log(NetworkTables.getValue('/SmartDashboard/camera/minh'));
    ui.camera.mins.value = NetworkTables.getValue('/SmartDashboard/camera/mins');
    ui.camera.minv.value = NetworkTables.getValue('/SmartDashboard/camera/minv');
    ui.camera.maxh.value = NetworkTables.getValue('/SmartDashboard/camera/maxh');
    ui.camera.maxs.value = NetworkTables.getValue('/SmartDashboard/camera/maxs');
    ui.camera.maxv.value = NetworkTables.getValue('/SmartDashboard/camera/maxv');

    ui.rod.kp.value = NetworkTables.getValue('/SmartDashboard/rod/kp');
    console.log(NetworkTables.getValue('/SmartDashboard/rod/kp'));
    ui.rod.ki.value = NetworkTables.getValue('/SmartDashboard/rod/ki');
    ui.rod.kd.value = NetworkTables.getValue('/SmartDashboard/rod/kd');
    ui.rod.kf.value = NetworkTables.getValue('/SmartDashboard/rod/kf');
    ui.rod.ktolerance.value = NetworkTables.getValue('/SmartDashboard/rod/ktolerance');

    ui.drive.kp.value = NetworkTables.getValue('/SmartDashboard/drive/kp');
    ui.drive.ki.value = NetworkTables.getValue('/SmartDashboard/drive/ki');
    ui.drive.kd.value = NetworkTables.getValue('/SmartDashboard/drive/kd');
    ui.drive.kf.value = NetworkTables.getValue('/SmartDashboard/drive/kf');
    ui.drive.ktolerance.value = NetworkTables.getValue('/SmartDashboard/drive/ktolerance');
};