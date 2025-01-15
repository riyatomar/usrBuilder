from constants.constantList import CXN_VALUE

def get_head_dep_info(entry, parser_output, index):
    """Generate the head-dependency information."""
    wx_word = entry.get('wx_word', '-')
    head_index = entry.get('head_index', '-')
    dep_relation = entry.get('dependency_relation', '-')
    
    # Check for 'QC' pos_tag or numeric wx_word
    if entry.get('pos_tag') == "QC" or wx_word.isdigit():
        if index + 1 < len(parser_output):
            next_entry = parser_output[index]  # Corrected to index + 1 for the next entry
            if next_entry.get('wx_word', '') in ['saxi', 'baje']:
                dep_rel = next_entry.get('dependency_relation', '-')
                head = next_entry.get('head_index', '-')
                return f"{head}:{dep_rel}" if head != '-' and dep_rel != '-' else '-'
    
    # Check cnx_component against CXN_VALUE
    if entry.get('cnx_component', '-') in CXN_VALUE:
        return '-'  # Skip returning head-dependency information

    # Generate head-dependency information
    return f"{head_index}:{dep_relation}" if head_index != '-' and dep_relation != '-' else '-'
