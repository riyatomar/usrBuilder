from constants.pos import TAGS_TO_DROP
from scripts.conceptModule import get_word
from scripts.indexModule import get_index
from scripts.semCatModule import get_original_word_info
from scripts.dependencyModule import get_head_dep_info
from scripts.cxnModule import get_cnx_info

def format_entry(entry):
    """Format a single entry."""
    pos_tag = entry.get('pos_tag', '-')
    if pos_tag in TAGS_TO_DROP:
        return None

    word = get_word(entry)
    index = get_index(entry)
    head_dep_info = get_head_dep_info(entry)
    cnx_info = get_cnx_info(entry)
    original_word_info = get_original_word_info(entry)

    return f"{word}\t{index}\t{original_word_info if original_word_info != '-' else '-'}\t{head_dep_info}\t{cnx_info}"

