import subprocess
from utils import count_lines_fast

def generate_data_size_experiments():
    name_template = 'train-lstm-wsd-{percent:02d}pc-data-google-model.job'
    content_template = '''#!/bin/bash
#SBATCH --time=720:00:00
#SBATCH -C TitanX
#SBATCH --gres=gpu:1

module load cuda80/toolkit
module load cuda80/blas
module load cuda80
module load cuDNN

echo -n 'Started: ' && date

head -n {num_lines} output/gigaword.txt > output/gigaword_{percent:02d}pc.txt && \\
        python3 -u prepare-lstm-wsd.py output/gigaword_{percent:02d}pc.txt \\
                                       output/gigaword_{percent:02d}pc-lstm-wsd && \\
        python3 -u train-lstm-wsd.py --model google \\
                                     --data_path output/gigaword_{percent:02d}pc-lstm-wsd \\
                                     --save_path output/lstm-wsd-google_trained_on_gigaword_{percent:02d}pc

echo -n 'Finished: ' && date
'''
    total_lines = count_lines_fast('output/gigaword.txt')
    for percent in (1, 10, 50, 75):
        num_lines = int(percent / 100.0 * total_lines)
        fname = name_template.format(**locals())
        if os.path.exists(fname):
            print('File %s already exists. Ignored.' %fname)
        else:
            with open(fname, 'w') as f_script:
                f_script.write(content_template.format(**locals()))
            subprocess.call('chmod a+x %s' %fname, shell=True)

if __name__ == '__main__':
    generate_data_size_experiments()