
def get_spk_view_info(entry):
    morph_info = entry.get('morph_info', {})
    root = morph_info.get('root', '-')
    
    if root == 'yaha':
        return 'proximal'
    if root == 'vaha':
        return 'distal'
    return '-'
