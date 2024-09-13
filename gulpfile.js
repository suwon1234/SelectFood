var gulp = require("gulp");
var browserify = require("browserify");
var babelify = require("babelify");
var source = require("vinyl-source-stream");
var sourcemaps = require("gulp-sourcemaps");
var buffer = require('vinyl-buffer');
var uglify = require('gulp-uglify');

gulp.task("default", async () => 
{
    return browserify("./source/app.js", {debug:true})
        .transform(babelify, {sourceMaps:true})
        .bundle()
        .pipe(source("main.js"))
        .pipe(buffer())
        .pipe(sourcemaps.init({loadMaps: true}))
        .pipe(uglify())
        .pipe(sourcemaps.write('./'))
        .pipe(gulp.dest("/var/www/html/js"));
})