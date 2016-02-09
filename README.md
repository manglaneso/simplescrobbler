# simplescrobbler
Simple last.fm [scrobbler](http://www.urbandictionary.com/define.php?term=Scrobble) written in python 3 using [python mutagen](https://mutagen.readthedocs.org/en/latest/)

## Install dependencies
In order to read metadata from the song, you must install python3-mutagen.
In Ubuntu like systems from version 15.10 and above:

    sudo apt-get install python3-mutagen

For previous Ubuntu versions you can install it from various sources like the [Rhythmbox third-party plugins PPA](https://launchpad.net/~fossfreedom/+archive/ubuntu/rhythmbox-plugins).

For other systems you can access the official site addressed above.

##Usage

Give the program executable privileges:

    chmod a+x simplescrobbler.py

Then execute it with the following pattern:

    LASTFM_USERNAME="your lastfm username (without quotes)" LASTFM_PASSWORD="your lastfm password (without quotes)" ./simplescrobbler.py "path to the song"
