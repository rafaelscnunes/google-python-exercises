#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib.request

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

HMTL_HEADER = '<!DOCTYPE html>\n<html>\n<body>\n'
HTML_FOOTER = '</body>\n</html>'


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""

    base_url = 'https://' + filename.split('_')[1]
    images = set(re.findall(r'\"GET (.*/puzzle/.*[\.jpg|\.png]) HTTP/', open(filename).read()))
    return [base_url + img for img in sorted(images)]


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """

    os.makedirs(dest_dir, exist_ok=True)
    with open(os.path.join(dest_dir, 'index.html'), 'w') as f_out:
        f_out.write(HMTL_HEADER)
        for url in img_urls:
            img_filename = url.split('/')[-1]
            img_name = img_filename.split('.')[0]
            with urllib.request.urlopen(url) as html_dump:
                with open(os.path.join(dest_dir, img_filename), 'wb') as img_file:
                    img_file.write(html_dump.read())
                f_out.write('<img src="' + img_filename + '" alt="' + img_name + '">' + '\n')
        f_out.write(HTML_FOOTER)


def main():
    args = sys.argv[1:]

    if not args:
        print('usage: [--todir dir] logfile ')
        sys.exit(1)

    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    img_urls = read_urls(args[0])

    if todir:
        download_images(img_urls, todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main()
