import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from rp_ext import get_rp_word 

def format_entry(entry, rp_word):
    """Format a single entry."""
    pos_tag = entry.get('pos_tag', '-')
    if pos_tag in ["PSP", "SYM", "CC", "RP"]:
        return None

    word = entry.get('wx_word', '-')
    index = entry.get('index', '-')
    head_index = entry.get('head_index', '-')
    dep_relation = entry.get('dependency_relation', '-')
    cnx_index = entry.get('cnx_index', '-')
    cnx_component = entry.get('cnx_component', '-')

    cnx_info = f"{cnx_index}:{cnx_component}" if cnx_index != '-' and cnx_component != '-' else '-'
    head_dep_info = f"{head_index}:{dep_relation}" if head_index != '-' and dep_relation != '-' else '-'

    if rp_word:
        return f"{word}\t{index}\t{head_dep_info}\t{cnx_info}\t{rp_word}"
    return f"{word}\t{index}\t{head_dep_info}\t{cnx_info}"

def format_sentence(sentence_data):
    """Format the parser output for a single sentence."""
    result = []
    sentence_id = sentence_data['sentence_id']
    result.append(f"<sent_id={sentence_id}>")

    from rp_extractor import get_rp_word
    rp_word = get_rp_word(sentence_data['parser_output'])

    for entry in sentence_data['parser_output']:
        formatted_entry = format_entry(entry, rp_word)
        if formatted_entry:
            result.append(formatted_entry)

    result.append(f"</sent_id>")
    result.append("")  # Blank line for separation
    return '\n'.join(result)
