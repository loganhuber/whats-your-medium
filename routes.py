from click import Path
from flask import Flask, redirect, render_template, send_from_directory, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, ContentBlock, Category, Image, FAQ
from sqlalchemy import desc

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

        questions = FAQ.query.all()

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
                               bio_paragraphs=bio_paragraphs,
                               questions=questions
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
        selected_category = request.args.get('category_id')
        categories = Category.query.all()
        print(f"selected category: {selected_category}")
        images = Image.query.filter_by(category_id=selected_category).order_by(desc(Image.id)).limit(2).all()

        return render_template(
            'public/portfolio.html',
            selected_category=selected_category,
            categories=categories,
            images=images
            )
    

    @app.route('/portfolio/load-more', methods=["GET"])
    def portfolio_load_more():
        selected_category = request.args.get('category_id')
        offset = request.args.get("offset", 0, type=int)

        images = (
            Image.query.filter_by(category_id=selected_category)
            .order_by(desc(Image.id))
            .limit(2)
            .offset(offset)
            .all()
        )

        html = render_template(
            'public/components/image-card.html',
            images=images
            )

        return jsonify({
            "html" : html
        })






    @app.route('/logout', methods=["GET", "POST"])
    def logout():
        logout_user()
        return redirect('/')


    @app.route("/uploads/<path:name>")
    def uploads(name):
        return send_from_directory(Path(app.config['UPLOAD_FOLDER']), name)
