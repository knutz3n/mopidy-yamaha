from __future__ import unicode_literals

import os

import pygst
pygst.require('0.10')
import gst
import gobject

from mopidy import config, ext


__version__ = '0.1.1'


class Extension(ext.Extension):
    dist_name = 'Mopidy-Yamaha'
    ext_name = 'yamaha'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def setup(self, registry):
        from .mixer import YamahaMixer
        gobject.type_register(YamahaMixer)
        gst.element_register(YamahaMixer, 'yamahamixer', gst.RANK_MARGINAL)
