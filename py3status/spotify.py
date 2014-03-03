import subprocess
import sys, dbus
from os import system
class Py3status:
    """
    Empty and basic py3status class.

    NOTE: py3status will NOT execute:
        - methods starting with '_'
        - methods decorated by @property and @staticmethod

    NOTE: reserved method names:
        - 'kill' method for py3status exit notification
        - 'on_click' method for click events from i3bar
    """

    def kill(self, i3status_output_json, i3status_config):
        """
        This method will be called upon py3status exit.
        """
        pass

    def on_click(self, i3status_output_json, i3status_config, event):
        """
        This method will be called when a click event occurs on this module's
        output on the i3bar.

        Example 'event' json object:
        {'y': 13, 'x': 1737, 'button': 1, 'name': 'empty', 'instance': 'first'}
        """
        reload(sys).setdefaultencoding('utf8')

        bus_name = 'org.mpris.MediaPlayer2.spotify'
        object_path = '/org/mpris/MediaPlayer2'
        interface_name = 'org.freedesktop.DBus.Properties'
        dbus_interface = 'org.mpris.MediaPlayer2.Player'

        
        bus = dbus.SessionBus()
        spotify = bus.get_object(bus_name, object_path)
        iface = dbus.Interface(spotify, interface_name)
        # props = iface.Get(dbus_interface, 'Metadata')

        if event['name'] == 'pauseSpotify':
            spotify.PlayPause()
            system("killall -USR1 py3status")
        elif event['name'] == 'nextSpotify':
            spotify.Next()
            system("killall -USR1 py3status")
        elif event['name'] == 'prevSpotify':
            spotify.Previous()
            system("killall -USR1 py3status")
        
        pass

    def nextSpotify(self, i3status_output_json, i3status_config):
        response = {'full_text':'NEXT', 'name':'nextSpotify','color':"#60b48a"}
        return (2, response)

    def pauseSpotify(self, i3status_output_json, i3status_config):
        reload(sys).setdefaultencoding('utf8')

        bus_name = 'org.mpris.MediaPlayer2.spotify'
        object_path = '/org/mpris/MediaPlayer2'
        interface_name = 'org.freedesktop.DBus.Properties'
        dbus_interface = 'org.mpris.MediaPlayer2.Player'
        status = ""
        
        bus = dbus.SessionBus()
        spotify = bus.get_object(bus_name, object_path)
        iface = dbus.Interface(spotify, interface_name)

        status = iface.Get(dbus_interface, 'PlaybackStatus')
        if status == 'Playing':
            text = "PAUSE"
        else:
            text = "PLAY"
        response = {'full_text':text, 'name':'pauseSpotify','color':"#dcdccc"}
        return (1, response)

    def prevSpotify(self, i3status_output_json, i3status_config):
        response = {'full_text':'PREV', 'name':'prevSpotify','color':"#60b48a"}
        return (0, response)

    def empty(self, i3status_output_json, i3status_config):
        reload(sys).setdefaultencoding('utf8')

        bus_name = 'org.mpris.MediaPlayer2.spotify'
        object_path = '/org/mpris/MediaPlayer2'
        interface_name = 'org.freedesktop.DBus.Properties'
        dbus_interface = 'org.mpris.MediaPlayer2.Player'

        artist_desc = 'xesam:artist'
        title_desc = 'xesam:title'

        try:
            bus = dbus.SessionBus()
            spotify = bus.get_object(bus_name, object_path)
            iface = dbus.Interface(spotify, interface_name)
            props = iface.Get(dbus_interface, 'Metadata')

            if(props.has_key(artist_desc)):
                artist = props.get(artist_desc)[0]
            
            if(props.has_key('xesam:title')):
                title = props.get('xesam:title')

            message = '%s - %s' % (artist, title)
        except dbus.exceptions.DBusException, e:
            message = 'SPOTIFY'
        except NameError, e:
            message = 'SPOTIFY'



        response = {'full_text': message, 'name': 'spotify', 'instance': '0','color':"#dcdccc"}
        return (3, response)