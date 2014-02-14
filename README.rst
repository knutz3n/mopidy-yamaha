*************
Mopidy-Yamaha
*************

.. image:: https://pypip.in/v/Mopidy-Yamaha/badge.png
    :target: https://pypi.python.org/pypi/Mopidy-Yamaha/
    :alt: Latest PyPI version

.. image:: https://pypip.in/d/Mopidy-Yamaha/badge.png
    :target: https://pypi.python.org/pypi/Mopidy-Yamaha/
    :alt: Number of PyPI downloads

.. image:: https://travis-ci.org/knutz3n/mopidy-yamaha.png?branch=master
    :target: https://travis-ci.org/mopidy/mopidy-yamaha
    :alt: Travis CI build status

.. image:: https://coveralls.io/repos/knutz3n/mopidy-yamaha/badge.png?branch=master
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
value in ``mopidy.conf`` to ``yamahamixer``. You probably also needs to add some
properties to the ``audio/mixer`` config value.

Supported properties includes:

- ``host``: The ip or hostname to the receiver.

- ``source``: The source that should be selected on the amplifier, like
  ``HDMI1``, ``AV_1``, ``AUDIO_1``, etc. Leave unset if you don't want
  the mixer to change it for you.

Configuration examples::

    # Minimum configuration, if the amplifier is available at IP 192.168.1.15
    [audio]
    mixer = yamahamixer host=192.168.1.15

    # Full configuration
    [audio]
    mixer = yamahamixer host=192.168.1.15 source=HDMI2


Project resources
=================

- `Source code <https://github.com/knutz3n/mopidy-yamaha>`_
- `Issue tracker <https://github.com/knutz3n/mopidy-yamaha/issues>`_
- `Download development snapshot <https://github.com/knutz3n/mopidy-yamaha/tarball/master#egg=Mopidy-Yamaha-dev>`_


Changelog
=========

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
