from flask import Flask, redirect, render_template, url_for


def register_routes(app):
    
    @app.route('/')
    def index():
        return render_template('public/index.html')