import sys
from zxcvbn import zxcvbn
from tqdm import tqdm
from patterns import has_keyboard_walk, has_date, has_repeated_chars, has_common_substitution
from common_passwords import COMMON_PASSWORDS

def analyze_password(password: str):
    print(f"\nAnalyzing password: {password}\n")
    
    
    result = zxcvbn(password)
    
    print("zxcvbn Score (0-4):", result['score'])
    print("Estimated crack time (offline, good GPU cluster):", result['crack_times_display']['offline_fast_hashing_1e10_per_second'])
    print("Estimated crack time (massive cluster):", result['crack_times_display']['offline_slow_hashing_1e4_per_second'])
    
    if result['feedback']['warning']:
        print("\nWarning:", result['feedback']['warning'])
    if result['feedback']['suggestions']:
        print("Suggestions:")
        for s in result['feedback']['suggestions']:
            print(" •", s)
    
    
    issues = []
    
    if len(password) < 8:
        issues.append("Too short (< 8 characters)")
    if password.lower() in COMMON_PASSWORDS:
        issues.append("This is one of the most common passwords — extremely weak!")
    if has_keyboard_walk(password):
        issues.append("Contains keyboard walk pattern (e.g. qwerty, asdf, 1qaz)")
    if has_date(password):
        issues.append("Contains a date — very common and predictable")
    if has_repeated_chars(password):
        issues.append("Has repeated characters (aaa, 1111, etc.)")
    if has_common_substitution(password):
        issues.append("Uses common leetspeak substitutions (@ for a, 3 for e, etc.)")
    
    if issues:
        print("\nAdditional detected issues:")
        for issue in issues:
            print(" •", issue)
    else:
        print("\nNo obvious dangerous patterns detected beyond zxcvbn analysis.")
    
    
    strength = ["Very Weak", "Weak", "Fair", "Strong", "Very Strong"][result['score']]
    bar = "█" * (result['score'] * 5) + "░" * (20 - result['score'] * 5)
    print(f"\nStrength: {strength}  [{bar}] ({result['score']}/4)")

def main():
    print("=== Offline Password Strength & Pattern Analyzer (2026) ===\n")
    print("Enter passwords one by one (press Ctrl+C or type 'quit' to exit)\n")
    
    while True:
        try:
            pw = input("Password: ").strip()
            if pw.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            if not pw:
                print("Empty password — not analyzed.")
                continue
                
            
            for _ in tqdm(range(100), desc="Analyzing", leave=False):
                pass  
            
            analyze_password(pw)
            print("-" * 60)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            sys.exit(0)

if __name__ == "__main__":
    main()
