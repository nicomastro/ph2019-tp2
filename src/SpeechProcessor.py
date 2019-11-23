import json
import os
from pocketsphinx import Pocketsphinx, get_model_path, get_data_path, Jsgf, FsgModel
from sphinxbase import *
DATADIR = "data/etc/"

class SpeechProcessor:
    def __init__(self, hmm='data/model_parameters/voxforge_es_sphinx.cd_ptm_4000', lm='data/etc/es-20k.lm',dict='data/etc/es.dict', dataPath='tmp/'):
        self.data_path = dataPath
        config = {
            'hmm': hmm,
            'lm': lm,
            'dict': dict,
        }
    	#model_path = get_model_path()
    	#config = {
    	#    'hmm': os.path.join(model_path, 'en-us'),
    	#    'lm': os.path.join(model_path, 'en-us.lm.bin'),
    	#    'dict': os.path.join(model_path, 'cmudict-en-us.dict')
    	#}

        self.ps = Pocketsphinx(**config)
        # Switch to JSGF grammar
        jsgf = Jsgf('data/etc/gramatica-hola-mundo.gram')
        rule = jsgf.get_rule('hola_mundo.grammar')
        fsg = jsgf.build_fsg(rule, self.ps.get_logmath(), 7.5)
        self.ps.set_fsg('hola_mundo', fsg)
        self.ps.set_search('hola_mundo')


    def sintetizar(self, outFileName, msg):
        pass

    def reconocer(self, inFileName='audio.wav'):
        # Reconocimiento
        print(self.data_path)
        self.ps.decode(
            audio_file=os.path.join(self.data_path,inFileName),
            buffer_size=2048,
            no_search=False,
            full_utt=False
        )

        return self.ps.best(count=3)
            

