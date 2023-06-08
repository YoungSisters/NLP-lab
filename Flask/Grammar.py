#!/usr/bin/env python
# coding: utf-8

# In[2]:

import nltk
import re
import logging
import spacy
import string
import language_check
import nltk.data
from nltk.stem import WordNetLemmatizer as wnl
from flask import Flask, request, jsonify
from nltk import sent_tokenize
app = Flask(__name__)


class GrammarCheck:

    def __init__(self):
        self.error_list = []
        self.error_dic = dict()
        self.rule_dic = {'i': ['am', 'could', 'should', 'have', 'did', 'had', 'will', 'was', 'can', 'shall', 'may', 'might', 'must', 'would'],
                         'he': ['is', 'could', 'should', 'did',  'has', 'will', 'had', 'was', 'can', 'shall', 'may', 'might', 'must', 'would'],
                         'you': ['are', 'had', 'could', 'should', 'did',  'have', 'will', 'were', 'can', 'shall', 'may', 'might', 'must', 'would']
                         }
        self.tool = language_check.LanguageTool('en-US')
        self.lemmatizer = wnl()
        self.nlp = spacy.load('en')

        logging.basicConfig(filename="log_file.log", format='%(asctime)s %(message)s', filemode='w', level=logging.DEBUG)

    def clean_sentence(self, sentence):
        sen_split = sentence.split()

        temp_list = []
        [temp_list.append(i.lower()) if not i.islower() else temp_list.append(i) for i in sen_split]
        if 'customer' in temp_list or 'she' in temp_list or 'it' in temp_list:
            sentence = ' '.join('He' if x in ['Customer', 'She', 'It'] else 'he' if x in ['customer', 'she', 'it'] else x for x in sen_split)

        if 'they' in temp_list or 'we' in temp_list:
            sentence = ' '.join('you' if x in ['they', 'we'] else 'You' if x in ['They', 'We'] else x for x in sen_split)

        return sentence

    def end_with_punctuation(self, sentence):
        if not re.match(r'[\.?!]$', sentence[-1]):
            self.error_list.append("Every sentence should end with either of '.', '?' or '!'.")

    def noun_capitalise(self, sentence):
        sen_split = sentence.split()
        for word in sen_split:
            # removing the punctuation from the word extracted.
            word = word.translate(str.maketrans('', '', string.punctuation))
            if self.nlp(word)[0].tag_ in ['NNP', 'NNPS']:
                if word[0] != word[0].upper():
                    self.error_list.append("The noun '" + word.strip('.') + "' should be capitalised.")

    def hyphen_space(self, sentence):
        if '-' in sentence:
            if sentence[-1] == '-':
                self.error_list.append('Sentence should not end with "-".')
            elif sentence[sentence.find('-') - 1] == ' ' or sentence[sentence.find('-') + 1] == ' ':
                self.error_list.append("There shouldn't be any spaces before or after the '-' symbol.")

    def check_for_i(self, sentence):
        if sentence[-1] == '?':
            return

        sen_split = sentence.lower().split()
        text = nltk.word_tokenize(sentence)

        if sen_split[0] == 'i':

            if 'i' in sen_split:

                if len(sen_split) - sen_split.index("i") > 1:
                    next_word = sen_split[sen_split.index("i") + 1]  # the word next to 'I'

                    next_word_tag = self.nlp(next_word)[0].tag_  # the postag of the next word

                    if len(sen_split) - sen_split.index("i") >= 3:
                        if next_word in ['have', 'had']\
                                and sen_split[sen_split.index("i") + 2] not in ['not']\
                                and self.nlp(sen_split[sen_split.index("i") + 2])[0].tag_ not in ['VBD', 'VBN', 'DT', 'RB']:
                            self.error_list.append("With 'I have/had', second form of the verb should be used ("\
                                                   + sen_split[sen_split.index("i") + 2].strip('.')+ "), like played, gone.")

                    if len(sen_split) - sen_split.index("i") >= 4:
                        if next_word == 'have'\
                           and sen_split[sen_split.index("i") + 2] == 'been'\
                           and sen_split[sen_split.index("i") + 3][-3:] != 'ing'\
                           and self.nlp(sen_split[sen_split.index("i") + 3])[0].tag_ not in ['JJ', 'VBG', 'RB', 'IN', 'UH', 'VBN', 'VBD']:
                            self.error_list.append("With 'I have been', the verb form should be past tense\
                             or present participle ("+ sen_split[sen_split.index("i") + 3].strip('.')+"), like playing, gone." )

                    if next_word == 'been':
                        self.error_list.append("'been' cannot come after 'I'.")

                    if next_word[-3:] == 'ing':
                        self.error_list.append("Present participle form of the verb shouldn't be used ("+ next_word + ").")
                    
                    if next_word_tag not in ['NN', 'VBN', 'VB', 'VBD', 'NNS', 'VBP', 'JJ', 'IN', 'UH'] and next_word not in self.rule_dic['i']:
                        self.error_list.append("Wrong usage of 'I'. 'I' should be used with a verb (work, play, etc.) or modals (would, could, etc).")

                    if len(sen_split) - sen_split.index("i") > 2:

                        if sen_split[sen_split.index("i") + 2] == 'have'\
                                and sen_split[sen_split.index("i") + 3] == 'been'\
                                and self.nlp(next_word)[0].tag_ != "MD":
                            self.error_list.append('You should use modals (would, could, etc.) after the Pronoun here.')

                        if sen_split[sen_split.index("i") + 2] == 'been'\
                                and next_word not in ['have', 'had']:
                            self.error_list.append("You should use have or had after the pronoun here.")

                    if len(sen_split) - sen_split.index("i") >= 3:
                        if next_word in ['am', 'was']\
                           and self.nlp(sen_split[sen_split.index("i") + 2])[0].tag_ in ['NN', 'JJS' 'NNP']:
                           self.error_list.append("You should use a determiner (a, an, the, this, etc) before the Noun \
                           or Superlative adjective.")

                        if next_word in ['am', 'was']\
                                and self.nlp(sen_split[sen_split.index("i") + 2])[0].tag_ \
                                not in ['NN', 'RB', 'JJ', 'VBN', 'IN', 'DT', 'NNP', 'VBP', 'PRP$']\
                                and sen_split[sen_split.index("i") + 2][-3:] != 'ing':
                            self.error_list.append("Present or past participle form of the verb should be used ("\
                                                   + sen_split[sen_split.index("i") + 2].strip('.')+"), like playing, gone, etc.")

                        if len(sen_split) - sen_split.index("i") >= 5:
                            if sen_split[sen_split.index(next_word) + 2][-3:] != 'ing'\
                                    and self.nlp(sen_split[sen_split.index(next_word) + 3])[0].tag_ not in ['JJ', 'VBN', 'VBD']\
                                    and sen_split[sen_split.index("i") + 1] == 'have'\
                                    and sen_split[sen_split.index("i") + 2] == 'been':
                                self.error_list.append("With sentence formations like 'I have been' we use present or past participle \
                                form of the verb ("+sen_split[sen_split.index(next_word) + 3].strip('.')\
                                                       +") like, playing, done, gone, etc.")

                        if self.nlp(next_word)[0].tag_ == "MD":
                            if self.nlp(sen_split[sen_split.index(next_word) + 1])[0].tag_ not in ['NN', 'VBG', 'RB', 'VB']\
                                    and sen_split[sen_split.index(next_word) + 1] not in ['have', 'not']:
                                self.error_list.append("After 'I would', verb or adverb should be used like do, play, go, etc.")

                        if len(sen_split) - sen_split.index("i") >= 5:
                            if sen_split[sen_split.index(next_word) + 3][-3:] != 'ing'\
                                    and self.nlp(sen_split[sen_split.index(next_word) + 3])[0].tag_ not in ['VBG', 'JJ', 'VBN', 'VBD']\
                                    and sen_split[sen_split.index("i") + 2] == 'have'\
                                    and sen_split[sen_split.index("i") + 3] == 'been':
                                self.error_list.append("With sentence formations like 'I would have been' we use present\
                                 or past participle form of the verb ("+sen_split[sen_split.index(next_word) + 3].strip('.')\
                                                       + ") like, playing, gone, etc.")

    def check_for_he(self, sentence):
        if sentence[-1] == '?':
                return
            
        sen_split = sentence.lower().split()
        text = nltk.word_tokenize(sentence)

        if sen_split[0] == 'he':

            if 'he' in sen_split and len(sen_split) - sen_split.index("he") > 1:
                next_word = sen_split[sen_split.index("he") + 1]  # the word next to 'He'
                next_word_tag = self.nlp(next_word)[0].tag_  # the postag of the next word

                if next_word == 'been':
                    self.error_list.append("'been' should not be used here.")

                if next_word[-3:] == 'ing':
                    self.error_list.append("Present participle form of the verb shouldn't be used with the pronoun ("
                                           + next_word + "), like playing, singing, etc.")

                if next_word_tag not in ['NNS', 'VBZ', 'VBD', 'VBN', 'IN'] and next_word not in self.rule_dic['he']:
                    self.error_list.append("Pronoun should be used with a third form of verb like plays, works, etc,or modals like would, could, should, etc. (" + next_word+")")

                if len(sen_split) - sen_split.index("he") >= 2:
                    if next_word in ['has', 'had'] and sen_split[sen_split.index("he") + 2][-3:] != 'ing':
                        self.error_list.append("Second form of the verb should be used with has/had ("\
                                               + sen_split[sen_split.index("he") + 2].strip('.') + ") like plays, works, etc.")

                if len(sen_split) - sen_split.index("he") >= 4:
                    if sen_split[sen_split.index("he") + 2] == 'have'\
                            and sen_split[sen_split.index("he") + 3] == 'been'\
                            and self.nlp(next_word)[0].tag_ != "MD":
                        self.error_list.append('You should use modals after the pronoun like would, could, etc.')

                    if sen_split[sen_split.index("he") + 2] == 'been' and next_word not in ['has', 'had']:
                        self.error_list.append("One should use has or had.")

                    if len(sen_split) - sen_split.index("he") >= 4:
                        if sen_split[sen_split.index(next_word) + 2][-3:] != 'ing'\
                                and self.nlp(sen_split[sen_split.index(next_word) + 2])[0].tag_ \
                                not in ['JJ', 'VBG', 'RB', 'IN', 'UH', 'VBD', 'VBN']\
                                and sen_split[sen_split.index("he") + 1] in ['has', 'had']\
                                and sen_split[sen_split.index("he") + 2] == 'been':
                            self.error_list.append("Wrong form of the verb is used here ("\
                                                   + sen_split[sen_split.index(next_word) + 2].strip('.') + ").")
                            
                    if len(sen_split) - sen_split.index("he") >= 3:

                        if next_word in ['is', 'was']\
                                and self.nlp(sen_split[sen_split.index("he") + 2])[0].tag_ in ['NN', 'JJS', 'NNP']:
                            self.error_list.append("You should use a determiner before the Noun \
                            or Superlative adjective like a, an, the, this, etc.")

                        if next_word in ['is', 'was']\
                                and self.nlp(sen_split[sen_split.index("he") + 2])[0].tag_ \
                                not in ['JJ', 'VBG', 'UH', 'JJR', 'RB', 'PRP', 'PRP$', 'DT', 'IN', 'VBP', 'NN']\
                                and sen_split[sen_split.index("he") + 2][-3:] != 'ing':
                            self.error_list.append("The present or past participle form of the verb should be used ("
                                                   + sen_split[sen_split.index("he") + 2].strip('.') + ') like playing, done, etc.')

                        if self.nlp(next_word)[0].tag_ == "MD":

                            if self.nlp(sen_split[sen_split.index(next_word) + 1])[0].tag_ not in ['NN', 'VB', 'IN']\
                                    and sen_split[sen_split.index(next_word) + 1] not in ['have', 'not']:
                                self.error_list.append("After a pronoun followed by 'would', a verb or an adverb should be used ("
                                                       + sen_split[sen_split.index(next_word) + 1].strip('.')
                                                       + ") like sleep, see, etc.")

                            if len(sen_split) - sen_split.index("he") >= 5:
                                if sen_split[sen_split.index(next_word) + 3][-3:] != 'ing'\
                                        and self.nlp(sen_split[sen_split.index(next_word) + 3])[0].tag_ \
                                        not in ['JJ', 'VBG', 'RB', 'VBN', 'VBD']\
                                        and sen_split[sen_split.index("he") + 2] == 'have'\
                                        and sen_split[sen_split.index("he") + 3] == 'been'\
                                        and self.nlp(next_word)[0].tag_ == "MD":
                                    self.error_list.append("There is some mistake after the noun/pronoun and 'would have been' ("
                                                           + sen_split[sen_split.index(next_word) + 3].strip('.') + ").")

    def check_for_you(self, sentence):
        if sentence[-1] == '?':
            return

        sen_split = sentence.lower().split()
        text = nltk.word_tokenize(sentence)

        if sen_split[0] == 'you':

            if 'you' in sen_split and len(sen_split) - sen_split.index("you") > 1:'
                next_word = sen_split[sen_split.index("you") + 1]  # the word next to 'you'
                next_word_tag = self.nlp(next_word)[0].tag_  # the postag of the next word
                
                if next_word == 'been':
                    self.error_list.append("'been' cannot come after the pronoun/noun.")
                    
                if next_word[-3:] == 'ing':
                    self.error_list.append("Present participle form of the verb should NOT be used after the "
                                           "pronoun/noun ( "
                                           + next_word + ") like play, work.")

                if next_word_tag not in ['NN', 'VB', 'VBD', 'VBP', 'VBN', 'IN'] and next_word not in self.rule_dic['you']:
                    self.error_list.append("Pronouns/nouns should be used with a verb or modals ("
                                           + next_word + ") like you love, you sing.")

                if len(sen_split) - sen_split.index("you") >= 3:
                    if sen_split[sen_split.index("you") + 2] == 'have'\
                            and sen_split[sen_split.index("you") + 3] == 'been'\
                            and self.nlp(next_word)[0].tag_ != "MD":
                        self.error_list.append('You should use modals like would, could, etc here.')

                    if sen_split[sen_split.index("you") + 2] == 'been'\
                            and next_word not in ['have', 'had']:
                        self.error_list.append("You should use have or had after the pronoun.")

                    if next_word in ['are', 'were']\
                            and self.nlp(sen_split[sen_split.index("you") + 2])[0].tag_ \
                            not in ['JJ', 'VBG', 'UH', 'JJR', 'IN', 'VBN', 'RB', 'NNP', 'RB', 'DT', 'JJS']\
                            and sen_split[sen_split.index("you") + 2][-3:] != 'ing':
                        self.error_list.append("The present or past participle form of the verb should be used ("
                                               + sen_split[sen_split.index("you") + 2].strip('.') + ") like reading, "
                                                                                                    "gone, etc.")

                    if len(sen_split) - sen_split.index("you") >= 4:
                        if sen_split[sen_split.index(next_word) + 2][-3:] != 'ing'\
                                and self.nlp(sen_split[sen_split.index(next_word) + 2])[0].tag_ \
                                not in ['JJ', 'VBG', 'RB', 'IN', 'UH']\
                                and sen_split[sen_split.index("you") + 1] in ['have', 'had']\
                                and sen_split[sen_split.index("you") + 2] == 'been':
                            self.error_list.append("With sentence formations like 'you have been' we use present or "
                                                   "past participle form of the verb (" + sen_split[sen_split.index\
                                                    (next_word) + 2].strip('.') + ") like gone, singing.")

                    if len(sen_split) - sen_split.index("you") >= 3:
                        if self.nlp(next_word)[0].tag_ == "MD":
                            if self.nlp(sen_split[sen_split.index(next_word) + 1])[0].tag_ not in ['NN', 'VB']\
                                    and sen_split[sen_split.index(next_word) + 1] not in ['have', 'not']:
                                self.error_list.append("After 'you would', 'a noun, verb or adverb' is used ("\
                                                       + sen_split[sen_split.index(next_word) + 1].strip('.') + ").")

                            if len(sen_split) - sen_split.index("you") >= 5:
                                if sen_split[sen_split.index(next_word) + 3][-3:] != 'ing'\
                                        and self.nlp(sen_split[sen_split.index(next_word) + 3])[0].tag_ not in ['JJ', 'VBG']\
                                        and sen_split[sen_split.index("you") + 2] == 'have'\
                                        and sen_split[sen_split.index("you") + 3] == 'been'\
                                        and self.nlp(next_word)[0].tag_ == "MD":
                                    self.error_list.append("With sentence formations like 'you would have been'"
                                                           "we use present or past participle form of the verb ("
                                                           + sen_split[sen_split.index(next_word) + 3].strip
                                                               ('.') + ") like told, singing, gone, etc.")

    def using_grammar_check(self, sentence):
        matches = self.tool.check(sentence)
        if len(matches) > 0:
            for i in range(len(matches)):
                if matches[i].msg not in ['Possible typo: you repeated a whitespace', 'Add a space between sentences', 'Possible spelling mistake found']:
                    self.error_list.append(matches[i].msg)

    def etcetera_check(self, sentence):
        pattern = '\s?[a-z]+\s?,[,|\s|.]*'
        count = len(re.findall(pattern, sentence))
        if count == 1\
                and self.nlp(re.findall(pattern, sentence)[0].split(',')[0].strip('.'))[0].tag_ in ['NN', 'NNS', 'NNP', 'NNPS']\
                and 'etc' not in sentence\
                and 'and' not in sentence:
            self.error_list.append("Should have used 'and' here.")

        if count > 1\
                and self.nlp(re.findall(pattern, sentence)[0].split(',')[0].strip('.'))[0].tag_ in ['NN', 'NNS', 'NNP', 'NNPS']\
                and 'etc' not in sentence\
                and 'and' not in sentence:
            self.error_list.append('Should use "et cetera" between multiple nouns.')

    def grammar_check(self, sentence):
        self.error_dic = dict()
        sent = sent_tokenize(sentence)
        for s in sent:
            self.error_list = []
            self.using_grammar_check(s)
            sen = self.clean_sentence(s)
            try:
                self.check_for_you(sen)
                self.check_for_he(sen)
                self.check_for_i(sen)
                self.noun_capitalise(sen)
                # self.end_with_punctuation(sen)
                self.hyphen_space(sen)

            except Exception as e:
                logging.error("{} - {}".format(s, str(e)))
            logging.info("{} - {}".format(s,  ', '.join(self.error_list)))
            self.error_dic[s] = self.error_list

        return self.error_dic

a = GrammarCheck()

@app.route('/grammar/', methods=['POST'])
def grammar():
    content = request.json
    sentence = content['text']

    grammarCheck = a.grammar_check(sentence)
    return jsonify({"text": grammarCheck})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



