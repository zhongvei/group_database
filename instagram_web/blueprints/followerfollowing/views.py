from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from models.followerfollowing import FollowerFollowing
from flask_login import current_user, login_required

followerfollowing_blueprint = Blueprint('followerfollowing',
                            __name__,
                            template_folder='templates')


@followerfollowing_blueprint.route('<username>/new', methods = ['GET'])
@login_required
def new(username):
    idol = User.get_or_none(User.name == username)
    requests = FollowerFollowing.select().where(FollowerFollowing.idol_id == idol)
    return render_template('/followerfollowing/new.html',requests = requests)

@followerfollowing_blueprint.route('<fan>/edit', methods = ['POST'])
@login_required
def edit(fan):
    fans = User.get_or_none(User.name == fan)
    approve = FollowerFollowing.get_or_none((FollowerFollowing.idol_id == current_user.id) & (FollowerFollowing.fan_id == fans.id))
    approve.request = True
    approve.save()
    return redirect(url_for('followerfollowing.new',username = current_user.name))

@followerfollowing_blueprint.route('/<idol_id>', methods = ['POST'])
@login_required
def create(idol_id):
    idol = User.get_or_none(User.id == idol_id)
    fan = current_user.id
    follow = FollowerFollowing(fan = fan, idol = idol.id)
    if not follow.save():
        flash ("Can't follow this user, try again", 'warning')
        return redirect(url_for('users.show', username = idol.name ))
    flash ('You followed this user', 'success')
    return redirect(url_for('users.show', username = idol.name ))

@followerfollowing_blueprint.route('/<idol_id>/delete', methods = ['POST'])
@login_required
def delete(idol_id):
    idol = User.get_or_none(User.id == idol_id)
    unfollow = FollowerFollowing.get_or_none((FollowerFollowing.idol_id == idol.id) & (FollowerFollowing.fan_id == current_user.id))
    if not unfollow:
        flash ("You can't do dis", 'warning')
        return redirect(url_for('users.show', username = idol.name))
    if not unfollow.delete_instance():
        flash ("Can't unfollow this user, try again", 'warning')
        return redirect(url_for('users.show', username = idol.name ))
    flash ('You unfollowed this user', 'success')
    return redirect(url_for('users.show', username = idol.name ))


