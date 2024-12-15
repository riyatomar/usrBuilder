from scripts.format import format_entry
from scripts.sentTypeModule import get_sentence_type
from scripts.originalSentModule import get_sentence_text

def format_sentence(sentence_data):
    """Format the parser output for a single sentence."""
    result = []
    sentence_id = sentence_data['sentence_id']
    result.append(f"<sent_id={sentence_id}>")
    sentence_text = get_sentence_text(sentence_data)
    result.append(f"#{sentence_text}")
    sentence_type = get_sentence_type(sentence_data)

    for entry in sentence_data['parser_output']:
        formatted_entry = format_entry(entry)
        if formatted_entry:
            result.append(formatted_entry)

    result.append(f"%{sentence_type}")
    result.append(f"</sent_id>")
    result.append("\n\n")  # Blank line for separation
    return '\n'.join(result)
