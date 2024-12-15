
def extract_head_index_of_RP(sentence_data):
    """Extract the head_index of entries with pos_tag 'RP' and find corresponding wx_word."""
    head_indices = []
    rp_words = {}  # To store the wx_word corresponding to the head_index of RP

    # Loop through each entry in the sentence
    for entry in sentence_data['parser_output']:
        pos_tag = entry.get('pos_tag', '-')
        word = entry.get('wx_word', '-')
        index = entry.get('index', '-')
        head_index = entry.get('head_index', '-')

        # Only try to convert head_index if it's a valid integer
        if head_index != '-' and head_index.isdigit():
            head_index = int(head_index)
            # If the pos_tag is RP, store its head_index and corresponding wx_word
            if pos_tag == 'RP' and head_index != '-':
                head_indices.append(head_index)
                rp_words[head_index] = word  # Store the word corresponding to the head_index

    # Now, check which words have the same index as the RP head_indices
    matched_index = None
    for entry in sentence_data['parser_output']:
        index = entry.get('index', '-')
        if index in head_indices:
            matched_index = entry.get('index', '-')
    
    return head_indices, matched_index, rp_words  # Return both the head indices and the matched words
