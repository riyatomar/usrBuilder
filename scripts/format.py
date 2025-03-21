from constants.constantList import TAGS_TO_DROP, COMPERLESS, COMPERMORE
from scripts.conceptModule import get_word
from scripts.indexModule import get_index
from scripts.semCatModule import get_original_word_info
from scripts.dependencyModule import get_head_dep_info
from scripts.cxnModule import get_cnx_info
from scripts.morphSemModule import get_num
from scripts.spkViewModule import get_spk_view_info

# def format_entry(entry):
def format_entry(entry, parser_output, index, discourse_info):
    """Format a single entry."""
    pos_tag = entry.get('pos_tag', '-')
    original_word = entry.get('original_word', '-')
    wx_word = entry.get('wx_word', '-')
    prev_index = index - 1  # Convert to 0-based index
    prev_to_prev_index = index - 2
    next_index = index + 1
    next_to_next_index = index + 2
    prev_entry = parser_output[prev_index] if prev_index >= 0 else {}
    prev_to_prev_entry = parser_output[prev_to_prev_index] if prev_to_prev_index >= 0 else {}
    next_entry = parser_output[next_index] if next_index < len(parser_output) else {}
    next_to_next_entry = parser_output[next_to_next_index] if next_to_next_index < len(parser_output) else {}


    if pos_tag in TAGS_TO_DROP:
        return None
    if original_word == 'सबसे' and pos_tag == 'INTF':
        return None
    if (wx_word in COMPERLESS or wx_word in COMPERMORE) and pos_tag == 'QF' and prev_entry.get('pos_tag') != 'INTF':
        return None
    if original_word in ['बजे', 'सदी']:
        if prev_entry.get('pos_tag') == "QC" or prev_entry.get('wx_word').isdigit():
            return None
    if wx_word == 'jI':
        if prev_entry.get('pos_tag') in ['NN', 'NNP', 'NNPC', 'NNP']:
            return None
    if prev_entry and ((entry.get('wx_word', '') == prev_entry.get('wx_word', '-'))):# or (prev_to_prev_entry.get('wx_word', '') == wx_word and prev_entry.get('wx_word', '-') == '-')):
        return None
    if wx_word == next_to_next_entry.get('wx_word', '') and next_entry.get('wx_word', '-') == '-':
        return None
        

    word = get_word(entry, parser_output, index)
    index = get_index(entry)
    head_dep_info = get_head_dep_info(entry, parser_output, index)
    cnx_info = get_cnx_info(entry)
    original_word_info = get_original_word_info(entry, parser_output, index)
    num_info = get_num(entry, parser_output, index)
    spk_view_info = get_spk_view_info(entry, parser_output, index)

    return f"{word}\t{index}\t{original_word_info if original_word_info != '-' else '-'}\t{num_info}\t{head_dep_info}\t{discourse_info}\t{spk_view_info}\t-\t{cnx_info}"
