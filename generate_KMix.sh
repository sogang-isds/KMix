#!/bin/bash
set -eu  # Exit on error
storage_dir=storage_dir
ksponspeech_dir=/home/private_data/KoreanSpeech
wham_dir=$storage_dir/wham_noise
kspon_outdir=$storage_dir/


function wham() {
	if ! test -e $wham_dir; then
		echo "Download wham_noise into $storage_dir"
		# If downloading stalls for more than 20s, relaunch from previous state.
		wget -c --tries=0 --read-timeout=20 https://storage.googleapis.com/whisper-public/wham_noise.zip -P $storage_dir
		unzip -qn $storage_dir/wham_noise.zip -d $storage_dir
		rm -rf $storage_dir/wham_noise.zip
	fi
}

wham &

wait

# Path to python
python_path=python

# If you wish to rerun this script in the future please comment this line out.
$python_path scripts/augment_train_noise.py --wham_dir $wham_dir

if test -d "metadata/wham_noise"; then
   echo "wham metadata directory already exists. Skipping generation."
else
   $python_path scripts/create_wham_metadata.py
fi

if test -d "metadata/KsponSpeech2"; then
   echo "KsponSpeech2 directory already exits. Skipping generation."
else
   $python_path scripts/create_KsponSpeech_metadata.py --n_src 2
fi

if test -d "metadata/KsponSpeech3"; then
   echo "KsponSpeech3 directory already exits. Skipping generation."
else
   $python_path scripts/create_KsponSpeech_metadata.py --n_src 3
fi

if test -d "metadata/Kspon3mix"; then
   echo "KMix folder already exits. Skipping generation."
else
   for n_src in 3; do
      $python_path scripts/create_kmix_metadata.py --n_src $n_src
   done
fi
      
for n_src in 2 3; do
  metadata_dir=metadata/Kspon
  $python_path scripts/create_kmix_from_metadata.py --kspon_dir $ksponspeech_dir \
    --wham_dir $wham_dir \
    --metadata_dir $metadata_dir \
    --kspon_outdir $kspon_outdir \
    --n_src $n_src \
    --freqs 8k 16k \
    --modes min max \
    --types mix_clean mix_both mix_single
done
