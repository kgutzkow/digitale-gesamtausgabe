var gulp = require('gulp'),
    sass = require('gulp-sass'),
    autoprefixer = require('gulp-autoprefixer'),
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

gulp.task('js', gulp.parallel('js:theme'));

gulp.task('default', gulp.parallel('css', 'js', 'reader'));

gulp.task('watch', gulp.series('default', function(cb) {
    gulp.watch('theme/src/**/*.scss', gulp.series('css:theme'));
    cb();
}))
