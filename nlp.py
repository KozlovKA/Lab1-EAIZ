import nltk
from nltk import word_tokenize
from pymorphy2 import MorphAnalyzer


def check_form(vocabulary, form, lemma):
    form_in_dict = vocabulary[lemma]['word_form']
    if form not in form_in_dict:
        vocabulary.update({form: 1})
    else:
        vocabulary[form]['count'] += 1


def wordize(sentences, **kwargs):
    list_word = []
    for sent in nltk.sent_tokenize(sentences.lower()):
        for word in nltk.word_tokenize(sent, **kwargs):
            if word != '.' and word != ',' and word != '?' and word != '!':
                list_word.append(word)
    return list_word



def parser(text):
    vocabulary = {}
    words = wordize(text)
    #words = word_tokenize(text, language='english')
    analyzer = MorphAnalyzer(lang='uk')
    # Finding part of sentence

    sentence_pos = nltk.pos_tag(words, lang='eng')

    for i in range(len(words)):
        parsed_words = analyzer.parse(words[i])
        word_lemma = parsed_words[0].normal_form
        word_form = parsed_words[0].word.lower()

        #word_tags = parsed_words[0].tag#.cyr_repr
        word_tags = sentence_pos[i][1]

        if word_lemma not in vocabulary:
            vocabulary.update({word_form: {'count': 1, 'word_form': word_form, 'tag': word_tags}})
        else:
            check_form(vocabulary, word_form, word_lemma)
            values = vocabulary.get(word_lemma)
            #values['count'] += 1
    return sorted(vocabulary.items(), key=lambda x: x[0])


if __name__ == '__main__':
    b = parser('Стали собакой')
    print(b)
