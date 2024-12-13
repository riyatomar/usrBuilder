# import json

# def format_parser_output(file_path, output_file):
#     with open(file_path, 'r', encoding='utf-8') as f:
#         data = json.load(f)

#     result = []

#     for sentence_data in data['response']:
#         sentence_id = sentence_data['sentence_id']
#         result.append(f"<sent_id={sentence_id}>")

#         rp_words = {}  # To collect RP wx_words for relevant indices
#         rp_head_index = None  # Initialize this variable to avoid UnboundLocalError
#         rp_word_to_add = None
#         for entry in sentence_data['parser_output']:
#             pos_tag = entry.get('pos_tag', '-')
#             if pos_tag == "RP":
#                 rp_head_index = entry.get('head_index', '-')
#                 rp_word = entry.get('wx_word', '-')
#             # Ensure valid conversion to int only when rp_head_index is not '-' or None
#             try:
#                 if rp_head_index != '-' and rp_head_index is not None:
#                     rp_head_index_int = int(rp_head_index)
#                     entry_index = entry.get('index', '-')
#                     if entry_index != '-' and int(entry_index) == rp_head_index_int:
#                         rp_word_to_add = rp_word
#                         print(rp_word_to_add)
#             except ValueError:
#                 pass 

#         # Second pass: Format entries and append RP words where applicable
#         for entry in sentence_data['parser_output']:
#             pos_tag = entry.get('pos_tag', '-')
#             if pos_tag in ["PSP", "SYM", "CC", "RP"]:
#                 continue

#             word = entry.get('wx_word', '-')
#             index = entry.get('index', '-')
#             head_index = entry.get('head_index', '-')
#             dep_relation = entry.get('dependency_relation', '-')
#             cnx_index = entry.get('cnx_index', '-')
#             cnx_component = entry.get('cnx_component', '-')

#             if cnx_index != '-' and cnx_component != '-':
#                 cnx_info = f"{cnx_index}:{cnx_component}"
#             else:
#                 cnx_info = '-'

#             if head_index == '-' and dep_relation == '-':
#                 head_dep_info = '-'
#             else:
#                 head_dep_info = f"{head_index}:{dep_relation}"
                

#             if rp_word_to_add:
#                 formatted_entry = f"{word}\t{index}\t{head_dep_info}\t{cnx_info}\t{rp_word_to_add}"
#             else:
#                 formatted_entry = f"{word}\t{index}\t{head_dep_info}\t{cnx_info}"

#             result.append(formatted_entry)

#         result.append(f"</sent_id>")
#         result.append("")  # Blank line for separation

#     formatted_output = '\n'.join(result)
    
#     with open(output_file, 'w', encoding='utf-8') as out_f:
#         out_f.write(formatted_output)

# # File path to the JSON input
# file_path = "cxn_json_out.txt"  # Replace with the actual file path
# output_file = "usr_output.txt"  # Replace with the desired output file path

# # Call the function to format and save the output
# format_parser_output(file_path, output_file)

import json

def load_json(file_path):
    """Load the JSON data from a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_output(output_file, formatted_output):
    """Save the formatted output to a file."""
    with open(output_file, 'w', encoding='utf-8') as out_f:
        out_f.write(formatted_output)

def get_rp_word(parser_output):
    """Extract the RP word based on the head index."""
    rp_head_index = None
    rp_word = None

    for entry in parser_output:
        pos_tag = entry.get('pos_tag', '-')
        if pos_tag == "RP":
            rp_head_index = entry.get('head_index', '-')
            rp_word = entry.get('wx_word', '-')
            break  # Assuming only one RP word per sentence

    if rp_head_index and rp_head_index != '-':
        try:
            rp_head_index_int = int(rp_head_index)
            for entry in parser_output:
                entry_index = entry.get('index', '-')
                if entry_index != '-' and int(entry_index) == rp_head_index_int:
                    return rp_word
        except ValueError:
            pass

    return None

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

    rp_word = get_rp_word(sentence_data['parser_output'])

    for entry in sentence_data['parser_output']:
        formatted_entry = format_entry(entry, rp_word)
        if formatted_entry:
            result.append(formatted_entry)

    result.append(f"</sent_id>")
    result.append("")  # Blank line for separation
    return '\n'.join(result)

def format_parser_output(file_path, output_file):
    """Main function to format parser output from a JSON file."""
    data = load_json(file_path)

    results = []
    for sentence_data in data['response']:
        results.append(format_sentence(sentence_data))

    formatted_output = '\n'.join(results)
    save_output(output_file, formatted_output)

# File path to the JSON input
file_path = "cxn_json_out.txt"  # Replace with the actual file path
output_file = "usr_output.txt"  # Replace with the desired output file path

# Call the function to format and save the output
format_parser_output(file_path, output_file)
