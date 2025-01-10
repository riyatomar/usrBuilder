from constants.constantList import COMPERLESS, COMPERMORE

def get_num(entry, parser_output, index):
   
    prev_index = index - 2  # Convert to 0-based index
    if prev_index >= 0:
        prev_entry = parser_output[prev_index]
        prev_word = prev_entry.get('wx_word')
        prev_pos = prev_entry.get('pos_tag')
        
    if entry.get('dependency_relation') == 'main':
        return '-'

    morph_info = entry.get('morph_info', {})
    num = morph_info.get('num', '-')
    
    # Check for specific conditions
    if (
        entry.get("pos_tag") in ('JJ', 'QF') and
        (prev_word == 'sabase' and prev_pos == 'INTF')
    ):
        return 'superl'
    
    if entry.get('wx_word', '').endswith('wama'):
        return 'superl'
    
    if entry.get('pos_tag', '') == 'JJ' and prev_pos == 'QF':
        if prev_word in COMPERMORE:
            return 'compermore'
        if prev_word in COMPERLESS:
            return 'comperless'
    
    return 'pl' if num == 'p' else '-'
