import jieba
import random
import re


class Markov(object):

    def __init__(self, open_file):
        self.cache = {}
        self.open_file = open_file
        self.sentences = self.file_to_sentence()
        self.sentence_size = len(self.sentences)
        self.database()


    def file_to_sentence(self):
        zh_puncmark = re.compile('[，。！；]')
        sentence_list = []
        with open(self.open_file, "r", encoding='utf-8') as f:
            for line in f.readlines():
                line = line.replace("\r", "").replace("\n", "").strip()
                if line == "" or line is None:
                    continue
                sentences = ' '.join(zh_puncmark.split(line))
                for sen in sentences.split(' '):
                    if sen:
                        sentence_list.append(sen)
        return sentence_list


    def triples(self):
        if len(self.sentences) < 3:
            return
        for i in range(len(self.sentences) - 2):
            yield (self.sentences[i], self.sentences[i + 1], self.sentences[i + 2])


    def database(self):
        for w1, w2, w3 in self.triples():
            key = (w1, w2)
            if key in self.cache:
                self.cache[key].append(w3)
            else:
                self.cache[key] = [w3]


    def generate_markov_text(self, size=100):
        seed = random.randint(0, self.sentence_size - 3)
        seed_word, next_word = self.sentences[seed], self.sentences[seed + 1]
        w1, w2 = seed_word, next_word

        gen_sentences = []
        for i in range(size):
            gen_sentences.append(w1)
            w1, w2 = w2, random.choice(self.cache[(w1, w2)])
        gen_sentences.append(w2)
        return ','.join(gen_sentences)


if __name__=='__main__':
    file = "./text.txt"
    markov = Markov(file)
    new_text = markov.generate_markov_text()
    print(new_text)