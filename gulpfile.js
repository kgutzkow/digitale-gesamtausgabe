var autoprefixer = require('gulp-autoprefixer'),
    concat = require('gulp-concat'),
    gulp = require('gulp'),
    pump = require('pump'),
    fs = require('fs'),
    replace = require('gulp-replace'),
    hash = require('gulp-hash-filename'),
    sass = require('gulp-dart-sass');


function getHash(dirname, basename, ext) {
    const result = fs.readdirSync(dirname).map((filename) => {
        const regexp = basename + '(\.[a-zA-Z0-9]+)?\.' + ext;
        const match = filename.match(new RegExp(regexp));
        if (match && match[1]) {
            return match[1].substring(1);
        } else {
            return null;
        }
    }).filter((match) => { return match !== null; });
    if (result.length === 1) {
        return result[0];
    } else {
        return '';
    }
}

gulp.task('theme:patch', function(cb) {
    const cssAppHash = getHash('theme/static/css', 'app', 'css');
    const cssFontsHash = getHash('theme/static/css', 'fonts', 'css');
    const jsThemeHash = getHash('theme/static/js', 'theme', 'js');
    const readerCssHash = getHash('theme/static/reader', 'app', 'css');
    const readerJsHash = getHash('theme/static/reader', 'app', 'js');
    const readerVendorsHash = getHash('theme/static/reader', 'chunk-vendors', 'js');
    pump([
        gulp.src([
            'theme/templates/base.html',
            'theme/templates/tei-document.html',
        ]),
        replace(/css\/app(\.[a-zA-Z0-9]*)?\.css/, 'css/app.' + cssAppHash + '.css'),
        replace(/css\/fonts(\.[a-zA-Z0-9]*)?\.css/, 'css/fonts.' + cssFontsHash + '.css'),
        replace(/js\/theme(\.[a-zA-Z0-9]*)?\.js/, 'js/theme.' + jsThemeHash + '.js'),
        replace(/reader\/app(\.[a-zA-Z0-9]*)?\.js/, 'reader/app.' + readerJsHash + '.js'),
        replace(/reader\/app(\.[a-zA-Z0-9]*)?\.css/, 'reader/app.' + readerCssHash + '.css'),
        replace(/reader\/chunk-vendors(\.[a-zA-Z0-9]*)?\.js/, 'reader/chunk-vendors.' + readerVendorsHash + '.js'),
        gulp.dest('theme/templates')
    ], cb);
});

gulp.task('css:theme', function(cb) {
    pump([
        gulp.src([
            'theme/src/fonts.scss',
            'theme/src/app.scss'
        ]),
        sass({
            includePaths: ['node_modules/foundation-sites/scss']
        }),
        autoprefixer(),
        hash({format: '{name}.{hash}{ext}'}),
        gulp.dest('theme/static/css')
    ], cb);
});

gulp.task('css', gulp.series('css:theme'));

gulp.task('reader', function(cb) {
    pump([
        gulp.src([
            'node_modules/tei-reader/dist/js/*.*',
            'node_modules/tei-reader/dist/css/*.*',
        ]),
        hash({format: '{name}.{hash}{ext}'}),
        gulp.dest('theme/static/reader')
    ], cb);
});

gulp.task('js:libs', function(cb) {
    pump([
        gulp.src([
            'node_modules/foundation-sites/dist/js/foundation.min.js',
            'node_modules/jquery/dist/jquery.min.js',
            'node_modules/what-input/dist/what-input.min.js',
            'node_modules/femtotween//dist/femtoTween.umd.js',
        ]),
        gulp.dest('theme/static/js')
    ], cb);
});

gulp.task('js:theme', function(cb) {
    pump([
        gulp.src([
            'theme/scripts/*.js',
        ]),
        concat('theme.js'),
        hash({format: '{name}.{hash}{ext}'}),
        gulp.dest('theme/static/js')
    ], cb);
});

gulp.task('js', gulp.parallel('js:libs', 'js:theme'));

gulp.task('default', gulp.series(gulp.parallel('css', 'js', 'reader'), 'theme:patch'));

gulp.task('watch', gulp.series('default', function(cb) {
    gulp.watch('theme/src/**/*.scss', gulp.series('css:theme', 'theme:patch'));
    gulp.watch('theme/scripts/**/*.js', gulp.series('js:theme', 'theme:patch'));
    cb();
}))
