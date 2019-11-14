# Instruccinoes para obtener las credenciales para usar estos servicios:
# 1. Entrar a https://www.ibm.com/watson/services/text-to-speech/
# 2. Crear y validar una cuenta en "Get Started Free". Es gratis y no requiere tarjeta de crédito.
# 3. Ir a "Create resource" en el Dashboard, seleccionar "Speech To Text" (opción 500 min/month - Free) y confirmar.
# 4. Ir a "Create resource" en el Dashboard, seleccionar "Text To Speech" (opción 10000 chars/month - Free) y confirmar.
# 5. Ir a My Resources > Services > Speech to Text. En la página siguiente, copiar la API Key y la URL en IBM_services.py.
# 6. Ir a My Resources > Services > Text to Speech. En la página siguiente, copiar la API Key y la URL en IBM_services.py.

from ibm_watson import TextToSpeechV1, SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json

# Síntesis
tts_authenticator = IAMAuthenticator('**ACÁ VA LA API KEY DE TTS**')
tts = TextToSpeechV1(authenticator=tts_authenticator)
tts.set_service_url('**ACÁ VA LA URL DE TTS**')

with open('hello_world.wav', 'wb') as audio_file:
    audio_file.write(
        tts.synthesize(
            'Hello world',
            voice='en-US_AllisonVoice',
            accept='audio/wav'
        ).get_result().content)

# Reconocimiento
stt_authenticator = IAMAuthenticator('**ACÁ VA LA API KEY DE STT**')
stt = SpeechToTextV1(authenticator=stt_authenticator)
stt.set_service_url('**ACÁ VA LA URL DE STT**')

with open('hello_world.wav', 'rb') as audio_file:
    print(json.dumps(stt.recognize(audio=audio_file,
                                   content_type='audio/wav',
                                   timestamps=True,
                                   word_confidence=True).get_result(),
                     indent=2))

