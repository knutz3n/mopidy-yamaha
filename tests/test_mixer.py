from __future__ import unicode_literals

import unittest

import mopidy.mixer

import pykka

from mopidy_yamaha import mixer


class MixerTest(unittest.TestCase):

    def test_is_a_mopidy_mixer(self):
        self.assert_(issubclass(mixer.YamahaMixer, mopidy.mixer.Mixer))

    def test_is_a_threadnig_actor(self):
        self.assert_(issubclass(mixer.YamahaMixer, pykka.ThreadingActor))
