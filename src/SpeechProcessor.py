import json
import os
from pocketsphinx import Pocketsphinx, get_model_path, get_data_path

class SpeechProcessor:
    def __init__(self, hmm='data/model_parameters/voxforge_es_sphinx.cd_ptm_4000', lm='data/etc/es-20k.lm', dict='data/etc/es.dict', dataPath='tmp/'):
        self.data_path = dataPath
        #config = {
        #    'hmm': hmm,
        #    'lm': lm,
        #    'dict': dict
        #}
        model_path = get_model_path()

        config = {
            'hmm': os.path.join(model_path, 'en-us'),
            'lm': os.path.join(model_path, 'en-us.lm.bin'),
            'dict': os.path.join(model_path, 'cmudict-en-us.dict')
        }

        self.ps = Pocketsphinx(**config)

    def sintetizar(self, outFileName, msg):
        pass

    def reconocer(self, inFileName='audio.wav'):
        # Reconocimiento
        self.ps.decode(
            audio_file=os.path.join(self.data_path,inFileName),
            buffer_size=2048,
            no_search=False,
            full_utt=False
        )

        return self.ps.best(count=1)
            

