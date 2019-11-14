# https://pypi.python.org/pypi/pynput
from pynput import mouse
import recorder

recfile = None
grabando = False
numwav = 0

def on_click(x, y, button, pressed):
  global grabando, recfile, numwav
  
  # Presionar el botón izquierdo para empezar a grabar.
  if pressed and button==mouse.Button.left:
    if not grabando:
      print('Empieza grabacion')
      recfile = recorder.Recorder(channels=2).open('audio'+str(numwav)+'.wav', 'wb')
      grabando = True
      recfile.start_recording()
      numwav += 1

  # Soltar el botón izquierdo para dejar de grabar.
  if not pressed and button==mouse.Button.left:
    if grabando:
      print('Termina grabacion')
      recfile.stop_recording()
      recfile = None
      grabando = False
      # Acá ya se podría hacer algo con el archivo creado.

  # Presionar el botón derecho para terminar.
  if pressed and button==mouse.Button.right:
    if not grabando:
      return False


print("Presionar el botón izquierdo para empezar a grabar.")
print("Soltar el botón izquierdo para dejar de grabar.")
print("Presionar el botón derecho para terminar.")

with mouse.Listener(on_click=on_click) as listener:
  listener.join()

