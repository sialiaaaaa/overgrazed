ignored_patterns = [
    # start, end, contains
    # Vim
    ('.', '.sw', None),  # .swp, .swo, .swn
    (None, '~', None),   # backup files
    # Emacs
    ('#', '#', None),    # auto-save
    ('.#', None, None),  # lock files
    # Generic temp/system files
    (None, '.tmp', None),
    (None, '.temp', None),
    (None, '.bak', None),
    (None, '.DS_Store', None),
    (None, 'Thumbs.db', None),
    (None, '.goutputstream', None),
    ('.', '.kate-swp', None),
    ('.git', None, None),
    ('README', None, None)
]

def is_ignored_filename(filename, ignored_patterns=[]):
    for prefix, suffix, contains in ignored_patterns:
        all_sat = True
        if prefix and not filename.startswith(prefix):
            all_sat = False
        if suffix and not filename.endswith(suffix):
            all_sat = False
        if contains and contains not in filename:
            all_sat = False
        if all_sat:
            return True
    return False
