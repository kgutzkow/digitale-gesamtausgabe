from doit.tools import result_dep
from hashlib import md5
from io import BytesIO

import os
import re
import subprocess


def remove_file(type, name, ext):
    if os.path.exists('theme') and os.path.exists('theme/static') and os.path.exists(f'theme/static/{type}'):
        for filename in os.listdir(f'theme/static/{type}'):
            if re.match(f'{name}\.[a-zA-Z0-9]+\.{ext}', filename):
                os.unlink(f'theme/static/{type}/{filename}')
                return f'theme/static/{type}/{filename}'
    return None


def calculate_hash(source):
    hash = md5()
    if isinstance(source, BytesIO):
        hash.update(source.getvalue())
    else:
        with open(source, 'rb') as in_f:
            hash.update(in_f.read())
    return hash.hexdigest()


def create_hash_file(type, name, ext, source):
    os.makedirs(f'theme/static/{type}', exist_ok=True)
    hash = calculate_hash(source)
    with open(f'theme/static/{type}/{name}.{hash}.{ext}', 'wb') as out_f:
        if isinstance(source, BytesIO):
            out_f.write(source.getvalue())
        else:
            with open(source, 'rb') as in_f:
                out_f.write(in_f.read())
    return hash


def get_file_list(basedir, prefix=None, suffix=None):
    return [os.path.join(basedir, filename)
            for filename in os.listdir(basedir)
            if (prefix is None or filename.startswith(prefix))
            and (suffix is None or filename.endswith(suffix))]


def get_file_hash(basedir, prefix, suffix):
    for filename in os.listdir(basedir):
        match = re.match(f'{prefix}([a-zA-Z0-9]+){suffix}', filename)
        if match:
            return match.group(1)
    return None


def replace_content(filename, patterns):
    with open(filename) as in_f:
        lines = in_f.readlines()
    with open(filename, 'w') as out_f:
        for line in lines:
            for pattern in patterns:
                line = re.sub(pattern[0], pattern[1], line)
            out_f.write(line)


def task_build_reader_js():
    def run():
        remove_file('js', 'reader', 'js')
        hash = create_hash_file('js', 'reader', 'js', 'node_modules/tei-reader/public/build/bundle.js')
        return f'reader.{hash}.js'

    return {
        'actions': [run],
        'file_dep': ['node_modules/tei-reader/public/build/bundle.js'],
        'targets': [f'theme/static/js/reader.{calculate_hash("node_modules/tei-reader/public/build/bundle.js")}.js'],
    }


def task_build_reader_css():
    def run():
        remove_file('css', 'reader', 'css')
        sass_result = subprocess.run(['sass', '--load-path', 'node_modules/foundation-sites/scss', 'theme/src/reader.scss'], capture_output=True)
        postcss_result = subprocess.run(['postcss', '--use', 'autoprefixer'], input=sass_result.stdout, capture_output=True)
        hash = create_hash_file('css', 'reader', 'css', BytesIO(postcss_result.stdout))
        return f'reader.{hash}.css'

    return {
        'actions': [run],
        'file_dep': ['theme/src/reader.scss'],
    }


def task_build_app_css():
    def run():
        remove_file('css', 'app', 'css')
        sass_result = subprocess.run(['sass', '--load-path', 'node_modules/foundation-sites/scss', 'theme/src/app.scss'], capture_output=True)
        postcss_result = subprocess.run(['postcss', '--use', 'autoprefixer'], input=sass_result.stdout, capture_output=True)
        hash = create_hash_file('css', 'app', 'css', BytesIO(postcss_result.stdout))
        return f'reader.{hash}.css'

    return {
        'actions': [run],
        'file_dep': ['theme/src/app.scss'] + get_file_list('theme/src', prefix='_', suffix='.scss'),
    }


def task_build_app_js():
    def run():
        remove_file('js', 'app', 'css')
        buffer = BytesIO()
        for filename in ['image-viewer.js', 'landing-page.js']:
            with open(os.path.join('theme/scripts', filename), 'rb') as in_f:
                buffer.write(in_f.read())
        hash = create_hash_file('js', 'app', 'js', buffer)
        return hash

    return {
        'actions': [run],
        'file_dep': get_file_list('theme/scripts', suffix='.js')
    }

def task_build_fonts_css():
    def run():
        remove_file('css', 'fonts', 'css')
        sass_result = subprocess.run(['sass', '--load-path', 'node_modules/foundation-sites/scss', 'theme/src/fonts.scss'], capture_output=True)
        postcss_result = subprocess.run(['postcss', '--use', 'autoprefixer', '--no-map'], input=sass_result.stdout, capture_output=True)
        hash = create_hash_file('css', 'fonts', 'css', BytesIO(postcss_result.stdout))
        return f'reader.{hash}.css'

    return {
        'actions': [run],
        'file_dep': ['theme/src/fonts.scss'],
    }


def task_patch_theme():
    def run():
        reader_css_hash = get_file_hash('theme/static/css', 'reader.', '.css')
        reader_js_hash = get_file_hash('theme/static/js', 'reader.', '.js')
        app_css_hash = get_file_hash('theme/static/css', 'app.', '.css')
        app_js_hash = get_file_hash('theme/static/js', 'app.', '.js')
        fonts_css_hash = get_file_hash('theme/static/css', 'fonts.', '.css')
        patterns = [
            (r'reader\.[a-zA-Z0-9]+\.css', f'reader.{reader_css_hash}.css'),
            (r'reader\.[a-zA-Z0-9]+\.js', f'reader.{reader_js_hash}.js'),
            (r'app\.[a-zA-Z0-9]+\.css', f'app.{app_css_hash}.css'),
            (r'app\.[a-zA-Z0-9]+\.js', f'app.{app_js_hash}.js'),
            (r'fonts\.[a-zA-Z0-9]+\.css', f'fonts.{fonts_css_hash}.css'),
        ]
        replace_content('theme/templates/base.html', patterns)
        replace_content('theme/templates/tei-document.html', patterns)
        return f'{reader_css_hash}::{reader_js_hash}::{app_css_hash}::{app_js_hash}::{fonts_css_hash}'

    return {
        'actions': [run],
        'uptodate': [
            result_dep('build_reader_js'),
            result_dep('build_reader_css'),
            result_dep('build_app_css'),
            result_dep('build_app_js'),
            result_dep('build_fonts_css')
        ]
    }

def task_rebuild_site():
    return {
        'actions': ['pelican -d'],
        'uptodate': [result_dep('patch_theme')],
        'file_dep': get_file_list('theme/templates', suffix='.html')
    }
