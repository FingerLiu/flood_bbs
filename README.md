# Basic script to auto comment or post on a bbs with captcha(using tesseract).

# The script does the following things

- hack captcha and login
- navigate to post your want to comment on
- hack captcha and comment on the post.

# Usage
1. `git clone https://github.com/FingerLiu/flood_bbs.git`

2. `pip install -r requirements.txt`

3. Fix TODO in `captcha.py` to fill your own situation

4. python3 captcha.py

# How
It just use tesseract to hack captcha and then use awesome requests_html to parse html.

# Warning
Only use this script when you clearly know what you are doing. It may cause your account banned by bbs admin.

