var gulp = require('gulp');
var sass = require('gulp-sass');
var autoprefixer = require('gulp-autoprefixer');
var sourceMaps = require('gulp-sourcemaps');
var plumber         = require('gulp-plumber');
var  notify          = require('gulp-notify');

var CONFIG = {
    'cssFolder': './',
    'scssFolder': 'scss',
};

function handleError(err) {
    console.log(err.toString());
    this.emit('end');
}

// Run everything
gulp.task('default', ['scss', 'minify-js']);

// Dev task with browserSync
gulp.task('watch', ['scss'], function() {
    gulp.watch(CONFIG.scssFolder + '/**/*.scss', ['scss']);
});

// Compiles SCSS files from /scss into /css
gulp.task('scss', function() {
    return gulp.src(CONFIG.scssFolder + '/**/*.scss')
        .pipe(plumber({errorHandler: notify.onError("<%= error.message %> \n\n→ <%= error.fileName %> \n\n@ <%= error.lineNumber %>")}))
        .pipe(sourceMaps.init())
        .pipe(sass({outputStyle: 'compressed'}))
        .pipe(autoprefixer())
        .pipe(sourceMaps.write())
        .pipe(gulp.dest(CONFIG.cssFolder))
        .on('error', handleError);
});

// Compiles SCSS files from /scss into /css - PRODUCTION (no source maps) - run scss-copy
gulp.task('scss-production', function() {
    return gulp.src(CONFIG.scssFolder + '/**/*.scss')
        .pipe(plumber({errorHandler: notify.onError("<%= error.message %> \n\n→ <%= error.fileName %> \n\n@ <%= error.lineNumber %>")}))
        .pipe(sourceMaps.init())
        .pipe(sass({outputStyle: 'compressed'}))
        .pipe(autoprefixer())
        .pipe(gulp.dest(CONFIG.cssFolder))
        .on('error', handleError);
});
