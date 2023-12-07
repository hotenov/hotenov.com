'use strict';

const _ = require('lodash');
const chokidar = require('chokidar');
const upath = require('upath');
const renderAssets = require('./render-assets');
const renderScripts = require('./render-scripts');
const renderSCSS = require('./render-scss');

const watcher = chokidar.watch('src_front', {
    persistent: true,
});

let READY = false;

process.title = 'front-watch';
process.stdout.write('Loading');

watcher.on('add', filePath => _processFile(upath.normalize(filePath), 'add'));
watcher.on('change', filePath => _processFile(upath.normalize(filePath), 'change'));
watcher.on('ready', () => {
    READY = true;
    console.log('->READY TO ROLL!');
});

_handleSCSS();

function _processFile(filePath, watchEvent) {
    
    if (!READY) {
        process.stdout.write('.');
        return;
    }

    console.log(`### INFO: File event: ${watchEvent}: ${filePath}`);

    if (filePath.match(/\.scss$/)) {
        if (watchEvent === 'change') {
            return _handleSCSS(filePath, watchEvent);
        }
        return;
    }

    if (filePath.match(/src_front\/js\//)) {
        return renderScripts();
    }

    if (filePath.match(/src_front\/assets\//)) {
        return renderAssets();
    }

}

function _handleSCSS() {
    renderSCSS();
}
