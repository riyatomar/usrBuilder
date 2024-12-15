
def get_head_dep_info(entry):
    """Generate the head-dependency information."""
    head_index = entry.get('head_index', '-')
    dep_relation = entry.get('dependency_relation', '-')
    return f"{head_index}:{dep_relation}" if head_index != '-' and dep_relation != '-' else '-'

