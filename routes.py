from flask import Flask, redirect, render_template, url_for, request, flash
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, ContentBlock, Category

def get_paragraphs(str) -> list:
    return str.split('\n')
    

def register_routes(app):

    @app.context_processor
    def inject_categories():
        categories = Category.query.all()
        return {
            'categories' : categories
        }
    
    @app.route('/')
    def index():

        hero_title = ContentBlock.query.filter_by(key='hero_title').one()
        hero_text = ContentBlock.query.filter_by(key='hero_text').one()
        bio_title = ContentBlock.query.filter_by(key='bio_title').one()
        bio_text = ContentBlock.query.filter_by(key='bio_text').one()

        hero_paragraphs = get_paragraphs(hero_text.value)
        bio_paragraphs = get_paragraphs(bio_text.value)

        return render_template('public/index.html',
                               hero_title=hero_title,
                               hero_paragraphs=hero_paragraphs,
                               bio_title=bio_title,
                               bio_paragraphs=bio_paragraphs
                               )
    
    @app.route('/contact')
    def contact():
        return render_template('public/contact.html')
    
    @app.route('/login', methods=["POST", "GET"])
    def login():

        if current_user.is_authenticated:
            return redirect(url_for('admin.index'))

        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter_by(username=username).first()

            if user and check_password_hash(user.pw_hash, password):
                login_user(user)
                return redirect('/admin')

            flash("Invalid Credentials")
        return render_template('admin/login.html')
    
    @app.route('/portfolio')
    def portfolio():
        selected_category = request.args.get('catgeory_id')
        categories = Category.query.all()

        return render_template(
            'public/portfolio.html',
            selected_category=selected_category,
            categories=categories
            )
    
    @app.route('/logout', methods=["GET", "POST"])
    def logout():
        logout_user()
        return redirect('/')
