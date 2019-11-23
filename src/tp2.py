# https://pypi.python.org/pypi/pynput
from pynput import mouse
import recorder
import os
import sox   
from SpeechProcessor import SpeechProcessor


sp=SpeechProcessor()
recfile = None
grabando = False
numwav = 0

def procesar():
  res = sp.reconocer('audio_final.wav')
  print(res)

def on_click(x, y, button, pressed):
  global grabando, recfile, numwav
  
  # Presionar el botón izquierdo para empezar a grabar.
  if pressed and button==mouse.Button.left:
    if not grabando:
      print('Empieza grabacion')
      recfile = recorder.Recorder(channels=1).open('tmp/audio.wav', 'wb')
      grabando = True
      recfile.start_recording()
      #numwav += 1

  # Soltar el botón izquierdo para dejar de grabar.
  if not pressed and button==mouse.Button.left:
    if grabando:
      print('Termina grabacion')
      recfile.stop_recording()
    
    # create transformer
      tfm = sox.Transformer()
      tfm.convert(samplerate=16000, n_channels=1,bitdepth=16)
      tfm.build('tmp/audio.wav', 'tmp/audio_final.wav')
      recfile = None
      grabando = False
      procesar()
      #os.remove('tmp/audio.wav')

  # Presionar el botón derecho para terminar.
  if pressed and button==mouse.Button.right:
    if not grabando:
      return False


print("Presionar el botón izquierdo para empezar a grabar.")
print("Soltar el botón izquierdo para dejar de grabar.")
print("Presionar el botón derecho para terminar.")

with mouse.Listener(on_click=on_click) as listener:
  listener.join()

