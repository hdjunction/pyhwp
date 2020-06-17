# -*- coding: utf-8 -*-
#
#   pyhwp : hwp file format parser in python
#   Copyright (C) 2010-2015 mete0r <mete0r@sarangbang.or.kr>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from argparse import ArgumentParser
from contextlib import contextmanager
from contextlib import closing
from functools import partial
import gettext
import io
import logging
import os.path
import shutil
import sys

from . import __version__ as version
from .cli import init_logger
from .transforms import BaseTransform
from .utils import cached_property


PY3 = sys.version_info.major == 3
logger = logging.getLogger(__name__)
locale_dir = os.path.join(os.path.dirname(__file__), 'locale')
locale_dir = os.path.abspath(locale_dir)
t = gettext.translation('hwp5html', locale_dir, fallback=True)
if PY3:
    _ = t.gettext
else:
    _ = t.ugettext


RESOURCE_PATH_XSL_CSS = 'xsl/hwp5css.xsl'
RESOURCE_PATH_XSL_HTML = 'xsl/hwp5html.xsl'


class HTMLTransform(BaseTransform):

    def transform_hwp5_to_css(self, hwp5file, outdir, **params):
        '''
        >>> T.transform_hwp5_to_css(hwp5file, 'styles.css', **{})
        '''
        transform_xhwp5 = self.make_transform_xhwp5_to_css(**params)
        return self.make_transform_hwp5(transform_xhwp5)(hwp5file, outdir)

    def transform_hwp5_to_html(self, hwp5file, outdir, **params):
        '''
        >>> T.transform_hwp5_to_html(hwp5file, 'index.html', **{})
        '''
        transform_xhwp5 = self.make_transform_xhwp5_to_html(**params)
        return self.make_transform_hwp5(transform_xhwp5)(hwp5file, outdir)

    def transform_hwp5_to_dir(self, hwp5file, outdir, **params):
        '''
        >>> T.transform_hwp5_to_dir(hwp5file, 'output', **{})
        '''
        with self.transformed_xhwp5_at_temp(hwp5file) as xhwp5path:
            self.transform_xhwp5_to_dir(xhwp5path, outdir, **params)

        bindata_dir = os.path.join(outdir, 'bindata')
        self.extract_bindata_dir(hwp5file, bindata_dir)

    def make_transform_xhwp5_to_css(self, **params):
        '''
        >>> T.make_transform_xhwp5_to_css(**{})('hwp5.xml', 'styles.css')
        '''
        resource_path = RESOURCE_PATH_XSL_CSS
        return self.make_xsl_transform(resource_path, **params)

    def make_transform_xhwp5_to_html(self, **params):
        '''
        >>> T.make_transform_xhwp5_to_html(**{})('hwp5.xml', 'index.html')
        '''
        resource_path = RESOURCE_PATH_XSL_HTML
        return self.make_xsl_transform(resource_path, **params)

    def transform_xhwp5_to_dir(self, xhwp5path, outdir, **params):
        '''
        >>> T.transform_xhwp5_to_dir('hwp5.xml', 'output', **{})
        '''
        html_path = os.path.join(outdir, 'index.html')
        with io.open(html_path, 'wb') as f:
            self.make_transform_xhwp5_to_html(**params)(xhwp5path, f)
        if params['embed-styles-css'] is '0':
            css_path = os.path.join(outdir, 'styles.css')
            with io.open(css_path, 'wb') as f:
                self.make_transform_xhwp5_to_css(**params)(xhwp5path, f)

    def extract_bindata_dir(self, hwp5file, bindata_dir):
        if 'BinData' not in hwp5file:
            return
        bindata_stg = hwp5file['BinData']
        if not os.path.exists(bindata_dir):
            os.mkdir(bindata_dir)

        from hwp5.storage import unpack
        unpack(bindata_stg, bindata_dir)


def main():
    from .dataio import ParseError
    from .errors import InvalidHwp5FileError
    from .utils import make_open_dest_file
    from .xmlmodel import Hwp5File

    argparser = main_argparser()
    args = argparser.parse_args()
    init_logger(args)

    hwp5path = args.hwp5file
    font_face = args.font_face + [''] * (5 - len(args.font_face))

    html_transform = HTMLTransform()

    open_dest = make_open_dest_file(args.output)
    params = {
        'sans-serif': font_face[0],
        'serif': font_face[1],
        'monospace': font_face[2],
        'cursive': font_face[3],
        'fantasy': font_face[4],
        'use-only-fallback-font': '1' if args.use_only_fallback_font else '0',
    }
    if args.css:
        transform = html_transform.transform_hwp5_to_css
        open_dest = wrap_for_css(open_dest)
    elif args.html:
        transform = html_transform.transform_hwp5_to_html
        open_dest = wrap_for_xml(open_dest)
        params['embed-styles-css'] = '1' if args.embed_styles_css else '0'
    else:
        transform = html_transform.transform_hwp5_to_dir
        dest_path = args.output
        if not dest_path:
            dest_path = os.path.splitext(os.path.basename(hwp5path))[0]
        open_dest = partial(open_dir, dest_path)
        params['embed-styles-css'] = '1' if args.embed_styles_css else '0'

    try:
        with closing(Hwp5File(hwp5path)) as hwp5file:
            with open_dest() as dest:
                transform(hwp5file, dest, **params)
    except ParseError as e:
        e.print_to_logger(logger)
    except InvalidHwp5FileError as e:
        logger.error('%s', e)
        sys.exit(1)


def main_argparser():
    parser = ArgumentParser(
        prog='hwp5html',
        description=_('HWPv5 to HTML converter'),
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {}'.format(version)
    )
    parser.add_argument(
        '--loglevel',
        help=_('Set log level.'),
    )
    parser.add_argument(
        '--logfile',
        help=_('Set log file.'),
    )
    parser.add_argument(
        '--font-face',
        nargs='+',
        default=[],
        help=_(f'Set fonts.{os.linesep}[----font-face sans-serif [serif monospace cursive fantasy]]'),
    )
    parser.add_argument(
        '--use-only-fallback-font',
        action='store_true',
        help=_(f'Set all font-family as fallback fonts.'),
    )
    parser.add_argument(
        '--output',
        help=_('Output file'),
    )
    parser.add_argument(
        '--embed-styles-css',
        action='store_true',
        help=_('Embed styles in output .html'),
    )
    parser.add_argument(
        'hwp5file',
        metavar='<hwp5file>',
        help=_('.hwp file to convert'),
    )
    generator_group = parser.add_mutually_exclusive_group()
    generator_group.add_argument(
        '--css',
        action='store_true',
        help=_('Generate CSS'),
    )
    generator_group.add_argument(
        '--html',
        action='store_true',
        help=_('Generate HTML'),
    )
    return parser


@contextmanager
def open_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    yield path


def wrap_for_css(open_dest):
    from .utils import wrap_open_dest_for_tty
    from .utils import pager
    from .utils import syntaxhighlight
    return wrap_open_dest_for_tty(open_dest, [
        pager(),
        syntaxhighlight('text/css'),
    ])


def wrap_for_xml(open_dest):
    from .utils import wrap_open_dest_for_tty
    from .utils import pager
    from .utils import syntaxhighlight
    from .utils import xmllint
    return wrap_open_dest_for_tty(open_dest, [
        pager(),
        syntaxhighlight('application/xml'),
        xmllint(format=True, nonet=True),
    ])
