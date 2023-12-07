'use strict';
const fsPromises = require('fs').promises;
const upath = require('upath');
const sh = require('shelljs');
const postcss = require('postcss')
const purgecss = require('@fullhuman/postcss-purgecss')
const minifier = require('postcss-minify')


/**
 * Compile fonts CSS.
 * CSS concatenation (Fontawesome + Google fonts) -> purging -> minification.
 */
module.exports.compileFontsCSS = function() {
    let cssFiles = [
        // "src_front/assets/webfonts/all-fontawesome-free-6.2.1-web.css",  // From 2023-10-26 without version
        "src_front/assets/webfonts/all-fontawesome-free-web.css",
        "src_front/assets/webfonts/google-fonts.css",
    ];
    const outputFile = "src/static/assets/webfonts/all-fonts-opt.css";

    // Set up PostCSS Processor instance
    const processor = postcss([
        purgecss({
            content: [
                // global Django HTML templates
                "src/templates/**/*.html",
                // apps Django HTML templates
                "src/website/templates/website/**/*.html",
                "src/resume/templates/resume/**/*.html",
                // scan all JS files (they are must be copied already from src_front)
                "src/static/js/*.js",
            ],
        }),
        minifier
    ]);


    const readFilesInParallel = async filenames => {
        return Promise.all(
            filenames.map(file => fsPromises.readFile(file))
        );
    }

    console.log("Reading CSS files and Processing result document...");

    readFilesInParallel(cssFiles)
    .then((fileBuffers) => {
        const document = postcss.document();
        for (const fileBuf of fileBuffers) {
            let file = cssFiles.shift();
            console.log(`input = ${file}`);
            const inputRoot = postcss.parse(fileBuf, { from: file });
            document.append(inputRoot);
        }
        return new Promise((resolve, reject) => {
            if (document.nodes.length === 0) {
                throw new Error('CSS document is empty');
            }
            const result = document.toResult({ to: outputFile, map: { inline: false }});
            resolve(result);
        });
    })
    .then(result => processor.process(result.root, {from: result.opts.from, to: result.opts.to, map: result.opts.map}))
    .then(optimized => {
        console.log("Writing purged and minified CSS file...");
        fsPromises.writeFile(optimized.opts.to, optimized.css)
        console.log(`Done. -> '${optimized.opts.to}'`);
        if (optimized.map) {
            console.log("Writing source map for origin CSS files...");
            fsPromises.writeFile(optimized.opts.to + '.map', optimized.map.toString())
            console.log(`Done. -> '${optimized.opts.to + '.map'}'`);
        }
    })
    .catch((error) => {
        console.error(`Error while processing files: ${error}`)
    });
}


/**
 * Copy Blog assets to separate folder.
 */
module.exports.copyOldBlogImages = function() {
    const nestedItems = sh.ls("-l", 'src_front/blog/assets/img/');

    const blogOldSrc = "src_front/blog/assets/img/";
    const copyToDest = "src/static/blog/";

    console.log("Starting: Copy old blog images..")

    createNewFolder(copyToDest);

    nestedItems.forEach(path => {
        
        const blogAssetsPath = upath.resolve(`${blogOldSrc}`, `${path.name}`);
        // console.log(`Copy FROM (i.e. blogAssetsPath):
        //     ${blogAssetsPath}`
        // );
        const destBlogPath = upath.resolve(`${copyToDest}`);
        // console.log(`Copy TO (i.e. destBlogPath):
        //     ${destBlogPath}\n`
        // );
        
        // Copy recursive, only new (updated) and preserve modification timestamp
        sh.cp('-Rup', blogAssetsPath, destBlogPath);
    });

    console.log(`Files and nested folders were copied FROM:\n${blogOldSrc}`);
    console.log(`Destination TO:\n -> ${copyToDest}`);
    console.log("Finished.\n")
}


/**
 * Filter array items based on search criteria (query).
 */
function filterItems(arr, query) {
    return arr.filter((el) => el.toLowerCase().includes(query.toLowerCase()));
}


/**
 * Create new folder by path, if it does not exist.
 */
function createNewFolder(path) {
    if (!sh.test("-e", path)) {
        sh.mkdir("-p", `${path}`);
        console.log(`Create folder: ${path} ...`);
    }
}


/**
 * Copy other rarely changed assets.
 * Mostly from previous (old) static website.
 */
module.exports.copyConstAssets = function() {
    const destPathRelative = "src/static/assets/.";
    const destPath = upath.resolve(`${destPathRelative}`);

    // List of assets relatives paths (copy sources)
    const constSrcAssets = [
        "src_front/assets/app-icons/",
        "src_front/assets/css/",
        "src_front/assets/img/",
        "src_front/assets/webfonts/*.woff",
        "src_front/assets/webfonts/*.woff2",
        "src_front/assets/webfonts/fa-brands-*.ttf",
        "src_front/assets/webfonts/fa-regular-*.ttf",
        "src_front/assets/webfonts/fa-solid-*.ttf",
        "src_front/assets/webfonts/fa-v*compatibility.ttf",
        "src_front/assets/favicon.ico",
        "src_front/assets/admin-favicon.ico",
    ];

    const wildPaths = filterItems(constSrcAssets, "*");
    let onlyFolders = wildPaths.map(wild => wild.split("*", 1)[0]);
    const onlyFoldersSet = new Set(onlyFolders);

    let folderNamesForWild = [];

    // Detect and create subfolders for wild (*) paths
    for (const folderPath of onlyFoldersSet){
        // If you use Node.js > 16.6.0 you can use at(-2) instead or reversing array below
        const newFolderName = folderPath.split("/").reverse()[1];
        folderNamesForWild.push(newFolderName);

        const destFolderPath = upath.resolve(`${destPathRelative}`, `${newFolderName}`);
        // console.log(destFolderPath);

        createNewFolder(destFolderPath);
    }

    let exactPaths = constSrcAssets.filter(x => !wildPaths.includes(x));
    // console.log(exactPaths);

    sh.cp('-Rup', exactPaths, destPath);

    let shellStrFonts = new sh.ShellString();

    for (const wild of wildPaths) {
        const srcFolderName = wild.split("*", 1)[0].split("/").reverse()[1];
        // console.log(`srcFolderName = ${srcFolderName}`);
        if (folderNamesForWild.indexOf(srcFolderName) >= 0) {
            const destFolderPath = upath.resolve(`${destPathRelative}`, `${srcFolderName}`);
            // console.log(destFolderPath);
            shellStrFonts = sh.cp('-Rup', wild, destFolderPath);
        }
    }

    console.log(`The following src files and folders were copied FROM:`);
    console.log(exactPaths.concat(wildPaths));
    console.log(`TO destination:\n -> ${destPath}\n`);
}
