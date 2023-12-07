const concurrently = require('concurrently');
const upath = require('upath');

const browserSyncPath = upath.resolve(upath.dirname(__filename), '../node_modules/.bin/browser-sync');

concurrently([
    { command: 'node --inspect scripts/bs-watch.js', name: 'BS_FILES_WATCH_DEBUG', prefixColor: 'bgBlue.bold' },
    { 
        command: `"${browserSyncPath}" "http://127.0.0.1:8882/" --files "src_front/**/*.*, src/website/static/css/*.css, src/website/**/*.py, src/templates/**/*.html, src/website/templates/**/*.html" -w --reload-delay 2000 --reload-debounce 2000 --no-online`,
        name: 'BS_PROXY_TO_DJANGO', 
        prefixColor: 'greenBright',
    }
], {
    prefix: 'name',
    killOthers: ['failure', 'success'],
}).then(success, failure);

function success() {
    console.log('Success');    
}

function failure() {
    console.log('Failure');
}