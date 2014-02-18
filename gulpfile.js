var gulp = require('gulp');
var gutil = require('gulp-util');
var less = require('gulp-less');
var concat = require('gulp-concat');

gulp.task('less', function() {
    return gulp.src([
            'components/normalize-css/normalize.css',
            'animeta/static/css/*.less'
        ])
        .pipe(less({
            paths: [
                'animeta/static/css',
                'components/semantic-grid/stylesheets/less'
            ]
        }))
        .pipe(concat('build.css'))
        .pipe(gulp.dest('animeta/static/css'));
});

gulp.task('watch', function() {
    gulp.watch('animeta/static/css/*.less', ['less']);
});

gulp.task('build', ['less']);
gulp.task('default', ['build', 'watch']);
