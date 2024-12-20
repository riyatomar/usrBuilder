
def get_word(entry, parser_output, index):
    """Retrieve the word from the entry."""
    morph_info = entry.get('morph_info', {})
    root = morph_info.get('root', '-')
    tam = morph_info.get('tam', '-')
    per = morph_info.get('per', '-')
    wx_word = entry.get('wx_word', '-')
    pos_tag = entry.get('pos_tag', '-')
    dependency = entry.get('dependency_relation', '-')

    ranjak_list= ["cala", "dAla", "cuka", "xe", "le", "bETa", "uTa", "jA", "padZa", "A"]

    category_1 = ["wuma", "wumhArA", "wumako", "wuJe", "wU", "wuJako", "Apa"]
    category_2 = ["mEM", "hama", "hamArA", "hamako", "hameM", "muJe", "muJako"]
    category_3 = ["Ji"]
    category_4 = ["vaha", "yaha"]
    category_5 = ["kyA", "kOna", "kaba", "kahAz", "kEse", "kisase", "kEsA", "kyoM", "kisane", "kisako", "kisaki", "kiwanA", "kiwanI", "kisaliye"]
    category_6 = ["jo", "jahAZ", "jisa", "jaba", "jina", "jiwanA", "jisakA", "jisake"]

    if pos_tag in ('NNPC', 'NNP', 'PRP', 'DEM', 'QC') and root != 'eka':
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
        next_root = morph_info.get('root', '-')
        next_tam = morph_info.get('tam', '-')

        if dependency == 'main':

            if next_entry.get('pos_tag') != 'VAUX':
                if root == 'hE':
                    word = root + '_1-pres'
                elif root == 'WA':
                    word = 'hE' + '_1-past'
                else:
                    word = root + '_1-' + tam + '_1'
            
            elif next_entry.get('pos_tag') == 'VAUX':
                if next_root == 'jA' and tam == 'yA':
                    word = root + '_1-' + tam + '_' + next_root + '_' + next_tam + '_1'
                elif next_root in ranjak_list:
                    word = root + '_1-' + next_tam + '_1'
                else:
                    word = root + '_1-' + tam + '_' + next_root + '_1'

        
            if next_entry.get('pos_tag') != 'VAUX':
                if (tam == 'imper' and per == 'm_h'):
                    word = word.rsplit('_',1)[0]
                    word = word + '_o_2'
                elif tam == 'imper':
                    word = word.rsplit('_',1)[0]
                    word = word + '_o_1'
                elif tam == 'subj':
                    word = word.rsplit('_',1)[0]
                    word = word + '_e_1'

    return word
