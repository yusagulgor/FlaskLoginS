from flask import Blueprint, render_template, request, redirect, url_for

main = Blueprint("main", __name__)

@main.route('/home')
def home():
    return render_template('home.html')

@main.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        pwd = request.form.get('pwd')
        if name == "sıgmazam" and pwd == "R*!key":
            return redirect(url_for('main.home'))
    
    return render_template('login.html')
