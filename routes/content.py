from flask import Blueprint
from flask import redirect, url_for, flash, request, render_template
from models import db, AppPost, Comment, User
from flask_login import current_user, login_required

home_bp = Blueprint("home" , __name__)
app_bp = Blueprint("app1" , __name__)
post_bp = Blueprint("post" , __name__)

@home_bp.route('/')
def index():
    apps = AppPost.query.filter_by(status='approved').order_by(AppPost.votes.desc()).all()
    return render_template('index.html', apps=apps)

@app_bp.route('/app/<int:id>', methods=['GET', 'POST'])
def app_details(id):
    item = db.session.get(AppPost, id)
    if not item: return "Não encontrado", 404
    
    if request.method == 'POST' and current_user.is_authenticated:
        content = request.form.get('content')
        parent_id = request.form.get('parent_id')
        if content:
            comment = Comment(content=content, user_id=current_user.id, post_id=id, parent_id=parent_id)
            db.session.add(comment)
            db.session.commit()
        return redirect(url_for('app1.app_details', id=id))
        
    return render_template('app_details.html', app=item)

@post_bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        post = AppPost(
            title=request.form['title'], version=request.form['version'],
            description=request.form['description'], download_url=request.form['download_url'],
            category=request.form['category'], image_url=request.form['image_url'],
            user_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        flash('Publicação enviada para análise!', 'success')
        return redirect(url_for('dashboard.dashboard'))
    return render_template('create_post.html', post=None)

@post_bp.route('/post/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = db.session.get(AppPost, id)
    if not post: return "Não encontrado", 404
    if post.user_id != current_user.id and current_user.role != 'admin':
        return "Acesso Negado", 403

    if request.method == 'POST':
        post.title = request.form['title']
        post.version = request.form['version']
        post.description = request.form['description']
        post.download_url = request.form['download_url']
        post.category = request.form['category']
        post.image_url = request.form['image_url']
        db.session.commit()
        flash('Atualizado com sucesso!', 'success')
        return redirect(url_for('dashboard.dashboard'))
        
    return render_template('create_post.html', post=post)

@post_bp.route('/post/delete/<int:id>')
@login_required
def delete_post(id):
    post = db.session.get(AppPost, id)
    if post and (post.user_id == current_user.id or current_user.role == 'admin'):
        db.session.delete(post)
        db.session.commit()
        flash('Publicação removida.', 'info')
    return redirect(url_for('dashboard.dashboard'))