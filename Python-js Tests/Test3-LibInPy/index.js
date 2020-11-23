const path = require('path')
const { spawn } = require('child_process')
/**
   * Run python myscript, pass in `-u` to not buffer console output
   * @return {ChildProcess}
*/

function runSetUpScript() {
    return spawn('py', [
        path.join(__dirname, 'installLibs.py'),
    ]);
}

// lib in python folder
function runScript() {
    return spawn('py', [
        path.join(__dirname, 'WebscraperUnitTests.py'),
    ]);
}

const setupProcess = runSetUpScript()
const subprocess = runScript()


setupProcess.stdout.on('data', (data) => {
    console.log(`Done installing python packages:${data}`);

});
setupProcess.stderr.on('data', (data) => {
    console.log(`error:${data}`);
});

// print output of script
subprocess.stdout.on('data', (data) => {
    console.log(`data:${data}`);
});
subprocess.stderr.on('data', (data) => {
    console.log(`error:${data}`);
});
subprocess.stderr.on('close', () => {
    console.log("Closed");
});