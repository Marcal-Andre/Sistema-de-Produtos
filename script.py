from flask import Flask, render_template
import webbrowser

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

    @app.route('/contact')
    def contact():
        return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000')
    app.run(debug=True)