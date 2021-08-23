# RUN_KLUE_DP
This code is for running Korean dependency parser using SOTA model and dataset.
It uses KLUE-DP dataset and dependency parser model with mecab-ko POS(Part-Of-Speech) tagging model.

이는 KLUE-DP 모델을 이용한 한글 구문 분석(Dependency parsing)을 쉽게 하기 위한 코드입니다.   
최근에 발표된 KLUE-DP 벤치마크 데이터셋과 KLUE-DP 논문에서 제안하는 모델을 이용하였으며, 문장 단위의 txt 파일만 입력값으로 넣으면 쉽게 사용할 수 있도록 일부 코드를 수정하였습니다.

+ 모델은 KLUE-DP benchmark 의 train data로 학습한 결과이며 **따로 학습시킬 필요가 없습니다!**
+ 기존 KLUE-DP의 모델은 추가 feature로 전문가가 직접 annotate한 input data의 형태소 분석 및 품사 태깅 값을 사용합니다. 따라서 일반적으로 사용할 수 있도록 **mecab-ko 모델을 이용하여 POS tagging 결과를 추가한 입력값**을 받도록 하였습니다.
+ 기존 KLUE-DP baseline model 이용시, input의 head값을 입력값으로 받는 부분을 수정하였습니다.



## Requirements
- mecab-ko
- torch==1.7.0
- transformers==4.5.1

## 실행방법
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
    

## output
output 폴더 내의 output.txt의 결과물 예시는 다음과 같다

```
## sentence_id	text
token_id	token	pos	head	dp
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
