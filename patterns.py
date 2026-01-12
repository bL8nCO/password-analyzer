import re
from datetime import datetime

def has_keyboard_walk(pw: str) -> bool:
    """Detects keyboard patterns like qwerty, asdf, 1qaz, etc."""
    keyboard = "qwertyuiopasdfghjklzxcvbnm"
    rev_keyboard = keyboard[::-1]
    numpad = "1234567890"
    
    lowers = pw.lower()
    for seq in [keyboard, rev_keyboard, numpad, numpad[::-1]]:
        for i in range(len(seq) - 3):
            if seq[i:i+4].lower() in lowers or seq[i:i+4][::-1].lower() in lowers:
                return True
    return False

def has_date(pw: str) -> bool:
    """Detects common date formats: 01012000, 01-01-2000, 1.1.00, etc."""
    patterns = [
        r'\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b',           
        r'\b\d{4}[./-]\d{1,2}[./-]\d{1,2}\b',             
        r'\b\d{6,8}\b'                                    
    ]
    return any(re.search(p, pw) for p in patterns)

def has_repeated_chars(pw: str) -> bool:
    """aaa, 1111, @@@ etc."""
    return bool(re.search(r'(.)\1{2,}', pw))

def has_common_substitution(pw: str) -> bool:
    """Detects leetspeak like p@ssw0rd, m1cr0$0ft"""
    lowers = pw.lower()
    subs = ["@", "3", "1", "0", "$", "!", "7"]
    for s in subs:
        if s in lowers and len(lowers) > 6:
            return True
    return False
