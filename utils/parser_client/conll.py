#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ConllStruct(object):

    def __init__(self, raw_conll):
        
        self.sentences = []
        self.raw_conll = raw_conll.strip()
        
        if self.raw_conll:

            raw_sentence = ""
            for line in raw_conll.split('\n'):

                if line.strip():
                    raw_sentence += line + '\n'

                elif raw_sentence:
                    sentence = ConllSentence(raw_sentence)
                    self.sentences.append(sentence)
                    raw_sentence = ""

        else:
            raise Exception('Empty conll!')

    def __iter__(self):
        return iter(self.sentences)

    def __repr__(self):
        return '\n\n'.join(map(repr, self.sentences))

class ConllSentence(object):

    def __init__(self, raw_sentence):

        self.tokens = {}
        self.token_list = []
        self.raw_sentence = raw_sentence.strip()
        
        if self.raw_sentence:
            self.raw_tokens = self.raw_sentence.split('\n')
            
            for raw_token in self.raw_tokens:
                token = ConllToken2009(raw_token)

                self.tokens[token.id] = token
                self.token_list.append(token)

        else:
            raise Exception('Empty conll sentence!')

    def __iter__(self):
        return iter(self.token_list)

    def __repr__(self):
        return '\n'.join(map(repr, self.token_list))

    def get_token(self, token_id):
        return self.tokens[token_id]


class ConllToken2009(object):

    def __init__(self, raw_token):

        if raw_token.strip():
            self.columns = raw_token.split('\t')

            self.id         = self.columns[0]
            self.form       = self.columns[1]
            self.lemma      = self.columns[2]
            self.plemma     = self.columns[3]
            self.pos        = self.columns[4]
            self.ppos       = self.columns[5]
            self.feat       = self.columns[6]
            self.pfeat      = self.columns[7]
            self.head       = self.columns[8]
            self.phead      = self.columns[9]
            self.deprel     = self.columns[10]
            self.pdeprel    = self.columns[11]
            self.fillpred   = self.columns[12]
            self.pred       = self.columns[13]

        else:
            raise Exception('Empty conll token!')

    def __repr__(self):
        return '\t'.join(self.columns)
    

