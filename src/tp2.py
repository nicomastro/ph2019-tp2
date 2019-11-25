# https://pypi.python.org/pypi/pynput
from pynput import mouse
import recorder
import signal, os
import sox   
#import simpleaudio as sa
#from playsound import playsound
#import simpleaudio.functionchecks as fc
import re
import pyaudio
import wave
import sys
from multiprocessing import Process
from enum import Enum
from sox import core
from sox.core import SoxiError
from SpeechProcessor import SpeechProcessor

sp=SpeechProcessor()
recfile = None
grabando = False
numwav = 0
pid = -1
process=None

class Estados(Enum):
  Escuchando = 0
  Reproduciendo = 1
  Pausado = 2

estado = Estados.Escuchando


#la reproduccion con esta funcion se escucha un poco raro, hasta ahora es la unica alternativa que me funciono "bien"
def play_wav(wav_filename, chunk_size=1024):
    global estado, Estados
    '''
    Play (on the attached system sound device) the WAV file
    named wav_filename.
    '''
    try:
        print('Trying to play file ' + wav_filename)
        wf = wave.open(wav_filename, 'rb')
    except IOError as ioe:
        sys.stderr.write('IOError on file ' + wav_filename + '\n' + \
        str(ioe) + '. Skipping.\n')
        estado = Estados.Escuchando
        return
    except EOFError as eofe:
        sys.stderr.write('EOFError on file ' + wav_filename + '\n' + \
        str(eofe) + '. Skipping.\n')
        estado = Estados.Escuchando
        return

    # Instantiate PyAudio.
    p = pyaudio.PyAudio()

    # Open stream.
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(chunk_size)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(chunk_size)

    # Stop stream.
    stream.stop_stream()
    stream.close()

    # Close PyAudio.
    p.terminate()

    estado = Estados.Escuchando

def resToString(res):
  if len(res) > 0:
    ret = [str(t[0])+ "," for t in res]
    return ''.join(ret)
  else:
    return ''

def procesar(audioName = 'audio_final.wav'):
  global pid, estado, Estados, process
  cmd, res = sp.reconocer(audioName)
  #str1 = ''.join(res)

  print(cmd)
  print(res)
  str1 = resToString(res)
  print(str1)
  msg = ""
  song=""
  
  if (re.search("poner|reproducir|poné", str1)):
    encontro = True
    if re.search("algo de|canción de",str1):
      if re.search("la renga|los redondos|épica|queen",str1):
        print("Reproduciendo...")
        msg = "Reproduciendo"
        if re.search("la renga",str1):
            msg = msg + " la renga"
        elif re.search("los redondos",str1):
            msg = msg + " los redondos"
        elif re.search("épica",str1):
            msg = msg + " épica"
        else:
            msg = msg + " cuin"
        estado = Estados.Reproduciendo
      else:
        encontro = False
    elif re.search("la bestia pop|el revelde | you give love a bad name",str1):
      print("Reproduciendo...")
      msg = "Reproduciendo"
      if re.search("la bestia pop",str1):
        msg = msg + " la bestia pop"
      elif re.search("you give love a bad name",str1):
        msg = msg + " iu guiv lov e bad neim"
        song="You_give_love_a_bad_name.mp3"
      else:
        msg = msg + " el revelde"
      estado = Estados.Reproduciendo
    else:
      encontro = False
    if encontro == True:
      #pid = os.fork()
      #if(pid == 0):
      if process != None:
        process.terminate()
        process.close()
      process = Process(target=play_wav, args=('canciones/'+song))
      process.start()
      print("Encontró:")
      #msg = "Reproduciendo"
        #play_wav('data/songs/el_revelde.wav')
        #os._exit(os.EX_OK)
      #else:
      #  print(pid)
    else:
      print("No Encontró:")
      msg = "No se encontró lo buscado"
  elif re.search("detener|pausar", str1):
    if estado == Estados.Reproduciendo:
      print("Pausando...")
      msg = "Pausando"
      estado = Estados.Pausado
      #os.kill(pid, signal.SIGSTOP)
    else:
      print("No se puede pausar porque no está reproduciendo...")
      msg = "No se puede pausar porque no está reproduciendo"
  elif (re.search("continuar|reanudar",str1)):
    if estado == Estados.Pausado:
      print("Reanudando...")
      msg = "Reanudando"
      estado = Estados.Reproduciendo
      #os.kill(pid, signal.SIGCONT)
    else:
      print("No se puede reanudar porque no está pausado...")
      msg = "No se puede reanudar porque no está pausado"
  else:
    print("No reconoce comando...")
    msg = "No reconoce comando"

  sp.sintetizar('tmp/salida.wav',msg)
  #if process != None:
  #  process.terminate()
  #  process.close()
  #process = Process(target=play_wav, args=('tmp/salida.wav'))
  #process.start()
  play_wav('tmp/salida.wav')
  return

def on_click(x, y, button, pressed):
  global grabando, recfile, numwav
  
  # Presionar el botón izquierdo para empezar a grabar.
  if pressed and button==mouse.Button.left:
    if not grabando:
      print('Empieza grabacion')
      recfile = recorder.Recorder(channels=1, rate=16000).open('tmp/audio.wav', 'wb')
      grabando = True
      recfile.start_recording()
      #numwav += 1

  # Soltar el botón izquierdo para dejar de grabar.
  if not pressed and button==mouse.Button.left:
    if grabando:
      print('Termina grabacion')
      recfile.stop_recording()
      recfile.close()
    # create transformer
      #tfm = sox.Transformer()
      #tfm.convert(samplerate=16000, n_channels=1,bitdepth=16)
      #tfm.build('tmp/audio.wav', 'tmp/audio_final.wav')
      recfile = None
      grabando = False
      procesar('audio.wav')
      #os.remove('tmp/audio.wav')
      #os.remove('tmp/audio_final.wav')

  # Presionar el botón derecho para terminar.
  if pressed and button==mouse.Button.right:
    if not grabando:
      return False
      #return


print("Presionar el botón izquierdo para empezar a grabar.")
print("Soltar el botón izquierdo para dejar de grabar.")
print("Presionar el botón derecho para terminar.")


with mouse.Listener(on_click=on_click) as listener:
  listener.join()

