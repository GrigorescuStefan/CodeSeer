import { exec } from 'child_process';

export function checkDocker(): Promise<{ ok: boolean; message?: string }> {
    return new Promise((resolve) => {

        exec('docker info', (error, _stdout, stderr) => {

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