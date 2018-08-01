class Stemmer(object):
    def __init__(self):
        self.vowels = 'aeiou'

    def is_consonant(self, letter: str) -> bool:
        # 判断字母是否为辅音
        if letter not in self.vowels:
            return True
        return False

    def is_vowel(self, letter: str) -> bool:
        # 判断字母是否为元音
        return not self.is_consonant(letter=letter)

    def consonant_in_word_by_index(self, word: str, index: int) -> bool:
        # 判断单词第index位是否为辅音
        letter = word[index]
        if self.is_consonant(letter=letter):
            if letter == 'y' and self.is_consonant(word[index-1]):
                return False
            return True
        return False

    def vowel_in_word_by_index(self, word: str, index: int) -> bool:
        # 判断单词第index位是否为元音
        return not self.consonant_in_word_by_index(word=word, index=index)

    def is_end_with(self, stem: str, letter='s') -> bool:
        # *s stem词干是否以s结尾
        if stem.endswith(letter):
            return True
        return False

    def is_end_with_double_same_consonants(self, stem: str)-> bool:
        # *d 判断词干以两个相同辅音结尾
        if len(stem) < 2:
            return False
        if stem[-1] != stem[-2]:
            return False
        if not (self.consonant_in_word_by_index(word=stem, index=-1) and
                self.consonant_in_word_by_index(word=stem, index=-2)):
            return False
        return True

    def vowel_in_word(self, stem: str)-> bool:
        # *v* 判断词干包含一个元音
        for letter in stem:
            if self.is_vowel(letter=letter):
                return True
        return False

    def get_form(self, word):
        # 根据word的元音和辅音组成返回VC序列
        form = str()
        for index in range(len(word)):
            if self.consonant_in_word_by_index(word=word, index=index):
                if index:
                    if not self.is_end_with(stem=form, letter='C'):
                        form += 'C'
                else:
                    form += 'C'
            else:
                if index:
                    if not self.is_end_with(stem=form, letter='V'):
                        form += 'V'
                else:
                    form += 'V'
        return form

    def get_m_count(self, word):
        # 获得单词中VC出现的次数
        return self.get_form(word=word).count('VC')

    def cvc(self, word):
        # *o  - 词干以cvc的形式结束, 但是第二个c（辅音）不是 W, X 或者Y
        if len(word) < 3:
            return False
        ignore = 'wxy'
        if self.consonant_in_word_by_index(word=word, index=-1) and \
                self.vowel_in_word_by_index(word=word, index=-2) and \
                self.consonant_in_word_by_index(word, index=-3):
            if word[-1] not in ignore:
                return True
            return False
        return False
