#!/usr/bin/env python
# coding: utf-8

# sentence text file -> pos tagging
# output = sentence\n token_id\t token\t pos\w

import MeCab
import sys
m = MeCab.Tagger()


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
            if pos in tok:
                pos_set +=' '+pos
                tag_set +='+'+tag
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
        tokens, poslist, taglist = pos_to_token(poses, text)
        g.write(gids % gid + text+'\n') # write gid with original sentence
        for tid, tok in enumerate(tokens):
            ws ='{}\t{}\t{}\t{}\t{}\t{}\n'.format(tid+1, tok, poslist[tid], taglist[tid], 0, 'NP')
            g.write(ws)
        gid +=1
        g.write('\n')
    f.close()
    g.close()


# In[ ]:


if __name__ == '__main__':
    make_file(sys.argv[1])

