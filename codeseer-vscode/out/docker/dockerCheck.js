"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.checkDocker = checkDocker;
const child_process_1 = require("child_process");
function checkDocker() {
    return new Promise((resolve) => {
        (0, child_process_1.exec)('docker info', (error, _stdout, stderr) => {
            if (error) {
                const msg = (stderr || error.message).toLowerCase();
                if (msg.includes('paused')) {
                    return resolve({
                        ok: false,
                        message: 'Docker Desktop is paused. Please unpause it.'
                    });
                }
                if (msg.includes('pipe') || msg.includes('cannot find')) {
                    return resolve({
                        ok: false,
                        message: 'Docker is not running. Please start Docker Desktop.'
                    });
                }
                return resolve({
                    ok: false,
                    message: 'Docker is not available.'
                });
            }
            resolve({ ok: true });
        });
    });
}
//# sourceMappingURL=dockerCheck.js.map