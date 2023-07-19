# KMix
한국어 자유환경 발화 데이터셋인 Ksponspeech와 Wham! noise를 활용하여 제작한 소음 환경 중첩음 데이터셋 생성 SW입니다.



#### KsponSpeech 

(paper) https://www.mdpi.com/2076-3417/10/19/6936 

(github) https://github.com/sooftware/ksponspeech

#### Wham! 

(paper) : https://arxiv.org/pdf/1907.01160.pdf

(site) : https://wham.whisper.ai/



## train/dev/eval

- Ksponspeech의 경우, train/dev/eval set이 분리되어 있지 않아 코퍼스를 나누는 과정을 거쳤습니다.
- 위 과정에서 flac 확장자를 wav로 변환하여 활용하였습니다.
- single channel seperation task 수행을 위해서 stero -> mono 변환을 진행했습니다.

```bash
#폴더 트리 구조

KsponSpeech/
	train/
	  KsponSpeech_01 (0001~0124)/
	  KsponSpeech_02 (0125~0186, 0202~0248)/
	  KsponSpeech_03 (0249~0372)/
	  KsponSpeech_04 (0373~0434, 0450~0496)/
	  KsponSpeech_05 (0497~0623)/
	dev/
	  KsponSpeech_02 (0187~0201)
	test/
	  KsponSpeech_04 (0435~0449)
```



## How To Use

```bash
cd KMix
pip install -r requirements.txt
./generate_KMix.sh
```

- KsponSpeech default directory는 /home/private_data/* 입니다.
- 경로 변경이 필요할 경우, **generate_KMix.sh** 내 **ksponspeech_dir** argument를 수정하시면 됩니다.
- 실행이 완료되면 KMix/storage_dir 내 wham_noise 및 Kspon(2,3)mix data가 생성됩니다.

