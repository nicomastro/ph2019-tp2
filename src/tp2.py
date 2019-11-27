# https://pypi.python.org/pypi/pynput
import psutil
from pynput import mouse
import recorder
import signal, os
import sox
import pandas as pd
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
proc=None
listando = 0
band = ""

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

    #estado = Estados.Escuchando

def resToString(res):
  if len(res) > 0:
    ret = [str(t[0])+ "," for t in res]
    return ''.join(ret)
  else:
    return ''

def resample(rate,file):
  tfm = sox.Transformer()
  tfm.convert(samplerate=rate, n_channels=1,bitdepth=16)
  tfm.build(file+".wav", file+"_final.wav")
  return
 
def listar():
  global listando, band

  df = pd.read_csv('canciones/songs.csv',header = 0)
  item = ""
  msg = ""
  if(band != ""):
    df = df[df['artist'] == band] 
    item = "canciones de "
  if(not(listando)):
    msg = "Se encontraron" + str(df.shape[0]) + item + band + ". Algunas de ellas son:"
  
  msg += df.iloc[listando:listando+2].to_string(index=False,index_names=False,header=False,columns=['song'])
  listando += 2
  if(listando< df.shape[0]):
    if(listando==2):
      msg+= ". ¿Desea continuar listando más canciones?"
    else:
      msg+=". ¿Sigo?"
  else:
    listando = 0
    band = ""
  
  print(msg)
  return msg

def procesar(audioName = 'audio_final.wav'):
  global pid, estado, Estados, process, proc
  cmd, res = sp.reconocer(audioName)
  #str1 = ''.join(res)

  print(cmd)
  print(res)
  str1 = resToString(res)
  print(str1)
  msg = ""
  song=""
  encontro = False
  if (re.search("poner|reproducir|poné", str1)):
    encontro = True
    msg="Reproduciendo"
    if re.search("algo de|canción de|canciones de|un tema de|temas de",str1):
      msg=msg + " algo de"
      if re.search("la renga|los redondos|épica|queen|bon jovi",str1):
        print("Reproduciendo...")
        if re.search("la renga",str1):
            msg = msg + " la renga"
        elif re.search("los redondos",str1):
            msg = msg + " los redondos"
        elif re.search("épica",str1):
            msg = msg + " épica"
            song="Cry_for_the_Moon.wav"
        elif re.search("bon jovi",str1):
            msg = msg + "bon shobi"
            song="You_give_love_a_bad_name.wav"
        else:
            msg = msg + " cuin"
            song="Under_Pressure.wav"
        estado = Estados.Reproduciendo
      else:
        encontro = False
    elif re.search("la bestia pop|el revelde|you give love a bad name",str1):
      print("Reproduciendo...")
      if re.search("la bestia pop",str1):
        msg = msg + " la bestia pop"
      elif re.search("you give love a bad name",str1):
        msg = msg + " iu guiv lov e bad neim"
        song="You_give_love_a_bad_name.wav"
      else:
        msg = msg + " el revelde"
      estado = Estados.Reproduciendo
    else:
      encontro = False

    if encontro == True:
      print("Encontró:")
    else:
      print("No Encontró:")
      msg = "No se encontró lo buscado"
  elif re.search("detener|pausar", str1):
    if estado == Estados.Reproduciendo:
      print("Pausando...")
      msg = "Pausando"
      estado = Estados.Pausado
      if process != None:
        proc.suspend()
      #os.kill(pid, signal.SIGSTOP)
    else:
      print("No se puede pausar porque no está reproduciendo...")
      msg = "No se puede pausar porque no está reproduciendo"
  elif (re.search("continuar|reanudar",str1)):
    if estado == Estados.Pausado:
      print("Reanudando...")
      msg = "Reanudando"
      estado = Estados.Reproduciendo
      if process != None:
        proc.resume()
      #os.kill(pid, signal.SIGCONT)
    else:
      print("No se puede reanudar porque no está pausado...")
      msg = "No se puede reanudar porque no está pausado"
  elif( re.search("listar|listá",str1)):
    match = re.search("queen|la renga|los redondos|bon jovi",str1)
    if(match):
      band = match[0]
    msg = listar()
  elif(re.search("si",str1) and listando):
    msg = listar()
  elif(re.search("no",str1) and listando):
    band = ""
    listando = 0
    msg = "¡Entendido!"
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
  
  if encontro == True:
    if process != None:
        process.terminate()
    if len(song) > 0:
        process = Process(target=play_wav, args=('canciones/'+song, 1024))
        process.start()
        pid = process.pid
        proc = psutil.Process(pid)
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


def main():
    print("Presionar el botón izquierdo para empezar a grabar.")
    print("Soltar el botón izquierdo para dejar de grabar.")
    print("Presionar el botón derecho para terminar.")
    
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

if __name__== '__main__':
    main()

