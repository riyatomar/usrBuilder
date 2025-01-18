# from constants.constantList import RANJAK_LIST

# def get_spk_view_info(entry, parser_output, index):
#     morph_info = entry.get('morph_info', {})
#     root = morph_info.get('root', '-')
#     wx_word = entry.get('wx_word', '-')
#     pos_tag = entry.get('pos_tag', '-')

#     rp_words = []
#     for item in parser_output:
#         if item.get('head_index') == str(index) and item.get('pos_tag') == 'RP':
#             rp_words.append(item.get('wx_word', '-'))
    
#     if rp_words:
#         return '/'.join(rp_words)

#     if pos_tag == 'VM' and index + 1 < len(parser_output):
#         next_entry = parser_output[index]
#         next_morph_info = next_entry.get('morph_info', {})
#         next_root = next_morph_info.get('root', '-')

#         if wx_word == root and next_root in RANJAK_LIST:
#             return f'[shade:{next_root}_1]'

#     if pos_tag in ['NN', 'NNP', 'NNPC', 'NNP'] and index + 1 < len(parser_output):
#         next_entry = parser_output[index]
#         if next_entry.get('wx_word', '') == 'jI':
#             return 'salutation'
    
#     if root == 'yaha':
#         return 'proximal'
#     if root == 'vaha':
#         return 'distal'
#     if root == 'wU':
#         return 'informal'
#     if root == 'Apa':
#         return 'respect'
#     return '-'


from constants.constantList import RANJAK_LIST

def get_spk_view_info(entry, parser_output, index):
    morph_info = entry.get('morph_info', {})
    root = morph_info.get('root', '-')
    wx_word = entry.get('wx_word', '-')
    pos_tag = entry.get('pos_tag', '-')

    results = []

    # Check for RP words
    rp_words = []
    for item in parser_output:
        if item.get('head_index') == str(index) and item.get('pos_tag') == 'RP':
            rp_words.append(item.get('wx_word', '-'))
    
    if rp_words:
        results.append('/'.join(rp_words))

    # Check for VM and RANJAK_LIST
    if pos_tag == 'VM' and index + 1 < len(parser_output):
        next_entry = parser_output[index]
        next_morph_info = next_entry.get('morph_info', {})
        next_root = next_morph_info.get('root', '-')

        if wx_word == root and next_root in RANJAK_LIST:
            results.append(f'[shade:{next_root}_1]')

    # Check for NN-based salutation
    if pos_tag in ['NN', 'NNP', 'NNPC', 'NNP'] and index + 1 < len(parser_output):
        next_entry = parser_output[index]
        if next_entry.get('wx_word', '') == 'jI':
            results.append('salutation')
    
    # Check for specific roots
    root_map = {
        'yaha': 'proximal',
        'vaha': 'distal',
        'Apa': 'respect'
    }
    if root in root_map:
        results.append(root_map[root])
    
    if wx_word == 'wU' and root == 'wU':
        results.append('informal')

    # Return joined results or '-' if empty
    return '/'.join(results) if results else '-'
