def map_tam(word):
    with open("constants/tam_dict.tsv", "r") as tam_details_dict:
        tam_details = tam_details_dict.read().strip().split("\n")  # Ensure no trailing newlines
        tam_part = word.split('-')[1]  # Extract tam_part from word
        verb_part = word.split('-')[0]
        for tam in tam_details:
            parts = tam.split('\t')
            default_tam = parts[0] 
            other_tams = parts[1:] 
            if tam_part in other_tams: 
                tam_part = default_tam 
    return verb_part + '-' + tam_part
