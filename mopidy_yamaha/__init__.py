from __future__ import unicode_literals

import os

from mopidy import config, ext


__version__ = '0.2.3'


class Extension(ext.Extension):
    dist_name = 'Mopidy-Yamaha'
    ext_name = 'yamaha'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['host'] = config.String()
        schema['source'] = config.String(optional=True)
        schema['party_mode'] = config.Boolean(optional=True)
        return schema

    def setup(self, registry):
        from .mixer import YamahaMixer

        registry.add('mixer', YamahaMixer)
