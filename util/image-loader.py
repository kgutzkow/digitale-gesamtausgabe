import click
import os
import re
import requests
import subprocess

from io import StringIO
from lxml import etree


def download_image(href, slug, target_dir):
    if not os.path.exists(os.path.join(target_dir, '{0}.jpg'.format(slug))):
        response = requests.get(href)
        if href.endswith('.gif'):
            with open(os.path.join(target_dir, '{0}.gif'.format(slug)), 'wb') as out_f:
                out_f.write(response.content)
            subprocess.run(['convert', os.path.join(target_dir, '{0}.gif'.format(slug)), os.path.join(target_dir, '{0}.jpg'.format(slug))])
            os.unlink(os.path.join(target_dir, '{0}.gif'.format(slug)))
        else:
            with open(os.path.join(target_dir, '{0}.jpg'.format(slug)), 'wb') as out_f:
                out_f.write(response.content)


def strip_spaces(text):
    while re.search('\s{2,}', text):
        text = re.sub('\s{2,}', ' ', text)
    return text.strip()


@click.command()
@click.argument('base-url')
@click.argument('target-dir')
def load_images(base_url, target_dir):
    response = requests.get(base_url)
    base_url = base_url[:base_url.rfind('/') + 1]
    index = etree.parse(StringIO(response.text), etree.HTMLParser())
    links = index.xpath('//table[@align="center"]//a')
    for idx, link in enumerate(links):
        slug = link.attrib['href'][:-4]
        relative_path = ''
        if '/' in slug:
            relative_path = slug[:slug.rfind('/') + 1]
            slug = slug[slug.rfind('/') + 1:]
        print(slug)
        # Get the image page
        response = requests.get('{0}{1}'.format(base_url, link.attrib['href']))
        page = etree.parse(StringIO(response.text), etree.HTMLParser())
        # Get the images
        img_links = page.xpath('//table[@align="center"]//a')
        found = False
        for img_link in img_links:
            big_link_href = img_link.attrib['href']
            if big_link_href.endswith('.jpg') or big_link_href.endswith('.gif'):
                download_image('{0}{1}{2}'.format(base_url, relative_path, img_link.attrib['href']), '{0}-large'.format(slug), target_dir)
                download_image('{0}{1}{2}'.format(base_url, relative_path, img_link.xpath('img')[0].attrib['src']), '{0}-small'.format(slug), target_dir)
                found = True
        if not found:
            for img in page.xpath('//img'):
                if 'pixel.gif' not in img.attrib['src']:
                    download_image('{0}{1}{2}'.format(base_url, relative_path, img.attrib['src']), '{0}-large'.format(slug), target_dir)
                    download_image('{0}{1}{2}'.format(base_url, relative_path, img.attrib['src']), '{0}-small'.format(slug), target_dir)
        # Get the page content
        blocks = []
        for bold in page.xpath('//b'):
            text = strip_spaces(''.join(bold.itertext()))
            if len(text) > 0:
                blocks.append((3, text))
        blocks = [blocks[-1]]
        for block in page.xpath('//font'):
            tmp = []
            first = True
            for node in block.iter():
                if node.tag != 'font' or first:
                    first = False
                    if node.text:
                        tmp.append(node.text)
            text = strip_spaces(''.join(tmp))
            if len(text) > 0:
                blocks.append((block.attrib['size'] if 'size' in block.attrib else '3', text.strip()))
        if len(blocks) > 0:
            tmp = [blocks[0]]
            for block in blocks[1:]:
                if block[1] != tmp[0][1]:
                    tmp.append(block)
            blocks = tmp
            with open(os.path.join(target_dir, '{0}.rst'.format(slug)), 'w') as out_f:
                out_f.write('{0}\n{1}\n\n'.format(blocks[0][1], '=' * len(blocks[0][1])))
                out_f.write(':slug: {0}\n:order: {1}\n\n'.format(slug, idx + 1))
                if len(blocks) > 2:
                    blocks = blocks[1:]
                for idx2, block in enumerate(blocks):
                    if block[0] == '2':
                        out_f.write('.. class:: source\n\n')
                        out_f.write('  {0}\n'.format(block[1]))
                    else:
                        out_f.write('{0}\n'.format(block[1]))
                    if idx2 != len(blocks) - 1:
                        out_f.write('\n')


if __name__ == '__main__':
    load_images()