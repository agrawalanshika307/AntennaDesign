from flask import Flask, render_template, request
import os, sys

# Ensure the module is importable
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from antenna_calculator import run_calculations

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    width = length = feed_point = None
    error = None
    
    if request.method == 'POST':
        freq_str = request.form['frequency']
        er = request.form['dielectric']
        height_str = request.form['height']
        
        try:
            er = float(er)
            width, length, feed_point = run_calculations(freq_str, er, height_str)
        except ValueError as e:
            error = str(e)
    
    return render_template('index.html', width=width, length=length, feed_point=feed_point, error=error)

if __name__ == '__main__':
    app.run(debug=True)
