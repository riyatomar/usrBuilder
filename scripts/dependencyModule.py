def get_head_dep_info(entry, parser_output, index):
    """Generate the head-dependency information."""
    wx_word = entry.get('wx_word', '-')
    head_index = entry.get('head_index', '-')
    dep_relation = entry.get('dependency_relation', '-')
    pos_tag = entry.get('pos_tag', '-')

    # Check if current wx_word is 'saxi' or 'baje'
    if wx_word in ['saxi', 'baje']:
        prev_index = index - 1  # Get previous entry (convert to 0-based index)
        if prev_index >= 0:
            prev_entry = parser_output[prev_index]
            prev_wx_word = prev_entry.get('wx_word', '-')
            if prev_wx_word.isdigit() or prev_entry.get('pos_tag') == 'QC':
                # Update dep_relation of the previous entry
                prev_entry['dependency_relation'] = wx_word

    # Generate head-dependency information
    return f"{head_index}:{dep_relation}" if head_index != '-' and dep_relation != '-' else '-'
