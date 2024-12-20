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


def format_sentence(sentence_data):
    """Format the parser output for a single sentence."""
    result = []
    sentence_id = sentence_data['sentence_id']
    result.append(f"<sent_id={sentence_id}>")
    sentence_type = get_sentence_type(sentence_data)
    sentence_text = get_sentence_text(sentence_data)
    result.append(f'#{sentence_text}')

    found_indices = []
    cxn_val_map = {}
    parser_output = sentence_data['parser_output']  # Access parser_output from sentence_data

    for i, entry in enumerate(parser_output):  # Use 'i' as the index for each entry
        formatted_entry = format_entry(entry, parser_output, i)  # Pass 'i' as the index
        if formatted_entry:
            # Split the formatted entry by tab
            entry_parts = formatted_entry.split('\t')
            index = entry_parts[1]
            
            if len(entry_parts) >= 8:  
                cxn_val = entry_parts[8].split(':')[0]
                dep_rel = entry_parts[4]
                cxn_val_map[cxn_val] = dep_rel
                # print(cxn_val_map)
                print(dep_rel, cxn_val)
                found_indices.append(cxn_val)
            
            # if index in found_indices:
            #     print(index)
           
            result.append(formatted_entry)
    # print('==================')

    

    result.append(f"%{sentence_type}")
    result.append(f"</sent_id>")
    result.append("\n\n")  # Blank line for separation
    return '\n'.join(result)

