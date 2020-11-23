const path = require('path')
const { spawn } = require('child_process')
/**
   * Run python myscript, pass in `-u` to not buffer console output
   * @return {ChildProcess}
*/
function runScript() {
    return spawn('py', [
        path.join(__dirname, 'index.py'),
    ]);
}
const subprocess = runScript()
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