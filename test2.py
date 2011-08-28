#!/usr/bin/env python

from gi.repository import Gtk, Gst, GObject
import os, sys, time

class sound_loop:
  ALIVE = True
  DURATION = 0
  PLAYING = False
   
  def __init__(self, DURATION, Metronome, PLAYING):
    print 'loopy created'
    self.DURATION = DURATION
    self.PLAYING = PLAYING
    if self.PLAYING: self.sound_loop(Metronome)

  def sound_loop(self, Metronome):
    GObject.timeout_add(self.DURATION, self.play_sound(Metronome)) 

  def play_sound(self, Metronome):
    if self.ALIVE:
      print 'Alive!'
      Metronome.player.set_state(Gst.State.NULL)
      Metronome.player.set_state(Gst.State.PLAYING)
      self.sound_loop(Metronome)
      return False 
    else:
      print 'Not Alive!'
      Metronome.player.set_state(Gst.State.NULL)
      return False

  def set_playing(self, PLAYING, Metronome):
    if self.PLAYING == PLAYING: print 'nothing to do...'
    else:
      self.PLAYING = PLAYING
      if self.PLAYING == True:
        self.sound_loop(Metronome)    
   

  def kill(self, string):
    self.ALIVE = False
    print string
   

class Metronome:
 
  DURATION = 0
  DURATION_CHANGED = False
  UI_FILE = "metrognome.ui"
  PLAY_FILE = "tick.mp3"
  PLAYING = False
  player = Gst.Pipeline(name='player')

  def __init__(self):
    self.builder = Gtk.Builder()
    self.builder.add_from_file(self.UI_FILE)
    self.builder.connect_signals(self) 

    self.pipeline = Gst.Pipeline(name='metrognome')
    self.source = Gst.ElementFactory.make('filesrc', 'src')
    sink = Gst.ElementFactory.make('mad', 'mad')

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
    

  def on_button_clicked(self, button):
    self.player.set_state(Gst.State.NULL)
    if button.get_label() == 'Start':
      loopy = sound_loop(self.DURATION, self, True)
      #loopy.set_playing(True, self)
      self.PLAYING = True
      button.set_label('Stop')
    else:
      self.PLAYING = False
      loopy.kill('getoetet!!')
      button.set_label('Start')

  def set_duration(self, adjustment):
    self.DURATION = int(round(60000/adjustment.get_value()))
    print 'duration set to ' + str(self.DURATION)
  
           

  
  def destroy(self, window):
    Gtk.main_quit()




def main():
  Gst.init(sys.argv)
  app = Metronome()
  Gtk.main() 



if __name__ == '__main__':
  main()
