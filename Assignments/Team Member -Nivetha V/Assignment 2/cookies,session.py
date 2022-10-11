from flask import Flask, session
app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret'

@app.route('/start_counter')
def start_counter():
    session['count'] = 0
    return 'New counter started!'

@app.route('/count')
def count():
    count = session.get('count')
    if isinstance(count, int):
        session['count'] += 1
        return str(session['count'])
    return 'No counter set!'

@app.route('/get_count')
def get_count():
    return str(session.get('count', 'No counter set!'))

@app.route('/clear_count')
def clear_count():
    session.pop('count', None)
    return 'Counter cleared!'

if __name__ == '__main__':
    app.run(debug=True)
