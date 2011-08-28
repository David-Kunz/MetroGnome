#!/usr/bin/env python

from gi.repository import Gtk, Gst, GObject
import os, sys, time

class Metronome:
 
  DURATION = 0
  DURATION_CHANGED = False
  UI_FILE = "metrognome.ui"
  PLAY_FILE = "tick.mp3"
  ABORT = False
  PLAYING = False
  DURATION_DICT = {0:True}

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

    self.source.set_property('location', self.PLAY_FILE)

    adjustment = self.builder.get_object('adjustment')
    self.DURATION = int(round(60000/adjustment.get_value()))

    window = self.builder.get_object('window')
    window.show_all()

  def sound_loop(self):
    self.ABORT = False
    self.play_sound(self.DURATION)
    GObject.timeout_add(self.DURATION, self.play_sound, self.DURATION)

  def on_button_clicked(self, button):
    if button.get_label() == 'Start':
      self.PLAYING = True
      self.player.set_state(Gst.State.NULL)
      self.sound_loop()  
      button.set_label('Stop')
    else:
      self.PLAYING = False
      self.ABORT = True
      self.stop_sound()
      button.set_label('Start')

  def set_duration(self, adjustment):
    self.DURATION = int(round(60000/adjustment.get_value()))
    print 'duration set to ' + str(self.DURATION)
    self.stop_sound()
    if self.PLAYING == True:
      self.sound_loop()
    
  
  def destroy(self, window):
    self.stop_sound()
    Gtk.main_quit()
  
  def play_sound(self, DURATION):
      print "Play!"
      if DURATION == self.DURATION:
        if self.ABORT == True:
          return False
        else:
          self.player.set_state(Gst.State.NULL)
          self.player.set_state(Gst.State.PLAYING)
          print 'self.DURATION ist:'
          print self.DURATION
          print 'DURATION ist:'
          print DURATION
          return True 
      else:
        return False
           
    
  def stop_sound(self):
    self.player.set_state(Gst.State.NULL)
    print "Stop!"
    return False






def main():
  Gst.init(sys.argv)
  app = Metronome()
  Gtk.main() 



if __name__ == '__main__':
  main()
