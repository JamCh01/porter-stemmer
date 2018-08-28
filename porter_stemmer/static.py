class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


static = AttrDict()
static.update({
    'step_a': {
        'ational': 'ate',
        'tional': 'tion',
        'enci': 'ence',
        'anci': 'ance',
        'izer': 'ize',
        'abli': 'able',
        'alli': 'al',
        'entli': 'ent',
        'eli': 'e',
        'ousli': 'ous',
        'ization': 'ize',
        'ation': 'ate',
        'ator': 'ate',
        'alism': 'al',
        'iveness': 'ive',
        'fulness': 'ful',
        'ousness': 'ous',
        'aliti': 'al',
        'iviti': 'ive',
        'biliti': 'ble'
    },
    'step_b': {
        'icate': 'ic',
        'ative': '',
        'alize': 'al',
        'iciti': 'ic',
        'ful': '',
        'ness': '',
    },
    'step_c': {
        'al': '',
        'ance': '',
        'ence': '',
        'er': '',
        'ic': '',
        'able': '',
        'ible': '',
        'ant': '',
        'ement': '',
        'ment': '',
        'ent': '',
        'ou': '',
        'ism': '',
        'ate': '',
        'iti': '',
        'ous': '',
        'ive': '',
        'ize': '',
    }
})
