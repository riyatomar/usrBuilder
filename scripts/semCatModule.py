from constants.constantList import NE_TAG, CALENDARIC_UNITS, DOW_UNITS

def get_original_word_info(entry):
    """Check for 'per', 'loc', 'org' in the original_word and include them in the third column if present."""
    original_word = entry.get('original_word', '')
    wx_word = entry.get('wx_word', '')

    if wx_word in CALENDARIC_UNITS:
        return 'moy'
    
    if wx_word in DOW_UNITS:
        return 'dow'

    matches = []
    for tag in NE_TAG:
        if tag in original_word:
            if tag == 'loc':
                matches.append('place')  # Replace 'loc' with 'place'
            else:
                matches.append(tag)
    return ','.join(matches) if matches else '-'  # Join matches with commas or return '-'


from constants.constantList import NE_TAG

