# Mecab_ko와 KLUE-DP 를 결합한 Korean Dependency Parser 모델
This code is for running Korean dependency parser using SOTA model and dataset.
It uses KLUE-DP dataset and dependency parser model with mecab-ko POS(Part-Of-Speech) tagging model.

이 코드는 KLUE-DP 모델을 이용한 한글 구문 분석(Dependency parsing)을 쉽게 하기 위한 코드입니다.   

KLUE는 2021년 한글 NLP의 발전을 위해 공개된 한글 benchmark dataset으로 동시에 이를 이용해 학습한 KLUE-BERT, KLUE-RoBERTa 를 기반으로 하는 pretrained language model(PLM) 과 총 8개의 nlp tasks를 해결할 수 있는 각각의 dataset과 model을 공개하였습니다.   

KLUE에서 코드를 공개하였으나, 아무나 모델을 학습시키고 구문 분석 결과를 사용하기는 어렵다고 생각되어, 공개된 여러 오픈 소스들을 일부 수정하고 결합하여, **python을 이용해 누구나 쉽게 최신 한글 모델을 이용한 한글 구문 분석을 할 수 있도록 만든 코드** 입니다.

KLUE-DP 벤치마크 데이터셋과 KLUE-DP 논문에서 제안하는 모델을 이용하였으며, 문장 단위의 txt 파일만 입력값으로 넣으면 쉽게 사용할 수 있도록 일부 코드를 수정하였습니다.

+ 모델은 KLUE-RoBERTa-base 모델을 기반으로 KLUE-DP benchmark 의 train data로 학습한 결과이며 **따로 학습시킬 필요가 없습니다!**
+ 기존 KLUE-DP의 모델은 추가 feature로 전문가가 직접 annotate한 input data의 형태소 분석 및 품사 태깅 값을 사용합니다. 따라서 일반적으로 사용할 수 있도록 **mecab-ko 모델을 이용하여 POS tagging 결과를 추가한 입력값**을 받도록 하였습니다.
+ 기존 KLUE-DP baseline model 이용시, input의 head값을 입력값으로 받는 부분을 수정하였습니다.



## Requirements
- mecab-ko
- torch==1.7.0
- transformers==4.5.1

## How to Run
1. mecab-ko를 설치
   - window에서는 한 번의 명령어로 설치하기 어려우며, 아래의 링크를 참조해 설치.
   - https://bitbucket.org/eunjeon/mecab-ko-dic/src/master/

2. dp-model.bin 을 아래의 링크에서 다운받아 run_klue_dp repository의 model 폴더 아래로 이동.
   - https://www.dropbox.com/s/n6zfylc69jr9c8f/dp-model.bin?dl=0

3. ```python pos_anal_mecab filename.txt``` 실행
    - filename 에 해당하는 파일은 분석하고자 하는 문장들이 포함된 text 파일로, txt format이며 문장당 \n로 구분되어 있어야 함.
    - 코드 실행시 output으로 동일한 filename의 tsv format의 파일 자동 생성(POS tagging 결과 포함)
    - pos tagging에는 mecab-ko를 이용하였으며, 주어진 KLUE-DP dataset에서의 정확도는 %임.

4. 해당 filename.tsv 를 data 폴더 아래로 이동

5. ```python inference.py --data_dir ./data --model_dir ./model --output_dir ./output --test_filename filename.tsv``` 실행
    - output/output.txt 로 결과물 저장.
    

## Output
output 폴더 내의 output.txt의 결과물 예시는 다음과 같다

```
## sentence_id	text
## 칼럼명 : token_id	token	pos	head	dp
## 0	'K팝스타3’ 유희열이 홍정희의 탈락에 눈물을 흘렸다.
1	'K팝스타3’	SS+SL+NNP+SN+SS	2	NP
2	유희열이	NNP+JKS	6	NP_SBJ
3	홍정희의	NNP+JKG	4	NP_MOD
4	탈락에	NNG+JKB	6	NP_AJT
5	눈물을	NNG+JKO	6	NP_OBJ
6	흘렸다.	VV+EP+EF+SF	0	VP

## 1	재판부는 검찰의 공정한 수사에 대한 신뢰가 깨져 버려 최씨와 김씨가 정신적 피해를 봤다는 점을 인정했다.
1	재판부는	NNG+JX	15	NP_SBJ
2	검찰의	NNG+JKG	4	NP_MOD
3	공정한	NNG+XSA+ETM	4	VP_MOD
4	수사에	NNG+JKB	5	NP_AJT
5	대한	VV+ETM	6	VP_MOD
6	신뢰가	NNG+JKS	7	NP_SBJ
7	깨져	VV+EC	8	VP
8	버려	VX+EC	13	VP
9	최씨와	NNP+NNB+JC	10	NP_CNJ
10	김씨가	NNP+NNB+JKS	13	NP_SBJ
11	정신적	NNG+XSN	12	NP
12	피해를	NNG+JKO	13	NP_OBJ
13	봤다는	VV+EP+ETM	14	VP_MOD
14	점을	NNG+JKO	15	NP_OBJ
15	인정했다.	NNG+XSV+EP+EF+SF	0	VP
```
- output.txt에는 문장의 token 단위로 분석이 되어있으며, 문장 앞에는 ## 과 sentence_id가 붙어있다.
- 여기서 token은 띄어쓰기 단위로 구분된 문장의 최소 단위인 어절을 의미한다.
- 문장의 text 다음에는 한 줄당(\n 구분), 토큰 번호(1부터 시작), 토큰, mecab-ko를 통한 pos tagging 결과, head의 토큰 번호(root의 경우 0),DP-label(string type) 가 적혀있다. (\t 로 구분)
- DP-label의 종류는 다음과 같다.
- dp_labels = [
     "NP",
     "NP_AJT",
     "VP",
     "NP_SBJ",
     "VP_MOD",
     "NP_OBJ",
     "AP",
     "NP_CNJ",
     "NP_MOD",
     "VNP",
     "DP",
     "VP_AJT",
     "VNP_MOD",
     "NP_CMP",
     "VP_SBJ",
     "VP_CMP",
     "VP_OBJ",
     "VNP_CMP",
     "AP_MOD",
     "X_AJT",
     "VP_CNJ",
     "VNP_AJT",
     "IP",
     "X",
     "X_SBJ",
     "VNP_OBJ",
     "VNP_SBJ",
     "X_OBJ",
     "AP_AJT",
     "L",
     "X_MOD",
     "X_CNJ",
     "VNP_CNJ",
     "X_CMP",
     "AP_CMP",
     "AP_SBJ",
     "R",
     "NP_SVJ",
 ]
 
## Evaluation
- evaluation dataset : KLUE-DP validation dataset을 이용하여 평가하였다.
   -  # of total sentences : 2000
   -  # of total tokens : 22496
   
-  Mecab-ko POS tagging 평가
   - KLUE-DP validation dataset 이용
   - KLUE에서 korean linguistics Ph.D. 가 직접 주석을 단 POS tagging 과 비교하였다.
   - 하나의 token은 여러개의 형태소(POS)로 구성된다.
   - 아래의 POS accuracy는 각 토큰당 tagging결과를 ground truth값을 비교한 정확도이며, 모든 pos tagging의 결과(개수, 숫서, 라벨)가 동일해야 정확하다고 판단하였다.
   - KLUE-DP 모델에서는 token(띄어쓰기 단위의 어절)의 마지막 POS 값만 이용하므로, Last POS accuracy(각 토큰의 마지막 형태소 분석 결과 정확도)가 이 DP 모델에 유의미한 값이다.
   - Last POS(per token) accuaracy : 94.03%
   - POS accuracy: 80.96%
   
- 기존 KLUE-DP : KLUE 논문에서 제안하는 대로 manually annotated POS tagging + KLUE-DP 모델
- Mecab-ko + KLUE-DP : 실사용하기 쉽도록 Mecab-ko를 이용해 POS tagging을 진행하고 KLUE-DP 모델 결합한 모델

- evaluation metrics 은 DP 모델 평가에 흔히 사용되는 UAS(Unlabeled Attachment Score)와 LAS(Labeled Attachment Score)를 이용한다.
   - UAS : Head(지배소) 예측 정확도
   - LAS : Head(지배소), Dependency Relation(의존 관계) 쌍의 예측 정확도

|Metrics|기존 KLUE-DP|Mecab-ko + KLUE+DP|
|:---|:---:|:---:|
|UAS|94.70%|94.67%|
|LAS|92.71%|92.67%|

- 기존 모델에 비해 성능차이가 크지 않음을 확인할 수 있다.



## 만든이
bb0711@kaist.ac.kr


## open-source
다음과 같은 open source code를 이용하였습니다.
- KLUE benchmark: https://github.com/KLUE-benchmark/KLUE
- KLUE-DP dataset & model:  https://klue-benchmark.com/tasks/71/overview/copyright
- KLUE-DP baseline model: https://aistages-prod-server-public.s3.amazonaws.com/app/Competitions/000071/data/klue-dp_code.tar.gz
- mecab-ko : https://bitbucket.org/eunjeon/mecab-ko-dic/src/master/

## License

This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />
