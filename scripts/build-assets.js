'use strict';

// const renderAssets = require('./render-assets');
const assets = require('./render-assets');


assets.copyOldBlogImages();

assets.copyConstAssets();

assets.compileFontsCSS();