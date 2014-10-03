from __future__ import unicode_literals

import unittest

import urllib2

from StringIO import StringIO

import example_responses

import xmltodict

from mopidy_yamaha import talker


class YamahaTalkerTest(unittest.TestCase):

    requests = []
    default_config = {
        'host': '192.168.1.15',
        'source': 'HDMI2',
        'party_mode': True
        }

    def test_on_start_sends_GetParam(self):
        self._start_talker()

        self.assertEquals(5, len(self.mock_requests))
        self._assert_request_data('''<YAMAHA_AV cmd="GET">
                <System><Config>GetParam</Config></System>
            </YAMAHA_AV>''')
        self._assert_request_data('''<YAMAHA_AV cmd="PUT">
                <System>
                    <Power_Control><Power>On</Power></Power_Control>
                </System>
            </YAMAHA_AV>''')
        self._assert_request_data('''<YAMAHA_AV cmd="PUT">
                <Main_Zone>
                    <Input><Input_Sel>HDMI2</Input_Sel></Input>
                </Main_Zone>
            </YAMAHA_AV>''')
        self._assert_request_data('''<YAMAHA_AV cmd="PUT">
                <Main_Zone><Volume><Mute>Off</Mute></Volume></Main_Zone>
            </YAMAHA_AV>''')
        self._assert_request_data('''<YAMAHA_AV cmd="PUT">
                <System><Party_Mode><Mode>On</Mode></Party_Mode></System>
            </YAMAHA_AV>''')
        self.assertEquals('RX-V673', self.yamaha_talker._model)

    def test_start_with_party_mode_on(self):
        self._start_talker(party_mode=True)
        self._assert_request_data('''<YAMAHA_AV cmd="PUT">
                <System><Party_Mode><Mode>On</Mode></Party_Mode></System>
            </YAMAHA_AV>''')

    def test_start_with_party_mode_off(self):
        self._start_talker(party_mode=False)
        self._assert_request_data('''<YAMAHA_AV cmd="PUT">
                <System><Party_Mode><Mode>Off</Mode></Party_Mode></System>
            </YAMAHA_AV>''')

    def test_start_with_party_mode_missing(self):
        self._start_talker(party_mode=None)
        party_mode_requests = [
            r for r in self.mock_requests
            if 'Party_Mode' in r.get_data()
            ]
        self.assertEquals(0, len(party_mode_requests))

    def test_mute_on(self):
        self._start_talker()

        mock_requests = self._mockRequest(example_responses.Basic_Status)

        self.yamaha_talker.mute(True)
        self._assert_request_data('''<YAMAHA_AV cmd="PUT">
                <Main_Zone><Volume><Mute>On</Mute></Volume></Main_Zone>
            </YAMAHA_AV>''', requests=mock_requests)

    def test_mute_off(self):
        self._start_talker()
        mock_requests = self._mockRequest(example_responses.Basic_Status)

        self.yamaha_talker.mute(False)

        self._assert_request_data('''<YAMAHA_AV cmd="PUT">
                <Main_Zone><Volume><Mute>Off</Mute></Volume></Main_Zone>
            </YAMAHA_AV>''', requests=mock_requests)

    def test_get_volume(self):
        self._start_talker()

        mock_requests = self._mockRequest(example_responses.Basic_Status)

        self.yamaha_talker.get_volume()

        self._assert_request_data('''<YAMAHA_AV cmd="GET">
                <Main_Zone><Basic_Status>GetParam</Basic_Status></Main_Zone>
            </YAMAHA_AV>''', requests=mock_requests)

    def test_set_volume(self):
        self._start_talker()

        volume = 20
        mock_requests = self._mockRequest(example_responses.Put_Volume)

        self.yamaha_talker.set_volume(volume)
        self._assert_request_data('''<YAMAHA_AV cmd="PUT">
                <Main_Zone>
                    <Volume>
                        <Lvl><Val>%d</Val><Exp>1</Exp><Unit>dB</Unit></Lvl>
                    </Volume>
                </Main_Zone>
            </YAMAHA_AV>''' % -645, requests=mock_requests)

    def test_set_volume_is_aligned_to_whole_5_values(self):
        self._start_talker()

        set_volume = 11
        expect_volume = -720
        mock_requests = self._mockRequest(example_responses.Put_Volume)

        self.yamaha_talker.set_volume(set_volume)

        self._assert_request_data('''<YAMAHA_AV cmd="PUT">
                <Main_Zone>
                    <Volume>
                        <Lvl><Val>%d</Val><Exp>1</Exp><Unit>dB</Unit></Lvl>
                    </Volume>
                </Main_Zone>
            </YAMAHA_AV>''' % expect_volume, requests=mock_requests)

    def _start_talker(self, *args, **kwargs):
        config = dict(self.default_config, **kwargs)
        self.yamaha_talker = talker.YamahaTalker(**config)
        self.mock_requests = self._mockRequest(example_responses.GetParam)
        self.yamaha_talker.on_start()

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

    def _assert_request_data(self, data, requests=None):
        if requests is None:
            requests = self.mock_requests
        xml_data = xmltodict.parse(data)
        matching = [
            r for r in requests
            if xml_data == xmltodict.parse(r.get_data())
            ]
        self.assertEquals(1, len(matching))
        self.assertEquals(xml_data, xmltodict.parse(matching[0].get_data()))
