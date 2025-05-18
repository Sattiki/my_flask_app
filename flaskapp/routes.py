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


# Scatter plot: Brexit support vs home ownership (removed nulls)
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

    plot_html = fig.to_html(full_html=False)
    return render_template("scatter.html", title="Brexit vs. Home Ownership", plot_html=plot_html)

# Scatter plot: Brexit support vs constituency (removed nulls)
@app.route("/constituency")
def constituency():
    conn = sqlite3.connect("instance/site.db")
    df = pd.read_sql_query("""
        SELECT constituency_name, BrexitVote19, TotalVote19
        FROM uk_data
        WHERE BrexitVote19 IS NOT NULL AND TotalVote19 IS NOT NULL
    """, conn)
    conn.close()

    df['brexit_vote_ratio'] = df['BrexitVote19'] / df['TotalVote19']

    fig = px.bar(
        df.sort_values(by='brexit_vote_ratio', ascending=False),
        x='constituency_name',
        y='brexit_vote_ratio',
        title='Brexit Vote Ratio by Constituency (No Nulls)',
        labels={'brexit_vote_ratio': 'Brexit Vote Ratio'},
        height=600
    )

    fig.update_layout(xaxis_tickangle=-45)

    plot_html = fig.to_html(full_html=False)
    return render_template("constituency.html", title="Brexit Vote Ratio by Constituency", plot_html=plot_html)


