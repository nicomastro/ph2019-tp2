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
from sox import core
from sox.core import SoxiError
from SpeechProcessor import SpeechProcessor

sp=SpeechProcessor()
recfile = None
grabando = False
numwav = 0
pid = -1


#la reproduccion con esta funcion se escucha un poco raro, hasta ahora es la unica alternativa que me funciono "bien"
def play_wav(wav_filename, chunk_size=1024):
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
        return
    except EOFError as eofe:
        sys.stderr.write('EOFError on file ' + wav_filename + '\n' + \
        str(eofe) + '. Skipping.\n')
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

def procesar():
  global pid
  cmd, res = sp.reconocer('audio_final.wav')
  str1 = ''.join(cmd)
  print(str1)
  print(cmd)
  print(res)
  
  if (re.search("poner|reproducir", str1)):
    print("Reproduciendo...")
    pid = os.fork()
    if(pid == 0):
      print("El revelde:")
      play_wav('data/songs/el_revelde.wav')
      os._exit(os.EX_OK)
    else:
      print(pid)
  elif (re.search("detener|pausar", str1)):
    print("Pausando...")
    os.kill(pid, signal.SIGSTOP)
  elif (re.search("continuar|reanudar",str1)):
    print("Reanudando...")
    os.kill(pid, signal.SIGCONT)

  return

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
      recfile.close()
    
    # create transformer
      tfm = sox.Transformer()
      tfm.convert(samplerate=16000, n_channels=1,bitdepth=16)
      tfm.build('tmp/audio.wav', 'tmp/audio_final.wav')
      recfile = None
      grabando = False
      procesar()
      #os.remove('tmp/audio.wav')

  # Presionar el botón derecho para terminar.
  #if pressed and button==mouse.Button.right:
  #  if not grabando:
  #    return False
      return


print("Presionar el botón izquierdo para empezar a grabar.")
print("Soltar el botón izquierdo para dejar de grabar.")
print("Presionar el botón derecho para terminar.")


with mouse.Listener(on_click=on_click) as listener:
  listener.join()

