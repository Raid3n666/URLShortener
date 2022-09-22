from flask import Flask, redirect, request, render_template, flash, url_for
from modules.url_shortener import url_maker
from modules.db import URL, DAL

app = Flask(__name__)

dal = DAL()

app.config['SECRET_KEY'] = '666'

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        target = request.form['target']
        short_url = url_maker()
        url = URL(target, short_url)
        if url.is_valid():
            if target in dal.list_all_targets():
                short_url = url.get_existing()
            else:
                url.add()
        else:
            flash('BAD LINK')
            return render_template('index.html')
        return render_template('index.html',url = short_url)
    else:
        return render_template('index.html')
        

@app.route('/<url>.shorturl')
def redirected(url):
    url = URL(url = url)
    if url.get_target():
        return redirect(f'{url.get_target()}', code = 302)
    else:
        return redirect(url_for('index'))

@app.route('/None')
def none():
    return redirect(url_for('index'))

@app.route('/custom', methods = ['POST', 'GET'])
def custom():
    if request.method == 'POST':
        target = request.form['target']
        custom_url = request.form['custom']
        url = URL(target = target, url = custom_url)
        if url.is_valid():
            if dal.custom_url_check(custom_url) == 'pass':
                url = URL(target, custom_url)
                url.add()
                status = 'URL CREATED'
                flash(url.url)
            else:
                status = f'{dal.custom_url_check(custom_url)}'
        else:
            status = 'Target URL is not valid.'
        return render_template('custom.html', status = status)
    else:
        return render_template('custom.html')

@app.route('/list')
def _list():
    objects = dal.get_all_objects()
    return render_template('list.html',urls = objects)

@app.route('/terms')
def terms():
    return render_template('terms.html')

app.run(debug = True, port = 80)
