from constants.constantList import COMPERLESS, COMPERMORE

def get_num(entry, parser_output, index):
   
    prev_index = index - 2 
    prev_to_prev = index - 3
    next_index = index 

    # Initialize with default values
    prev_word = ''
    prev_pos = ''
    pre_to_prev_entry = {}

    if prev_index >= 0:
        prev_entry = parser_output[prev_index]
        pre_to_prev_entry = parser_output[prev_to_prev]
        prev_word = prev_entry.get('wx_word', '')
        prev_pos = prev_entry.get('pos_tag', '')
    
    if next_index < len(parser_output):  # Check if next_index is within bounds
        next_entry = parser_output[next_index]
        next_word = next_entry.get('wx_word', '')
    else:
        next_entry = {}
        next_word = ''
        
    if entry.get('dependency_relation') == 'main':
        return '-'

    morph_info = entry.get('morph_info', {})
    num = morph_info.get('num', '-')
    
    if (
        entry.get("pos_tag") in ('JJ', 'QF') and
        (prev_word == 'sabase' and prev_pos == 'INTF')
    ):
        return 'superl'
    
    if entry.get('wx_word', '').endswith('wama') and entry.get("pos_tag") == 'JJ':
        return 'superl'
    
    if entry.get('pos_tag', '') == 'JJ' and prev_pos == 'QF' and pre_to_prev_entry.get('pos_tag', '') != 'INTF':
        if prev_word in COMPERMORE:
            return 'compermore'
        if prev_word in COMPERLESS:
            return 'comperless'
    
    if entry.get('pos_tag', '') in ['NN', 'NNP'] and next_word in ['vAlA', 'vAlI', 'vAle']:
        return 'mawupa'

    if ('-' in entry.get('wx_word', '') and entry.get('wx_word', '').split('-')[0] == entry.get('wx_word', '').split('-')[1]) or (entry.get('wx_word', '') == next_word) or (pre_to_prev_entry.get('wx_word', '') == entry.get('wx_word', '') and prev_word == '-'):
        return 'xviwva'

    return 'pl' if num == 'p' else '-'
