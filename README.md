# Offline Password Strength & Pattern Analyzer

**Educational tool only** — Helps users understand why passwords are weak and how attackers exploit patterns.

**Features**
- Realistic crack-time estimation using zxcvbn
- Detects keyboard walks, dates, repeated chars, common substitutions
- Checks against a small list of extremely common passwords
- Gives concrete improvement suggestions

**Important**
- This tool **never** sends passwords anywhere.
- It **does not** crack or brute-force anything.
- Purely defensive/educational.

**Installation**
```bash
pip install zxcvbn tqdm
python main.py
