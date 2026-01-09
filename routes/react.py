from flask import Blueprint
from flask import redirect, url_for, flash
from models import db, AppPost, Vote, Comment
from flask_login import current_user, login_required

vote_bp = Blueprint("vote" , __name__)
reporte_bp = Blueprint("reporte" , __name__)
like_comment_bp = Blueprint("like_comment" , __name__)

@vote_bp.route('/vote/<int:post_id>/<string:val>')
@login_required
def vote(post_id, val):
    try:
        val = int(val)
    except:
        return redirect(request.referrer or url_for('home.index'))

    if val not in [1, -1]: return redirect(request.referrer or url_for('home.index'))
    
    post = db.session.get(AppPost, post_id)
    if not post: return "Post não encontrado", 404
    
    author = post.author
    existing_vote = Vote.query.filter_by(user_id=current_user.id, post_id=post_id).first()

    if existing_vote:
        if existing_vote.value == val:
            post.votes -= val
            author.karma -= val
            db.session.delete(existing_vote)
        else:
            post.votes -= existing_vote.value
            author.karma -= existing_vote.value
            existing_vote.value = val
            post.votes += val
            author.karma += val
    else:
        new_vote = Vote(user_id=current_user.id, post_id=post_id, value=val)
        db.session.add(new_vote)
        post.votes += val
        author.karma += val
    
    db.session.commit()
    return redirect(request.referrer or url_for('app1.app_details', id=post_id))

@reporte_bp.route('/report/<int:post_id>')
@login_required
def report_post(post_id):
    post = db.session.get(AppPost, post_id)
    if post:
        post.reports += 1
        db.session.commit()
        flash('Denúncia enviada aos moderadores.', 'warning')
    return redirect(url_for('app1.app_details', id=post_id))

@like_comment_bp.route('/like_comment/<int:comment_id>')
@login_required
def like_comment(comment_id):
    comment = db.session.get(Comment, comment_id)
    if comment:
        comment.likes += 1
        db.session.commit()
    return redirect(request.referrer or url_for('home.index'))