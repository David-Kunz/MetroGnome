#!/usr/bin/env python

from gi.repository import Gtk, Gst, GObject
import os, sys, time





class Metronome:

  DURATION = 500
  plaing = False
  UI_FILE = "metrognome.ui"
  PLAY_FILE = "tick.mp3"

  def __init__(self):
    self.builder = Gtk.Builder()
    self.builder.add_from_file(self.UI_FILE)
    self.builder.connect_signals(self) 

    self.pipeline = Gst.Pipeline(name='metrognome')
    self.source = Gst.ElementFactory.make('filesrc', 'src')
    sink = Gst.ElementFactory.make('mad', 'mad')

    self.player = Gst.Pipeline(name='player')
    self.source = Gst.ElementFactory.make('filesrc', self.PLAY_FILE)
    self.decoder = Gst.ElementFactory.make('mad', 'mp3-decoder')
    self.sink = Gst.ElementFactory.make('alsasink', 'alsa-output')

    self.player.add(self.source)
    self.player.add(self.decoder)
    self.player.add(self.sink)

    self.source.link(self.decoder)
    self.decoder.link(self.sink)

    adjustment = self.builder.get_object('adjustment')

    window = self.builder.get_object('window')
    window.show_all()

  def sound_loop(self):
    self.source.set_property('location', self.PLAY_FILE)
    self.play_sound()
    GObject.timeout_add(self.DURATION, self.play_sound)

  def on_button_clicked(self, button):
    if button.get_label() == 'Start':
      button.set_label('Stop')
      self.player.set_state(Gst.State.NULL)
      self.playing = True
      self.sound_loop()  
    else:
      button.set_label('Start')
      self.stop_sound()

  def set_duration(self, adjustment):
    self.DURATION = int(round(60000/adjustment.get_value()))

  def destroy(self, window):
    self.stop_sound()
    Gtk.main_quit()
  
  def play_sound(self):
    if self.playing == True:
      print "Play!"
      self.player.set_state(Gst.State.NULL)
      self.player.set_state(Gst.State.PLAYING)
      return True
    else:
      return False
    
  def stop_sound(self):
    self.player.set_state(Gst.State.NULL)
    self.playing = False
    print "Stop!"
    return False






def main():
  Gst.init(sys.argv)
  app = Metronome()
  Gtk.main() 



if __name__ == '__main__':
  main()
