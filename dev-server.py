#!/usr/bin/env python
from livereload import Server, shell

shell('jupyter-book clean content')()
incremental_build = shell('jupyter-book build content')
full_build = shell('jupyter-book build content --all')
full_build()

server = Server()
server.watch('content/**/*.md', incremental_build)
server.watch('content/**/*.rst', incremental_build)
server.watch('content/**/*.tei', incremental_build)
server.watch('content/**/*.yml', full_build)
server.watch('content/_static/*.*', full_build)
server.serve(root='content/_build/html', port=8000)
