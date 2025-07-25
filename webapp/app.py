from flask import Flask, render_template, request, redirect, url_for, flash
import re, html

app = Flask(__name__)
app.secret_key = 'abc123'

SQLI_PATTERNS = [r"(\bor\b|\band\b).*=.*", r"(['\";])+.*(--)+", r"(union\s+select)", r"drop\s+table", r"information_schema"]

def is_xss(input_text):
    return bool(re.search(r"<[^>]*script", input_text, re.IGNORECASE))

def is_sqli(input_text):
    return any(re.search(p, input_text, re.IGNORECASE) for p in SQLI_PATTERNS)

# ✅ HOME ROUTE (MISSING IN YOUR CASE)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        term = request.form.get('search', '').strip()
        if is_xss(term):
            flash("XSS detected!")
            return redirect(url_for('home'))
        if is_sqli(term):
            flash("SQL Injection detected!")
            return redirect(url_for('home'))
        return redirect(url_for('result', term=html.escape(term)))
    return render_template('home.html')

@app.route('/result')
def result():
    term = request.args.get('term', '')
    return render_template('result.html', term=term)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
