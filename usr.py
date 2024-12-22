import json
from constants.constantList import NE_TAG
from constants.constantList import TAGS_TO_DROP

def load_json(file_path):
    """Load the JSON data from a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_output(output_file, formatted_output):
    """Save the formatted output to a file."""
    with open(output_file, 'w', encoding='utf-8') as out_f:
        out_f.write(formatted_output)

def get_word(entry):
    """Retrieve the word from the entry."""
    return entry.get('wx_word', '-')

def get_index(entry):
    """Retrieve the index from the entry."""
    return entry.get('index', '-')

def get_head_dep_info(entry):
    """Generate the head-dependency information."""
    head_index = entry.get('head_index', '-')
    dep_relation = entry.get('dependency_relation', '-')
    return f"{head_index}:{dep_relation}" if head_index != '-' and dep_relation != '-' else '-'

def get_cnx_info(entry):
    """Generate the construction information."""
    cnx_index = entry.get('cnx_index', '-')
    cnx_component = entry.get('cnx_component', '-')
    return f"{cnx_index}:{cnx_component}" if cnx_index != '-' and cnx_component != '-' else '-'

def get_original_word_info(entry):
    """Check for 'per', 'loc', 'org' in the original_word and include them in the third column if present."""
    original_word = entry.get('original_word', '')
    matches = []
    for tag in NE_TAG:
        if tag in original_word:
            if tag == 'loc':
                matches.append('place')  # Replace 'loc' with 'place'
            else:
                matches.append(tag)
    return ','.join(matches) if matches else '-'  # Join matches with commas or return '-'

def get_sentence_type(sentence_data):
    """Determine the sentence type based on the presence of 'nahIM' in wx_word."""
    for entry in sentence_data['parser_output']:
        if 'nahIM' in entry.get('wx_word', ''):
            return 'negative'  # If "nahIM" is found, sentence type is negative
        if '?' in entry.get('original_word', ''):
            return 'interrogative'
        if '!' in entry.get('original_word', ''):
            return 'imperative'
    return 'affirmative'  # Otherwise, sentence type is affirmative

def extract_head_index_of_RP(sentence_data):
    """Extract the head_index of entries with pos_tag 'RP' and find corresponding wx_word."""
    head_indices = []
    rp_words = {}  # To store the wx_word corresponding to the head_index of RP
    
    for entry in sentence_data['parser_output']:
        pos_tag = entry.get('pos_tag', '-')
        word = entry.get('wx_word', '-')
        head_index = entry.get('head_index', '-')
        
        if head_index != '-' and head_index.isdigit():
            head_index = int(head_index)
            if pos_tag == 'RP':
                head_indices.append(head_index)
                rp_words[head_index] = word
    return head_indices, rp_words

def format_entry(entry, discourse_marker_match):
    """Format a single entry."""
    pos_tag = entry.get('pos_tag', '-')
    if pos_tag in TAGS_TO_DROP:
        return None

    word = get_word(entry)
    index = get_index(entry)
    head_dep_info = get_head_dep_info(entry)
    cnx_info = get_cnx_info(entry)
    original_word_info = get_original_word_info(entry)

    # Add 'true' if there's a discourse marker match and dependency_relation is 'main'
    additional_flag = 'true' if discourse_marker_match and entry.get('dependency_relation', '-') == 'main' else '-'

    return f"{word}\t{index}\t{original_word_info if original_word_info != '-' else '-'}\t-\t-\t{head_dep_info}\t{cnx_info}\t{additional_flag}"

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

        formatted_entry = format_entry(entry, discourse_marker_match)
        if formatted_entry:
            result.append(formatted_entry)

    result.append(f"%{sentence_type}")
    result.append(f"</sent_id>")
    result.append("")  # Blank line for separation
    return '\n'.join(result)


def format_parser_output(file_path, discourse_path, output_file):
    """Main function to format parser output from a JSON file."""
    data = load_json(file_path)
    discourse_data = load_json(discourse_path)

    results = []
    for sentence_data in data['response']:
        results.append(format_sentence(sentence_data, discourse_data))

    formatted_output = '\n'.join(results)
    save_output(output_file, formatted_output)

# File path to the JSON input
file_path = "IO/updated_parser_output.json"
discourse_path = "IO/discourse_output.txt"
output_file = "IO/usr_output.txt"

# Call the function to format and save the output
format_parser_output(file_path, discourse_path, output_file)

