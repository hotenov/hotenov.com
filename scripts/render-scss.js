'use strict';
const autoprefixer = require('autoprefixer')
const purgecss = require('@fullhuman/postcss-purgecss')
const minifier = require('postcss-minify')
const fs = require('fs');
// const packageJSON = require('../package.json');
const upath = require('upath');
const postcss = require('postcss')
const sass = require('sass');
const sh = require('shelljs');

const stylesPath = './src_front/scss/styles.scss';
const destPath = upath.resolve(upath.dirname(__filename), '../src/static/css/styles.min.css');

module.exports = function renderSCSS() {
    
    // const results = sass.renderSync({
    //     data: entryPoint,
    //     includePaths: [
    //         upath.resolve(upath.dirname(__filename), '../node_modules')
    //     ],
    // });
    const results = sass.compile(
        stylesPath,
        {
            loadPaths: [
                upath.resolve(upath.dirname(__filename), '../node_modules')
            ]
        }
    );

    const destPathDirname = upath.dirname(destPath);
    if (!sh.test('-e', destPathDirname)) {
        sh.mkdir('-p', destPathDirname);
    }


    // With purgeCSS + minification
    postcss([ 
        autoprefixer,
        purgecss({
            content: [
                './src/website/templates/website/**/*.html',
                './src/templates/**/*.html',
                './src_front/js/**/*.js',
                './src_front/scss/**/*.scss',
            ],
        }),
        minifier
    ]).process(results.css, {from: 'styles.css', to: 'styles.css'}).then(result => {
        result.warnings().forEach(warn => {
            console.warn(warn.toString())
        })
        fs.writeFileSync(destPath, result.css.toString());
    })
};

// const entryPoint = `/*!
// * Start Bootstrap - ${packageJSON.title} v${packageJSON.version} (${packageJSON.homepage})
// * Copyright 2013-${new Date().getFullYear()} ${packageJSON.author}
// * Licensed under ${packageJSON.license} (https://github.com/StartBootstrap/${packageJSON.name}/blob/master/LICENSE)
// */
// @import "${stylesPath}"
// `
