#!/usr/bin/env python
# coding: utf-8

# sentence text file -> pos tagging
# output = sentence\n token_id\t token\t pos\w

import MeCab
import sys
m = MeCab.Tagger()

# 품사태깅(pos tagging) 결과를 mecab-ko 품사 태깅에서 klue에서 사용한 품사 분류 기준으로 변경
# klue의 품사 태깅 기준 : https://aiopen.etri.re.kr/data/001.%ED%98%95%ED%83%9C%EC%86%8C%EB%B6%84%EC%84%9D_%EA%B0%80%EC%9D%B4%EB%93%9C%EB%9D%BC%EC%9D%B8.pdf
def pos_mecab_to_klue(pos,tag):
    mmd = ['이','그','저','요','고','조','이런','저런','그런','다른','어느','무슨','웬','옛','올','현','구','전','후','래']
    mmn = ['한','두','세','석','서','네','넉','너','다섯','닷','엿','일곱','여덟','아홉','열','스무','스물','째','제','몇몇','여러']
    if tag == 'NNBC':
        tag = 'NNB'
    elif tag == 'UNKNOWN':
        tag = 'NA'
    elif tag == 'SSO' or tag == 'SSC':
        tag = 'SS'
    elif tag == 'SC':
        tag = 'SP'
    elif tag =='SY':
        if '~' in pos: # ~ 인경우 SO
            tag ='SO'
        else:
            tag = 'SW'
    elif tag == 'MM': # MM 관형사 인경우, 위 참조 자료에 해당하는 예제를 보고 직접 분류
        if pos in mmd:
            tag = 'MMD'
        else:
            for ex in mmn:
                if ex in pos:
                    tag ='MMN'
                    return (pos, tag)
            tag = 'MMA'
    
    return (pos, tag)

# 한 문장 -> (형태소, 형태소 종류) 분석 결과 리스트
def parse_mecab_str(tagger, text):
    out = tagger.parse(text).split('\n')
    tups = []
    for i in out[:-2] :# EOS 제외
        name,tag = i.split('\t')[0],i.split('\t')[1].split(',')[0]
        tups.append((name,tag))
    return tups

# 한 토큰 당 형태소 분석 결과물 저장
# ex: [('이것', 'NP'),('은', 'JX')] -> [('이것은','이것 은', 'NP+JX')] 
def pos_to_token(poses, text): 
    tokens = text.split(' ')
    poslist = []
    taglist = []
    for tok in tokens:
        pos_set = ''
        tag_set = ''
        while len(poses)> 0:
            pos, tag = poses.pop(0)
            if pos == tok[:len(pos)]:
                pos_set +=' '+pos
                tag_set +='+'+tag
                tok = tok[len(pos):]
            else:
                poses.insert(0,(pos,tag))
                break
        poslist.append(pos_set.strip())
        
        if tag_set[0]=='+':
            tag_set = tag_set[1:]
        taglist.append(tag_set)
    return tokens, poslist, taglist

# read .txt file and convert to .tsv file which has klue-dp's input form
def make_file(file):
    f = open(file, 'rt', encoding='UTF8')
    g = open(file.replace('.txt','.tsv'), 'w', encoding='UTF8')
    head = '## 칼럼명 : INDEX	WORD_FORM	LEMMA	POS	HEAD	DEPREL\n'
    gid = 0
    gids = '## klue-dp-eval_%06d	'
    g.write(head)

    writes =[]
    while True:
        line = f.readline()
        if not line: break
        text = line.strip()
        poses = parse_mecab_str(m, text)
        poses = [pos_mecab_to_klue(p,t) for p,t in poses]
        tokens, poslist, taglist = pos_to_token(poses, text)
        g.write(gids % gid + text+'\n') # write gid with original sentence
        for tid, tok in enumerate(tokens):
            ws ='{}\t{}\t{}\t{}\t{}\t{}\n'.format(tid+1, tok, poslist[tid], taglist[tid], 0, 'NP')
            g.write(ws)
        gid +=1
        g.write('\n')
    f.close()
    g.close()


if __name__ == '__main__':
    make_file(sys.argv[1])

