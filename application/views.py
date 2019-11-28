from .models import User, get_todays_recent_posts
from flask import Flask, request, session, redirect, url_for, render_template, flash

app = Flask(__name__)

videos = {'ids': ['ooJSgsB5fIE','-AkuKKJ8dN0','VxRX2u0Bk2g','_nVq7f26-Uo'], 'name':['What is Cyber Security? | Introduction to Cyber Security | Cyber Security Training | Edureka','An Introduction to Cybersecurity Careers','Day in the Life of a Cybersecurity Student','The Five Laws of Cybersecurity | Nick Espinosa | TEDxFondduLac']}
topics = ['Encryption','Encrypt','Standards']

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', topics = topics)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    
        if len(username) < 1:
            flash('Your username must be at least one character.')
        elif len(password) < 5:
            flash('Your password must be at least 5 characters.')
        elif not User(username).register(password):
            flash('A user with that username already exists.')
        else:
            session['username'] = username
            flash('Logged in.')
            return redirect(url_for('index'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not User(username).verify_password(password):
            flash('Invalid login.')
        else:
            session['username'] = username
            flash('Logged in.')
            return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/add_post', methods=['POST'])
def add_post():
    title = request.form['title']
    tags = request.form['tags']
    text = request.form['text']

    if not title:
        flash('You must give your post a title.')
    elif not tags:
        flash('You must give your post at least one tag.')
    elif not text:
        flash('You must give your post a text body.')
    else:
        print(session)
        User(session['username']).add_post(title, tags, text)

    return redirect(url_for('index'))

# @app.route('/results/<term>', methods=['GET'])
# def results(term):
#     return render_template('results.html')

@app.route('/search', methods=['POST'])
def search():
    term = request.form['search_term']

    return render_template('results.html',
                            term=term,
                            videos = videos)

@app.route('/video')
def video():
    return render_template('video.html', videos=videos)

@app.route('/like_post/<post_id>')
def like_post(post_id):
    username = session.get('username')

    if not username:
        flash('You must be logged in to like a post.')
        return redirect(url_for('login'))

    User(username).like_post(post_id)

    flash('Liked post.')
    return redirect(request.referrer)

@app.route('/profile/<username>')
def profile(username):
    logged_in_username = session.get('username')
    user_being_viewed_username = username

    user_being_viewed = User(user_being_viewed_username)
    posts = user_being_viewed.get_recent_posts()

    similar = []
    common = []

    if logged_in_username:
        logged_in_user = User(logged_in_username)

        if logged_in_user.username == user_being_viewed.username:
            similar = logged_in_user.get_similar_users()
        else:
            common = logged_in_user.get_commonality_of_user(user_being_viewed)

    return render_template(
        'profile.html',
        username=username,
        posts=posts,
        similar=similar,
        common=common
    )

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    flash('Logged out.')
    return redirect(url_for('index'))