"""Mixer that controls volume using a Yamaha receiver."""

from __future__ import unicode_literals

import logging

import pygst
pygst.require('0.10')
import gobject
import gst

from mopidy_yamaha import talker


logger = logging.getLogger(__name__)


class YamahaMixer(gst.Element, gst.ImplementsInterface, gst.interfaces.Mixer):
    __gstdetails__ = (
        'YamahaMixer',
        'Mixer',
        'Mixer to control network enabled Yamaha receivers',
        'Mopidy')

    host = gobject.property(type=str)
    source = gobject.property(type=str, default=None)

    _volume_cache = -805
    _yamaha_talker = None

    def list_tracks(self):
        track = create_track(
            label='Master',
            initial_volume=-805,
            min_volume=-805,
            max_volume=0,
            num_channels=1,
            flags=(
                gst.interfaces.MIXER_TRACK_MASTER |
                gst.interfaces.MIXER_TRACK_OUTPUT))
        return [track]

    def get_volume(self, track):
        return [self._volume_cache]

    def set_volume(self, track, volumes):
        if len(volumes):
            volume = volumes[0]
            self._volume_cache = volume
            self._yamaha_talker.set_volume(volume)

    def set_mute(self, track, mute):
        self._yamaha_talker.mute(mute)

    def do_change_state(self, transition):
        if transition == gst.STATE_CHANGE_NULL_TO_READY:
            self._start_yamaha_talker()
        return gst.STATE_CHANGE_SUCCESS

    def _start_yamaha_talker(self):
        self._yamaha_talker = talker.YamahaTalker.start(
            host=self.host,
            source=self.source,
        ).proxy()
        self._volume_cache = self._yamaha_talker.get_volume().get()


def create_track(label, initial_volume, min_volume, max_volume,
                 num_channels, flags):

    class Track(gst.interfaces.MixerTrack):
        def __init__(self):
            super(Track, self).__init__()
            self.volumes = (initial_volume,) * self.num_channels

        @gobject.property
        def label(self):
            return label

        @gobject.property
        def min_volume(self):
            return min_volume

        @gobject.property
        def max_volume(self):
            return max_volume

        @gobject.property
        def num_channels(self):
            return num_channels

        @gobject.property
        def flags(self):
            return flags

    return Track()
