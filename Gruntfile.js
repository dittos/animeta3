module.exports = function(grunt) {
    grunt.initConfig({
        less: {
            development: {
                options: {
                    paths: ['animeta/static/css'],
                    yuicompress: true
                },
                files: {
                    'animeta/static/css/build.css': 'animeta/static/css/*.less'
                }
            }
        },
        watch: {
            files: 'animeta/static/css/*.less',
            tasks: ['less']
        }
    });

    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-watch');

    grunt.registerTask('build', ['less']);
    grunt.registerTask('default', ['build', 'watch']);
};
