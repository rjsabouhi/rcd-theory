# Deprecated: Merged into lake_state.py
# Kept for compatibility with older imports.

def is_lake_state(*args, **kwargs):
    from .lake_state import is_lake_state
    return is_lake_state(*args, **kwargs)

def transition_state(*args, **kwargs):
    return sum(args)  # Placeholder

def collapse_or_expand(state_vector, force_factor):
    return state_vector * force_factor
