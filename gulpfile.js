'use strict';

var gulp = require('gulp'),
    sass = require('gulp-sass'),
    autoprefixer = require('gulp-autoprefixer'),
    concat = require('gulp-concat'),
    pump = require('pump');

gulp.task('default', ['css', 'js']);

gulp.task('css', ['css:theme', 'css:reader']);

gulp.task('css:theme', function(cb) {
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

gulp.task('css:reader', function(cb) {
    pump([
        gulp.src(['node_modules/digital-edition-reader/dist/edition-reader.css']),
        concat('digital-edition-reader.css'),
        gulp.dest('theme/static/css')
    ], cb);
})

gulp.task('js', function(cb) {
    pump([
        gulp.src([
            'node_modules/digital-edition-reader/dist/edition-reader-vendor.js',
            'node_modules/digital-edition-reader/dist/edition-reader.js',
        ]),
        concat('digital-edition-reader.js'),
        gulp.dest('theme/static/js')
    ], cb);
});

gulp.task('watch', ['default'], function(db) {
    gulp.watch('theme/src/**/*.scss', ['css:theme']);
})
