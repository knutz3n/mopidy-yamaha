from __future__ import unicode_literals

import unittest

import pygst
pygst.require('0.10')
import gst

from mopidy_yamaha import mixer


class MixerTest(unittest.TestCase):

    def test_is_a_gstreamer_mixer(self):
        self.assert_(issubclass(mixer.YamahaMixer, gst.Element))
