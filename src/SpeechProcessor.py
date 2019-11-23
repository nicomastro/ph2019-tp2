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
        self.ps = Pocketsphinx(**config)
        # Switch to JSGF grammar
        jsgf = Jsgf('data/etc/gramatica-tp2.gram')
        rule = jsgf.get_rule('tp2.grammar')
        fsg = jsgf.build_fsg(rule, self.ps.get_logmath(), 7.5)
        self.ps.set_fsg('tp2', fsg)
        self.ps.set_search('tp2')


    def sintetizar(self, outFileName, msg):
        pass

    def reconocer(self, inFileName='audio.wav'):
        # Reconocimiento
        self.ps.decode(
            audio_file=os.path.join(self.data_path,inFileName),
            buffer_size=512,
            no_search=False,
            full_utt=False
        )

        return self.ps.best(count=3)
            

