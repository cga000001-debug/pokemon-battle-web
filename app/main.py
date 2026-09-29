from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

@app.route('/')
def hello_world():
    return render_template('template1.html',
            project_name = "pokemon-battle-web", 
            name = "Alicia", 
            year = 2026)

if __name__ == '__main__':
    app.run('0.0.0.0', 8080)