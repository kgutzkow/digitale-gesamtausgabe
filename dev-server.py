#!/usr/bin/env python
from livereload import Server, shell

shell('jupyter-book clean content')()
build_content = shell('jupyter-book build content')
build_content()

server = Server()
server.watch('content/**/*.md', build_content)
server.watch('content/**/*.rst', build_content)
server.watch('content/**/*.tei', build_content)
server.watch('content/**/*.yml', shell('jupyter-book build content --all'))
server.serve(root='content/_build/html', port=8000)
