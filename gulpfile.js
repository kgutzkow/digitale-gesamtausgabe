var autoprefixer = require('gulp-autoprefixer'),
    concat = require('gulp-concat'),
    gulp = require('gulp'),
    pump = require('pump'),
    sass = require('gulp-sass');


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
        gulp.dest('theme/static/js')
    ], cb);
});

gulp.task('js', gulp.parallel('js:libs', 'js:theme'));

gulp.task('default', gulp.parallel('css', 'js', 'reader'));

gulp.task('watch', gulp.series('default', function(cb) {
    gulp.watch('theme/src/**/*.scss', gulp.series('css:theme'));
    gulp.watch('theme/scripts/**/*.js', gulp.series('js:theme'));
    cb();
}))
