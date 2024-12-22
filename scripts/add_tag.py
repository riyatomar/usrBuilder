from scripts.format import format_entry
from scripts.sentTypeModule import get_sentence_type
from scripts.originalSentModule import get_sentence_text


# def format_sentence(sentence_data):
#     """Format the parser output for a single sentence."""
#     result = []
#     sentence_id = sentence_data['sentence_id']
#     result.append(f"<sent_id={sentence_id}>")
#     sentence_type = get_sentence_type(sentence_data)
#     sentence_text = get_sentence_text(sentence_data)
#     result.append(f'#{sentence_text}')

#     parser_output = sentence_data['parser_output']  # Access parser_output from sentence_data

#     for i, entry in enumerate(parser_output):  # Use 'i' as the index for each entry
#         formatted_entry = format_entry(entry, parser_output, i)  # Pass 'i' as the index
#         if formatted_entry:
#             result.append(formatted_entry)

#     result.append(f"%{sentence_type}")
#     result.append(f"</sent_id>")
#     result.append("\n\n")  # Blank line for separation
#     return '\n'.join(result)


def format_sentence(sentence_data, discourse_data):
    """Format the parser output for a single sentence."""
    result = []
    sentence_id = sentence_data['sentence_id']
    result.append(f"<sent_id={sentence_id}>")
    sentence_type = get_sentence_type(sentence_data)

    parser_output = sentence_data['parser_output']
    skip_next = False  # Flag to skip processing the next entry

    # Check if discourse_marker exists in discourse data
    discourse_marker_match = any(
        discourse['discourse_marker'] != 'None' and discourse['sent_2_id'] == sentence_id
        for discourse in discourse_data
    )

    for i, entry in enumerate(parser_output):
        if skip_next:
            skip_next = False
            continue

        if entry.get('pos_tag') == 'VM' and i + 1 < len(parser_output):
            next_entry = parser_output[i + 1]
            if next_entry.get('pos_tag') == 'VAUX':
                entry['wx_word'] = f"{entry['wx_word']} {next_entry['wx_word']}"
                entry['dependency_relation'] += f" {next_entry.get('dependency_relation', '-')}"
                skip_next = True

        formatted_entry = format_entry(entry, parser_output, i, discourse_marker_match)
        if formatted_entry:
            result.append(formatted_entry)

    result.append(f"%{sentence_type}")
    result.append(f"</sent_id>")
    result.append("")  # Blank line for separation
    return '\n'.join(result)
