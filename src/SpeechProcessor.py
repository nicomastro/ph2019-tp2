from ibm_watson import TextToSpeechV1, SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json
import os
from pocketsphinx import Pocketsphinx, get_model_path, get_data_path, Jsgf, FsgModel
from sphinxbase import *
DATADIR = "data/etc/"

class SpeechProcessor:
    def __init__(self, hmm='data/spanish/CIEMPIESS_Spanish_Models_581h/Models/modelo',
                       lm='data/spanish/CIEMPIESS_Spanish_Models_581h/Models/leng.lm.bin',
                       dict='data/spanish/CIEMPIESS_Spanish_Models_581h/Models/dicc.dic',
                       grammar='data/gramatica-tp2.gram', dataPath='tmp/'):
        self.data_path = dataPath
        config = {
            'hmm': hmm,
            'lm': lm,
            'dict': dict
        }
        #model_path = get_model_path()

        self.ps = Pocketsphinx(**config)
        
        # Switch to JSGF grammar
        jsgf = Jsgf(grammar)
        rule = jsgf.get_rule('tp2.grammar')
        fsg = jsgf.build_fsg(rule, self.ps.get_logmath(), 7.5)
        self.ps.set_fsg('tp2', fsg)
        self.ps.set_search('tp2')

        # Síntesis
        self.tts_authenticator = IAMAuthenticator('avYYGN5-aWqijOa1l-ftrUjX20KTE5tLZg1riiy-5HDX')
        self.tts = TextToSpeechV1(authenticator=self.tts_authenticator)
        self.tts.set_service_url('https://stream.watsonplatform.net/text-to-speech/api')


    def sintetizar(self, outFileName, msg):
        if len(msg) > 0:
            with open(outFileName, 'wb') as audio_file:
                audio_file.write(
                    self.tts.synthesize(
                        msg,
                        voice='es-LA_SofiaV3Voice',
                        accept='audio/wav'
                    ).get_result().content)

    def reconocer(self, inFileName='audio.wav'):
        # Reconocimiento
        print(self.data_path)
        self.ps.decode(
            audio_file=os.path.join(self.data_path,inFileName),
            buffer_size=2048,
            no_search=False,
            full_utt=False
        )
        return self.ps.segments(), self.ps.best(count=3)
            

