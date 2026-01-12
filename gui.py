# gui.py - Simple GUI version of the Password Strength Analyzer
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from zxcvbn import zxcvbn
from patterns import has_keyboard_walk, has_date, has_repeated_chars, has_common_substitution
from common_passwords import COMMON_PASSWORDS

def analyze_password():
    password = entry.get().strip()
    result_text.delete(1.0, tk.END)  # Clear previous output
    
    if not password:
        result_text.insert(tk.END, "Please enter a password!\n")
        return
    
    result_text.insert(tk.END, f"Analyzing: {password}\n\n")
    
    # zxcvbn core analysis
    try:
        z_result = zxcvbn(password)
        
        score = z_result['score']
        strength = ["Very Weak", "Weak", "Fair", "Strong", "Very Strong"][score]
        
        result_text.insert(tk.END, f"zxcvbn Score: {score}/4 → {strength}\n")
        result_text.insert(tk.END, f"Offline crack time (fast GPU): {z_result['crack_times_display']['offline_fast_hashing_1e10_per_second']}\n")
        result_text.insert(tk.END, f"Offline crack time (massive cluster): {z_result['crack_times_display']['offline_slow_hashing_1e4_per_second']}\n\n")
        
        if z_result['feedback']['warning']:
            result_text.insert(tk.END, f"Warning: {z_result['feedback']['warning']}\n")
        
        if z_result['feedback']['suggestions']:
            result_text.insert(tk.END, "Suggestions:\n")
            for s in z_result['feedback']['suggestions']:
                result_text.insert(tk.END, f" • {s}\n")
        
        result_text.insert(tk.END, "\n")
        
    except Exception as e:
        result_text.insert(tk.END, f"Error in zxcvbn analysis: {e}\n")
    
    # Custom pattern checks
    issues = []
    if len(password) < 8:
        issues.append("Too short (< 8 characters)")
    if password.lower() in COMMON_PASSWORDS:
        issues.append("This is one of the most common passwords — extremely weak!")
    if has_keyboard_walk(password):
        issues.append("Contains keyboard walk pattern (qwerty, asdf, 1qaz, etc.)")
    if has_date(password):
        issues.append("Contains a date — very predictable")
    if has_repeated_chars(password):
        issues.append("Has repeated characters (aaa, 1111, etc.)")
    if has_common_substitution(password):
        issues.append("Uses common leetspeak substitutions (@, 3, 1, 0, etc.)")
    
    if issues:
        result_text.insert(tk.END, "Additional Issues:\n")
        for issue in issues:
            result_text.insert(tk.END, f" • {issue}\n")
    else:
        result_text.insert(tk.END, "No obvious dangerous patterns detected beyond zxcvbn.\n")
    
    # Strength bar (text version)
    bar = "█" * (score * 5) + "░" * (20 - score * 5)
    result_text.insert(tk.END, f"\nStrength: {strength}  [{bar}] ({score}/4)\n")

# ---------------- GUI Setup ----------------
root = tk.Tk()
root.title("Password Strength Analyzer")
root.geometry("650x550")
root.resizable(False, False)

# Style
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 11))
style.configure("TButton", font=("Helvetica", 10, "bold"))

# Header
ttk.Label(root, text="Offline Password Strength & Pattern Analyzer", font=("Helvetica", 14, "bold")).pack(pady=10)

# Input
frame = ttk.Frame(root)
frame.pack(pady=10)

ttk.Label(frame, text="Enter Password:").pack(side=tk.LEFT, padx=5)
entry = ttk.Entry(frame, width=40, show="•")  # masked input
entry.pack(side=tk.LEFT, padx=5)

# Analyze Button
ttk.Button(root, text="Analyze", command=analyze_password).pack(pady=5)

# Result Area
result_text = scrolledtext.ScrolledText(root, width=75, height=22, font=("Consolas", 10))
result_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Footer note
ttk.Label(root, text="Educational tool only • Never sends your password anywhere", font=("Helvetica", 9, "italic")).pack(pady=5)

root.mainloop()
