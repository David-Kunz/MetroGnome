#!/usr/bin/env python


from gi.repository import Gtk, Gst, GObject
import os, sys, time


class Metronome:
  PLAYING = False
  TICK = 0
  MAXTICK = 4
  DURATION = 0
  DURATION_CHANGED = False
  UI_FILE = "metrognome.ui"
  PLAY_FILE = "tick.mp3"
  TAG = 0

  def __init__(self):
    self.builder = Gtk.Builder()
    self.builder.add_from_file(self.UI_FILE)
    self.builder.connect_signals(self) 

 
    #self.player = Gst.ElementFactory.make('playbin2', 'player')
    source = Gst.ElementFactory.make('filesrc', 'source')
    decoder = Gst.ElementFactory.make('mad', 'decoder')
    converter = Gst.ElementFactory.make('audioconvert', 'converter')
    sink = Gst.ElementFactory.make('alsasink', 'sink')
    self.player = Gst.Pipeline()
    self.player.add(source)
    self.player.add(decoder)
    self.player.add(converter)
    self.player.add(sink)

    source.link(decoder)
    decoder.link(converter)
    converter.link(sink)
    source.set_property('location', self.PLAY_FILE)

    adjustment = self.builder.get_object('adjustment')
    self.DURATION = int(round(60000/adjustment.get_value()))

    window = self.builder.get_object('window')
    window.show_all()

  def sound_loop(self):
    self.play_sound()
    self.TAG = GObject.timeout_add(self.DURATION, self.play_sound)

  def on_button_clicked(self, button):
    if button.get_label() == 'Start':
      button.set_label('Stop')
      self.player.set_state(Gst.State.READY)
      self.PLAYING = True
      self.sound_loop()  
    else:
      GObject.source_remove(self.TAG)
      button.set_label('Start')
      self.stop_sound()

  def set_duration(self, adjustment):
    self.DURATION = int(round(60000/adjustment.get_value()))
    if self.PLAYING == True:
      GObject.source_remove(self.TAG)
      self.sound_loop()

  def destroy(self, window):
    self.stop_sound()
    Gtk.main_quit()
  
  def play_sound(self):
      if self.PLAYING == False:
        self.player.set_state(Gst.State.READY)
        return False
      else:
        if self.TICK == self.MAXTICK: self.TICK=1
        else: self.TICK+=1
        self.player.set_state(Gst.State.READY)
        self.player.set_state(Gst.State.PLAYING)
        
        return True 
    
  def stop_sound(self):
    self.PLAYING = False
    self.player.set_state(Gst.State.NULL)
    return False






def main():
  Gst.init(sys.argv)
  app = Metronome()
  Gtk.main() 



if __name__ == '__main__':
  main()
