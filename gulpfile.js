'use strict';

var gulp = require('gulp'),
    sass = require('gulp-sass'),
    autoprefixer = require('gulp-autoprefixer'),
    pump = require('pump');

gulp.task('default', ['css']);

gulp.task('css', function(cb) {
    pump([
        gulp.src('theme/src/app.scss'),
        sass({
            includePaths: ['node_modules/foundation-sites/scss']
        }),
        autoprefixer({
            browsers: ['last 2 versions'],
            cascade: false
        }),
        gulp.dest('theme/static/css')
    ], cb);
});

gulp.task('watch', ['default'], function(db) {
    gulp.watch('theme/src/**/*.scss', ['css']);
})
