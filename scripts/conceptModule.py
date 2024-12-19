
def get_word(entry, parser_output, index):
    """Retrieve the word from the entry."""
    morph_info = entry.get('morph_info', {})
    root = morph_info.get('root', '-')
    tam = morph_info.get('tam', '-')
    wx_word = entry.get('wx_word', '-')
    pos_tag = entry.get('pos_tag', '-')

    category_1 = ["wuma", "wumhArA", "wumako", "wuJe", "wU", "wuJako", "Apa"]
    category_2 = ["mEM", "hama", "hamArA", "hamako", "hameM", "muJe", "muJako"]
    category_3 = ["Ji"]
    category_4 = ["vaha", "yaha"]
    category_5 = ["kyA", "kOna", "kaba", "kahAz", "kEse", "kisase", "kEsA", "kyoM", "kisane", "kisako", "kisaki", "kiwanA", "kiwanI", "kisaliye"]
    category_6 = ["jo", "jahAZ", "jisa", "jaba", "jina", "jiwanA", "jisakA", "jisake"]

    if pos_tag in ('NNPC', 'NNP', 'PRP', 'DEM', 'QC'):
        concept = root if root != '-' else wx_word
    else:
        concept = root + '_1' if root != '-' else wx_word

    # Check for categories
    if concept in category_1:
        return "$addressee"
    elif concept in category_2:
        return "$speaker"
    elif concept in category_3:
        return "$respect"
    elif concept in category_4:
        return "$wyax"
    elif concept.strip('_1') in category_5:
        return "$kim"
    elif concept.strip('_1') in category_6:
        return "$yax"

    # Default concept assignment
    word = concept

    # Check if the current pos_tag is VM and the next pos_tag is VAUX
    if pos_tag == 'VM' and index + 1 < len(parser_output):
        next_entry = parser_output[index + 1]
        if next_entry.get('pos_tag') != 'VAUX':
            if root == 'hE':
                word = root + '_1-pres'
            elif root == 'WA':
                word = root + '_1-past'
            else:
                word = root + '_1-' + tam + '_1'

    return word
