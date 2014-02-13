from __future__ import unicode_literals

import unittest
import xmltodict

import urllib2
from StringIO import StringIO

from mopidy_yamaha import talker

import example_responses


class YamahaTalkerTest(unittest.TestCase):

    requests = []

    def setUp(self):
        self.yamaha_talker = talker.YamahaTalker(
            host='192.168.1.15',
            source='HDMI2'
            )

    def test_on_start_sends_GetParam(self):
        mock_requests = self._mockRequest(example_responses.GetParam)

        self.yamaha_talker.on_start()

        self.assertEquals(4, len(mock_requests))
        self.assertEquals(
            xmltodict.parse('''<YAMAHA_AV cmd="GET">
                <System><Config>GetParam</Config></System>
            </YAMAHA_AV>'''),
            xmltodict.parse(mock_requests[0].get_data())
            )
        self.assertEquals(
            xmltodict.parse('''<YAMAHA_AV cmd="PUT">
                <System>
                    <Power_Control><Power>On</Power></Power_Control>
                </System>
            </YAMAHA_AV>'''),
            xmltodict.parse(mock_requests[1].get_data())
            )
        self.assertEquals(
            xmltodict.parse('''<YAMAHA_AV cmd="PUT">
                <Main_Zone>
                    <Input><Input_Sel>HDMI2</Input_Sel></Input>
                </Main_Zone>
            </YAMAHA_AV>'''),
            xmltodict.parse(mock_requests[2].get_data())
            )
        self.assertEquals(
            xmltodict.parse('''<YAMAHA_AV cmd="PUT">
                <Main_Zone><Volume><Mute>Off</Mute></Volume></Main_Zone>
            </YAMAHA_AV>'''),
            xmltodict.parse(mock_requests[3].get_data())
            )
        self.assertEquals('RX-V673', self.yamaha_talker._model)

    def test_mute_on(self):
        mock_requests = self._mockRequest(example_responses.Basic_Status)

        self.yamaha_talker.mute(True)

        self.assertEquals(1, len(mock_requests))
        self.assertEquals(
            xmltodict.parse('''<YAMAHA_AV cmd="PUT">
                <Main_Zone><Volume><Mute>On</Mute></Volume></Main_Zone>
            </YAMAHA_AV>'''),
            xmltodict.parse(mock_requests[0].get_data())
            )

    def test_mute_off(self):
        mock_requests = self._mockRequest(example_responses.Basic_Status)

        self.yamaha_talker.mute(False)

        self.assertEquals(1, len(mock_requests))
        self.assertEquals(
            xmltodict.parse('''<YAMAHA_AV cmd="PUT">
                <Main_Zone><Volume><Mute>Off</Mute></Volume></Main_Zone>
            </YAMAHA_AV>'''),
            xmltodict.parse(mock_requests[0].get_data())
            )

    def test_get_volume(self):
        mock_requests = self._mockRequest(example_responses.Basic_Status)

        self.yamaha_talker.get_volume()

        self.assertEquals(1, len(mock_requests))
        self.assertEquals(
            xmltodict.parse('''<YAMAHA_AV cmd="GET">
                <Main_Zone><Basic_Status>GetParam</Basic_Status></Main_Zone>
            </YAMAHA_AV>'''),
            xmltodict.parse(mock_requests[0].get_data())
            )

    def test_set_volume(self):
        volume = -200
        mock_requests = self._mockRequest(example_responses.Put_Volume)

        self.yamaha_talker.set_volume(volume)

        self.assertEquals(1, len(mock_requests))
        self.assertEquals(
            xmltodict.parse('''<YAMAHA_AV cmd="PUT">
                <Main_Zone>
                    <Volume>
                        <Lvl><Val>%d</Val><Exp>1</Exp><Unit>dB</Unit></Lvl>
                    </Volume>
                </Main_Zone>
            </YAMAHA_AV>''' % volume),
            xmltodict.parse(mock_requests[0].get_data())
            )

    def test_set_volume_is_aligned_to_whole_5_values(self):
        set_volume = -201
        expect_volume = -205
        mock_requests = self._mockRequest(example_responses.Put_Volume)

        self.yamaha_talker.set_volume(set_volume)

        self.assertEquals(1, len(mock_requests))
        self.assertEquals(
            xmltodict.parse('''<YAMAHA_AV cmd="PUT">
                <Main_Zone>
                    <Volume>
                        <Lvl><Val>%d</Val><Exp>1</Exp><Unit>dB</Unit></Lvl>
                    </Volume>
                </Main_Zone>
            </YAMAHA_AV>''' % expect_volume),
            xmltodict.parse(mock_requests[0].get_data())
            )

    def _mockRequest(self, response_xml):
        mock_requests = []

        def mock_response(req):
            mock_requests.append(req)
            if (req.get_full_url()
                    == 'http://%s/YamahaRemoteControl/ctrl'
                    % self.yamaha_talker.host):
                resp = urllib2.addinfourl(
                    StringIO(response_xml),
                    None, req.get_full_url())
                resp.code = 200
                resp.msg = "OK"
                return resp

        class MockHTTPHandler(urllib2.HTTPHandler):
            requests = []

            def http_open(self, req):
                return mock_response(req)

        urllib2.install_opener(urllib2.build_opener(MockHTTPHandler))
        return mock_requests
