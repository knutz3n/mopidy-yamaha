*************
Mopidy-Yamaha
*************

.. image:: https://img.shields.io/pypi/v/Mopidy-Yamaha.svg?style=flat
    :target: https://pypi.python.org/pypi/Mopidy-Yamaha/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/Mopidy-Yamaha.svg?style=flat
    :target: https://pypi.python.org/pypi/Mopidy-Yamaha/
    :alt: Number of PyPI downloads

.. image:: https://img.shields.io/travis/knutz3n/mopidy-yamaha/master.png?style=flat
    :target: https://travis-ci.org/mopidy/mopidy-yamaha
    :alt: Travis CI build status

.. image:: https://img.shields.io/coveralls/knutz3n/mopidy-yamaha/master.svg?style=flat
   :target: https://coveralls.io/r/knutz3n/mopidy-yamaha?branch=master
   :alt: Test coverage

`Mopidy <http://www.mopidy.com/>`_ extension for controlling volume on
external Yamaha network connected receivers. Developed and tested with a Yamaha RX-V673.


Installation
============

Install by running::

    sudo pip install Mopidy-Yamaha


Configuration
=============

The Mopidy-Yamaha extension is enabled by default. To disable it, add the
following to ``mopidy.conf``::

    [yamaha]
    enabled = false

The Yamaha receiver must be connected to the local network and the receiver ip
must be specified in the configuration.

To use the Yamaha receiver to control volume, set the ``audio/mixer`` config
value in ``mopidy.conf`` to ``yamaha``. You must also add some
properties to the ``yamaha`` config section.

Supported properties:

- ``host``: The ip or hostname to the receiver.

- ``source``: The source that should be selected on the amplifier, like
  ``HDMI1``, ``AV_1``, ``AUDIO_1``, etc. Leave unset if you don't want
  the mixer to change it for you.

- ``party_mode``: Enable/Disable party mode. Party mode sends the same audio to
  all of the receiver's zones. Not available on all receivers.
  Example values: ``on`` or ``off``.

Configuration example::

    [audio]
    mixer = yamaha

    # If the amplifier is available at IP 192.168.1.15
    # and audio is connected to the HDMI 2 port.
    [yamaha]
    host = 192.168.1.15
    source = HDMI2
    party_mode = off


Project resources
=================

- `Source code <https://github.com/knutz3n/mopidy-yamaha>`_
- `Issue tracker <https://github.com/knutz3n/mopidy-yamaha/issues>`_
- `Download development snapshot <https://github.com/knutz3n/mopidy-yamaha/tarball/master#egg=Mopidy-Yamaha-dev>`_


Changelog
=========

v0.2.6 (2017-12-09)
-------------------
- Fix 'YamahaMixer mixer returned bad data' Error. Thanks @rawdlite.

v0.2.5 (2014-10-07)
-------------------
- Fix bug which caused party mode never to get enabled

v0.2.4 (2014-10-03)
-------------------
- Fix spelling in documentation

v0.2.3 (2014-10-03)
-------------------
- Add support for party mode

v0.2.2 (2014-08-06)
-------------------
- Fix wrong configuration parameter in example docs

v0.2.1 (2014-08-06)
-------------------

- Update README to reflect configuration changes

v0.2.0 (2014-08-06)
-------------------

- Use the new Mopidy mixer API (requires Mopidy >=v0.19)
- New configuration section. Remember to update your ``mopidy.conf``

v0.1.2 (2014-02-14)
-------------------

- Update changelog

v0.1.1 (2014-02-14)
-------------------

- Minor doc changes
- Add talker test for mute on/off

v0.1 (2014-02-13)
-----------------

- Initial release
