import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Gst", "1.0")
from gi.repository import Gtk, Gst, GObject
import os
import sys

class VideoWindow(Gtk.Window):

    path = "video.mp4"
    #path = "videotestsrc"

    def __init__(self):
        Gtk.Window.__init__(self, title="Video Test")
        self.path = "{}/{}".format(os.path.dirname(os.path.realpath(__file__)), self.path)
        v_widget = VideoWidget(self.path)
        v_widget.set_size_request(1280, 720)
        self.add(v_widget)

class VideoWidget(Gtk.Box):
    _path = None
    _widget = None
    _player = None
    _sink = None

    def __init__(self, path):
        super().__init__()
        self.connect('realize', self._on_realize)
        self._path = path
        self._player = Gst.ElementFactory.make("playbin", "bin")
        self._sink = Gst.ElementFactory.make("gtksink", "sink")
        self._player.set_property("video-sink", self._sink)
        self._widget = self._sink.get_property("widget")
        self.add(self._widget)
        self._widget.set_size_request(1280, 720)
        self._player.set_property("uri", "file://{}".format(self._path))
    
    def _on_realize(self, widget):
        self._player.set_state(Gst.State.PLAYING)

GObject.threads_init()
Gst.init(None)
Gst.init_check(None)
window = VideoWindow()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()


