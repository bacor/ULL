def clean_corpus(C, sep="$"):
    """Removes utterance boundaries and returns clean corpus
    with utterance boundary positions.

    Args:
        C: a very long string separated by utterance boundaries
        sep: the utterance boundary character, defaults to "$"

    Returns:
        new_C: clean corpus
        U: List with utterance boundary positions
    """
    # Make sure the corpus ends with a utterance boundary (sep)
    if C[-1] != sep: C += sep
        
    # Utterance boundary positions
    U = [i for i, w in enumerate(C) if w == sep]
    
    # Remove separators ($) and fix indices in U accordingly
    new_C = C.replace(sep, "")
    U = [U[i] - i for i in range(len(U))]

    return new_C, U