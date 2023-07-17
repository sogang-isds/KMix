import os
import argparse
import soundfile as sf
import pandas as pd
import glob
from tqdm import tqdm

NUMBER_OF_SECONDS = 3
RATE = 16000

parser = argparse.ArgumentParser()
parser.add_argument('--root_dir', type=str, required=False, default='/home/private_data/KoreanSpeech', help='Path to ksponspeech root directory')
parser.add_argument('--n_src', type=int, required=True)

def create_ksponspeech_metadata(subset, root_dir, args):
    wav_path, txt_path, subset = load_data(subset, root_dir)
    wav_path.sort()
    txt_path.sort()

    # extract speaker_ID
    speaker_ID = []
    print('extract {} speaker_ID ..'.format(subset))

    for i in tqdm(range(len(wav_path))):
        tmp_ID = wav_path[i].split('/')[-1]
        speaker_ID.append(tmp_ID)

    # extract length
    length = []
    print('extract {} length ..'.format(subset))

    for i in tqdm(range(len(wav_path))):
        tmp_len = len(sf.SoundFile(wav_path[i]))
        length.append(tmp_len)

    print('make {} metadata ..'.format(subset))

    txt_length = []
    for i in tqdm(range(len(txt_path))):
        with open(txt_path[i], encoding='utf-8') as f:
            tmp = f.readlines()[0]
            tmp = tmp.strip()
            tmp = len(tmp)
            txt_length.append(tmp)

    df = pd.DataFrame(columns=['speaker_ID', 'subset', 'length', 'origin_path', 'txt_path'])
    df['speaker_ID'] = speaker_ID
    df['subset'] = [subset] * len(wav_path)
    df['length'] = length
    df['origin_path'] = wav_path
    df['txt_path'] = txt_path
    df['txt_len'] = txt_length

    #text len 추가해서 30 음절 이상인 애들만 빼는 코드 추가
    # if subset != 'test-clean':
    #     df = df[df['txt_len'] >= 28]

    df = df[df['length'] >= NUMBER_OF_SECONDS * RATE]
    df = df.sort_values('length')

    # # 길이 긴 순서대로 남기기
    df = df.sort_values('txt_len', ascending=False)

    if subset == 'test-clean' or subset == 'dev-clean':
        df = df.iloc[:6000,:]
    else:
        if args.n_src == 2:
            df = df.iloc[:101600, :]
        elif args.n_src == 3:
            df = df.iloc[:101700, :]

    md_path = 'metadata'
    os.makedirs(md_path, exist_ok=True)

    kspon_path = md_path +'/KsponSpeech{}'.format(args.n_src)
    os.makedirs(kspon_path, exist_ok=True)
    save_path = os.path.join(kspon_path, subset + '.csv')
    df.to_csv(save_path, index=False)

def load_data(subset, root_dir):
    tmp = os.path.join(root_dir, subset)
    wav_path = glob.glob(tmp + '/*/*/*.wav')
    txt_path = glob.glob(tmp + '/*/*/KsponSpeech*.txt')

    return wav_path, txt_path, subset

def main(args):
    subset_name = ['dev-clean', 'test-clean', 'train-clean']
    root_dir = args.root_dir

    for i in range(len(subset_name)):
        create_ksponspeech_metadata(subset_name[i], root_dir, args)

if __name__=='__main__' :
    args = parser.parse_args()
    main(args)