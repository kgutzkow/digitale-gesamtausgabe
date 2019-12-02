var gulp = require('gulp'),
    sass = require('gulp-sass'),
    autoprefixer = require('gulp-autoprefixer'),
    concat = require('gulp-concat'),
    pump = require('pump');

gulp.task('css:theme', function(cb) {
    pump([
        gulp.src('theme/src/app.scss'),
        sass({
            includePaths: ['node_modules/foundation-sites/scss']
        }),
        autoprefixer(),
        gulp.dest('theme/static/css')
    ], cb);
});

gulp.task('css:reader', function(cb) {
    pump([
        gulp.src(['node_modules/tei-reader/dist/app.css']),
        concat('tei-reader.css'),
        gulp.dest('theme/static/css')
    ], cb);
});

gulp.task('css', gulp.series('css:theme', 'css:reader'));

gulp.task('js:reader', function(cb) {
    pump([
        gulp.src([
            'node_modules/tei-reader/dist/app.js',
        ]),
        concat('tei-reader.js'),
        gulp.dest('theme/static/js')
    ], cb);
});

gulp.task('js:theme', function(cb) {
    pump([
        gulp.src([
            'node_modules/foundation-sites/dist/js/foundation.min.js',
            'node_modules/jquery/dist/jquery.min.js',
            'node_modules/what-input/dist/what-input.min.js',
        ]),
        gulp.dest('theme/static/js')
    ], cb);
});

gulp.task('js', gulp.parallel('js:reader', 'js:theme'));

gulp.task('default', gulp.parallel('css', 'js'));

gulp.task('watch', gulp.series('default', function(cb) {
    gulp.watch('theme/src/**/*.scss', gulp.series('css:theme'));
    cb();
}))
