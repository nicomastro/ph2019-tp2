# https://pypi.python.org/pypi/pynput
import psutil
from pynput import mouse
import recorder
import signal, os,time
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
import threading
from enum import Enum
from sox import core
from sox.core import SoxiError
from SpeechProcessor import SpeechProcessor
from subprocess import call
import alsaaudio
sp=SpeechProcessor()

recfile = None
grabando = False
numwav = 0
pid = -1
process=None
proc=None
playlist_process = None
playlist_proc = None
playlist_pid = -1
listando = 0
band = ""
vol = 70
playlist = None
playlist_on = False

# Instantiate PyAudio.





class Estados(Enum):
  Escuchando = 0
  Reproduciendo = 1
  Pausado = 2
  Listando = 3
  Playlisteando = 4

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
    print(p.get_default_output_device_info())
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

def terminar_reproduccion():
	global estado, playlist_proc, playlist_process, proc, process

	if estado == Estados.Pausado and playlist_on:
		playlist_proc.resume()
	elif estado == Estados.Pausado:
		proc.resume()

	if process != None:
		process.terminate()
		proc = None
		process = None
	elif playlist_process != None:
		playlist_proc.terminate()
		playlist_proc = None
		playlist_process = None

	return

def resample(rate,file):
  tfm = sox.Transformer()
  tfm.convert(samplerate=rate, n_channels=1,bitdepth=16)
  tfm.build(file+".wav", file+"_final.wav")
  return

def any_song(band):
	df = pd.read_csv('canciones/songs.csv',header = 0)
	song = str(df[df['artist'] == band].iloc[0][0])
	filename = re.sub(r" (\w+?)", r"_\1", song) + ".wav"
	return filename

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

  return msg
 

def pausar():
	global estado, Estados, process, proc, playlist_on
	msg = ""
	if estado == Estados.Reproduciendo or estado == Estados.Playlisteando:
		print("Pausando...")
		msg = "Pausado"
		if estado == Estados.Reproduciendo:
			if process != None:
				proc.suspend()
		elif estado == Estados.Playlisteando:
			playlist_on = True
			if playlist_process != None:
				playlist_proc.suspend()
		estado = Estados.Pausado
	else:
		print("No se puede pausar porque no está reproduciendo...")
		msg = "No se puede pausar porque no está reproduciendo"

	return msg

def controlar_volumen(sentido):
	m = alsaaudio.Mixer()
	vol = m.getvolume()[0]
	print(vol)
	vol = vol + 15*sentido
	if(vol <= 100 and vol >= 0):
		m.setvolume(vol)
	return

def proximo():
	global playlist_proc, playlist_process
	if playlist_process != None:
		playlist_process.terminate()
		playlist_process = None

def anterior():
	return

def continuar():
  global estado, Estados, process, proc
  msg = ""
  if estado == Estados.Pausado:
    print("Reanudando...")
    msg = "Reanudando"
    if(playlist_on):
        estado = Estados.Playlisteando
        if playlist_process != None:
           playlist_proc.resume()
    else:
        estado = Estados.Reproduciendo
        if process != None:
           proc.resume()
  else:
    print("No se puede reanudar porque no está pausado...")
    msg = "No se puede reanudar porque no está pausado"
    
  return msg

def reproducir_playlist():

	global playlist, playlist_proc, playlist_process, playlist_pid, estado 

	for song in playlist:

		playlist_process = Process(target=play_wav, args=('canciones/'+song, 1024))
		print(playlist_process)
		
		playlist_process.start()
		playlist_pid = playlist_process.pid
		playlist_proc = psutil.Process(playlist_pid)
		playlist_process.join()
		if estado == Estados.Reproduciendo:
			return

		print("aqui")

	msg = "No hay más canciones"
	playlist_proc = None
	playlist_process = None
	print(msg)
	#sintetizar
	estado = Estados.Escuchando
	return

def procesar(audioName = 'audio_final.wav'):
	global pid, estado, Estados, process, proc, listando, band,vol,playlist

	msg = ""
	song=""
	encontro = False
	cmd, res = sp.reconocer(audioName)
	str1 = resToString(res)

	print(cmd)
	if (re.search("poner|reproducir|poné", str1)):

		if (re.search("algo de|canción de|un tema de|temas de",str1)):
			listando = 0
			msg="Reproduciendo algo de"
			match = re.search("la renga|los redondos|épica|queen|bon jovi",str1)

			if(match):
				print("Reproduciendo...")
				encontro = True			
				estado = Estados.Reproduciendo
				banda = match.group(0)
				msg += banda
				song = any_song(banda) 

			else:
				encontro = False
				msg="No encontré la banda"

		elif(re.search("playlist",str1) and not estado == Estados.Playlisteando):

			terminar_reproduccion()

			if playlist != None and len(playlist) > 0:
				estado = Estados.Playlisteando
				t = threading.Thread(target=reproducir_playlist)
				t.start()
			else:
				msg = "No existe ninguna playlist"
				
		else:
			msg = "Reproduciendo "
			match = re.search("la bestia pop|el revelde|you give love a bad name|under pressure",str1)
			listando = 0
			if(match):
				encontro = True
				print("Reproduciendo...")
				estado = Estados.Reproduciendo
				msg += match.group(0)
				song = re.sub(r" (\w+?)", r"_\1", match.group(0)) + ".wav"		
			else:
				msg = "Lo siento, no pude encontrar lo que buscás"
				encontro = False

	elif re.search("detener|pausar", str1):
		msg = pausar()

	elif (re.search("continuar|reanudar",str1)):
		continuar()

	elif(re.search("próxima|siguiente",str1) and estado == Estados.Playlisteando):
		proximo()

	elif(re.search("anterior|previa",str1) and estado == Estados.Playlisteando):
		anterior()

	elif( re.search("listar|listá",str1)):

		terminar_reproduccion()

		estado = Estados.Escuchando

		match = re.search("queen|la renga|los redondos|bon jovi|épica",str1)
		if(match):
			band = match.group(0)
		msg = listar()

	elif(re.search("armar playlist|crear playlist",str1)):

		terminar_reproduccion()

		estado = Estados.Escuchando

		if(playlist == None):
			msg = "Comencemos. Diga agregar y el nombre de la primer cancion a agregar"
		else:
			msg = "Ya existe una playlist, será reemplazada. Diga agregar y el nombre de la primer cancion"
		playlist = []

	elif(re.search("agregar",str1) and not playlist == None):

		terminar_reproduccion()

		estado = Estados.Escuchando
		match = re.search("la bestia pop|el revelde|you give love a bad name|under pressure",str1)

		if (match):	
			
			if(playlist == []):
				msg = "Muy bien. Diga solamente el nombre de la próxima canción o bien terminar"
			else:
				msg = "Okay. ¿Próxima canción?"
			song = re.sub(r" (\w+?)", r"_\1", match.group(0)) + ".wav"	
			playlist.append(song)

		else:
			msg = "Lo siento. No encuentro esa canción."

	elif(re.search("terminar",str1) and estado == Estados.Escuchando and not playlist == []):
		msg = "Cuando quiera, puede reproducir su playlist."

	elif(re.search("si",str1) and listando):
		msg = listar()

	elif(re.search("no",str1) and listando):

		band = ""
		listando = 0
		Estados.Escuchando
		msg = "¡Entendido!"

	elif(re.search("aumentar volumen|subir volumen|subir",str1)):
		controlar_volumen(1)

	elif(re.search("bajar volumen|bajar",str1)):
		controlar_volumen(-1)

	else:
		print("No reconozco el comando...")
		msg = "No reconozco el comando. Pruebe listar, y luego, reproducir alguna de la lista."

	#if len(msg) > 0 and not (estado == Estados.Reproduciendo or estado == Estados.Playlisteando):
		#sp.sintetizar('tmp/salida.wav',msg)
		#resample(48000,'tmp/salida')  
		#play_wav('tmp/salida_final.wav')
		
	if encontro == True:
		terminar_reproduccion()
		if len(song) > 0:
		    process = Process(target=play_wav, args=('canciones/'+song, 1024))
		    process.start()
		    pid = process.pid
		    proc = psutil.Process(pid)

	print(msg)
	return

def on_click(x, y, button, pressed):
	global grabando, recfile, numwav

	# Presionar el botón izquierdo para empezar a grabar.
	if pressed and button==mouse.Button.left and not grabando:
		print('Empieza grabacion')
		recfile = recorder.Recorder(channels=1, rate=48000).open('tmp/audio.wav', 'wb')
		grabando = True
		recfile.start_recording()

	# Soltar el botón izquierdo para dejar de grabar.
	if not pressed and button==mouse.Button.left and grabando:
		print('Termina grabacion')
		recfile.stop_recording()
		recfile.close()
		resample(16000,'tmp/audio')
		recfile = None
		grabando = False
		procesar('audio_final.wav')
		return

def main():
	print("Presionar el botón izquierdo para empezar a grabar \n. Soltar el botón izquierdo para dejar de grabar.\n Presionar el botón derecho para terminar.")
	m = alsaaudio.Mixer()
	m.setvolume(vol)
	print(vol)
	with mouse.Listener(on_click=on_click) as listener:
	    listener.join()

if __name__== '__main__':
    main()

