from flask import render_template, flash, redirect, url_for, request, current_app as app
from flaskapp import db
from flaskapp.models import BlogPost, IpView, Day
from flaskapp.forms import PostForm
import datetime
import pandas as pd
import json
import plotly.express as px
import sqlite3


# Home page
@app.route("/")
@app.route("/home")
def home():
    posts = BlogPost.query.all()
    return render_template('home.html', posts=posts)

# About page
@app.route("/about")
def about():
    return render_template('about.html', title='About page')

# Create new blog post
@app.route("/post/new", methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = BlogPost(title=form.title.data, content=form.content.data, user_id=1)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form)

# Dashboard showing page views per day
@app.route('/dashboard')
def dashboard():
    days = Day.query.all()
    df = pd.DataFrame([{'Date': day.id, 'Page views': day.views} for day in days])
    fig = px.bar(df, x='Date', y='Page views')
    graphJSON = json.dumps(fig, cls=px.utils.PlotlyJSONEncoder)
    return render_template('dashboard.html', title='Page views per day', graphJSON=graphJSON)

# Scatter plot: Brexit support vs home ownership
@app.route("/scatter")
def scatter():
    conn = sqlite3.connect("instance/site.db")
    df = pd.read_sql_query("""
        SELECT 
            constituency_name, 
            BrexitVote19, 
            TotalVote19, 
            c11HouseOwned 
        FROM uk_data 
        WHERE BrexitVote19 IS NOT NULL 
          AND TotalVote19 IS NOT NULL 
          AND c11HouseOwned IS NOT NULL;
    """, conn)
    conn.close()

    df['brexit_vote_ratio'] = df['BrexitVote19'] / df['TotalVote19']
    fig = px.scatter(
        df,
        x='c11HouseOwned',
        y='brexit_vote_ratio',
        hover_name='constituency_name',
        labels={
            'c11HouseOwned': 'Home Ownership (%)',
            'brexit_vote_ratio': 'Brexit Vote Ratio'
        },
        title='Brexit Support vs. Home Ownership by Constituency',
        trendline='ols'
    )

    graphJSON = json.dumps(fig, cls=px.utils.PlotlyJSONEncoder)
    return render_template("scatter.html", title="Brexit vs. Home Ownership", graphJSON=graphJSON)

# Track IP views
@app.before_request
def before_request_func():
    day_id = datetime.date.today()
    client_ip = request.remote_addr

    query = Day.query.filter_by(id=day_id)
    if query.count() > 0:
        current_day = query.first()
        current_day.views += 1
    else:
        current_day = Day(id=day_id, views=1)
        db.session.add(current_day)

    query = IpView.query.filter_by(ip=client_ip, date_id=day_id)
    if query.count() == 0:
        ip_view = IpView(ip=client_ip, date_id=day_id)
        db.session.add(ip_view)

    db.session.commit()
