"""Mixer that controls volume using a Yamaha receiver."""

from __future__ import unicode_literals

import logging

from mopidy import mixer

import pykka

from mopidy_yamaha import talker


logger = logging.getLogger(__name__)


class YamahaMixer(pykka.ThreadingActor, mixer.Mixer):

    name = 'yamaha'

    def __init__(self, config):
        super(YamahaMixer, self).__init__(config)

        self.host = config['yamaha']['host']
        self.source = config['yamaha']['source']

        self._volume_cache = 0
        self._yamaha_talker = None

    def get_volume(self):
        return self._volume_cache

    def set_volume(self, volume):
        self._volume_cache = volume
        self._yamaha_talker.set_volume(volume)
        self.trigger_volume_changed(volume)

    def get_mute(self):
        return False

    def set_mute(self, mute):
        self._yamaha_talker.mute(mute)
        self.trigger_mute_changed(mute)

    def on_start(self):
        self._start_yamaha_talker()

    def _start_yamaha_talker(self):
        self._yamaha_talker = talker.YamahaTalker.start(
            host=self.host,
            source=self.source,
        ).proxy()
        self._volume_cache = self._yamaha_talker.get_volume().get()
