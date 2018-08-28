from .static import static


class Stemmer(object):
    def __init__(self):
        self.vowels = 'aeiou'
        self.cvc_ignore = 'wxy'

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
            if letter == 'y' and self.is_consonant(word[index - 1]):
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

    def is_end_with_double_same_consonants(self, stem: str) -> bool:
        # *d 判断词干以两个相同辅音结尾
        if len(stem) < 2:
            return False
        if stem[-1] != stem[-2]:
            return False
        if not (self.consonant_in_word_by_index(word=stem, index=-1)
                and self.consonant_in_word_by_index(word=stem, index=-2)):
            return False
        return True

    def vowel_in_word(self, stem: str) -> bool:
        # *v* 判断词干包含一个元音
        for letter in stem:
            if self.is_vowel(letter=letter):
                return True
        return False

    def get_form(self, word: str) -> str:
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

    def get_m_count(self, word: str) -> int:
        # 获得单词中VC出现的次数
        return self.get_form(word=word).count('VC')

    def cvc(self, word: str) -> bool:
        # *o  - 判断词干是否以以cvc的形式结束, 但是第二个C（辅音）不是 W, X 或者Y
        if len(word) < 3:
            return False
        if self.consonant_in_word_by_index(word=word, index=-1) and \
                self.vowel_in_word_by_index(word=word, index=-2) and \
                self.consonant_in_word_by_index(word, index=-3):
            if word[-1] not in self.cvc_ignore:
                return True
            return False
        return False

    def replace(self, origin: str, rem: str, rep: str, m=None) -> str:
        # 将输入的origin单词后缀替换
        if m is None:
            return origin[:origin.rfind(rem)] + rep
        else:
            base = origin[:origin.rfind(rem)]
            if self.get_m_count(word=base) > m:
                return base + rep
            else:
                return origin

    def stem(self, word: str) -> str:
        if word.endswith('sses'):
            word = self.replace(origin=word, rem='sess', rep='ss')
        elif word.endswith('ies'):
            word = self.replace(origin=word, rem='ies', rep='i')
        elif word.endswith('ss'):
            word = self.replace(origin=word, rem='ss', rep='ss')
        elif word.endswith('s'):
            word = self.replace(origin=word, rem='s', rep='')

        flag = False
        if word.endswith('eed'):
            base = word[:word.rfind('edd')]
            if self.get_m_count(word=base):
                word = base + 'ee'
        elif word.endswith('ed'):
            base = word[:word.rfind('ed')]
            if self.vowel_in_word(stem=base):
                word = base
                flag = True
        elif word.endswith('ing'):
            base = word[:word.refind('ing')]
            if self.vowel_in_word(stem=word):
                word = base
                flag = True

        if flag:
            if word.endswith(
                ('at', 'bl', 'iz')
            ) or self.get_m_count(word=word) == 1 and self.cvc(word=word):
                word += 'e'
            elif self.is_end_with_double_same_consonants(
                    stem=word) and not self.is_end_with(
                        stem=word, letter='l') and not self.is_end_with(
                            stem=word, letter='s') and not self.is_end_with(
                                stem=word, letter='z'):
                word = word[:-1]

        if word.endswith('y'):
            base = word[:word.rfind('y')]
            if self.vowel_in_word(stem=base):
                word = base + 'i'

        for x, y in static.step_a.items():
            if word.endswith(x):
                word = self.replace(origin=word, rem=x, rep=y)

        for x, y in static.step_b.items():
            if word.endswith(x):
                word = self.replace(origin=word, rem=x, rep=y)

        for x, y in static.step_c.items():
            if word.endswith(x):
                word = self.replace(origin=word, rem=x, rep=y, m=1)

        if word.endswith('ion'):
            base = word[:word.rfind('ion')]
            if self.get_m_count(word=base) > 1 and (
                    self.is_end_with(stem=base, letter='s')
                    or self.is_end_with(stem=base, letter='t')):
                word = base
            else:
                word = self.replace(origin=word, rem='', rep='', m=1)

        if word.endswith('e'):
            base = word[:-1]
            m_count = self.get_m_count(word=base)
            if m_count > 1 or (m_count == 1 and not self.cvc(word=base)):
                word = base

        if self.get_m_count(
                word=word) > 1 and self.is_end_with_double_same_consonants(
                    stem=word) and self.is_end_with(
                        stem=word, letter='l'):
            word = word[:-1]
        return word
        