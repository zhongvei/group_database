from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from models.user_images import Image
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from flask_login import login_user, current_user, login_required, current_user
from instagram_web.util.helpers import upload_file_to_s3


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    password = request.form.get('password')
    hashed_password = generate_password_hash(password)
    user = User(email=request.form.get('email'), name=request.form.get('username'), password=hashed_password)
    if user.save():
        login_user(user)
        flash(u'User successfully created!','success')
        return redirect(url_for('home'))
    else:
        flash(user.errors, 'danger')
        return redirect(url_for('users.new'))
    
@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    from models.followerfollowing import FollowerFollowing
    user = User.get_or_none(User.name == username)
    follower = FollowerFollowing.select().where((FollowerFollowing.request == True) & (FollowerFollowing.idol_id == user.id))
    following = FollowerFollowing.select().where((FollowerFollowing.request == True) & (FollowerFollowing.fan_id == user.id))
    return render_template('users/users.html', user=user, follower = follower, following = following)

@users_blueprint.route('/index', methods=["GET"])
def index():
    images = Image.select().order_by(Image.created_at.desc())
    return render_template('/users/index.html',images = images)

@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    if str(current_user.id) == id:
        return render_template('users/edit.html')
    return current_user.id

@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    user = User.get_or_none(User.id == id)
    email = request.form.get('email')
    name = request.form.get('username')
    user.email = email
    user.name = name
    if not user.save():
        flash(u"Temporary can't update your details!",'danger')
        return redirect(url_for('users.edit', id=user.id))
    flash(u'Successfully edit your new details!','success')
    return redirect(url_for('users.edit', id=user.id))

@users_blueprint.route('/upload', methods=["POST"])
@login_required
def upload_img():
    file = request.files["user_file"]
    user = User.get_or_none(User.id == current_user.id)
    if user:
        if file :
            file.filename = secure_filename(file.filename)
            output   	  = upload_file_to_s3(file)
            if str(output) == 'None':
                user.image_path = file.filename
                user.save()
                flash(u"You look good in your new profile picture",'success')
                return redirect(url_for('users.edit',id = user.id))
            else:
                flash(u"Can't change your new profile picture",'danger')
                return redirect(request.referrer)
        else:
            return redirect("/")
    else:
        return redirect("/")
    return render_template('/users/profile.html')

@users_blueprint.route('/private',methods = ['POST'])
@login_required
def private():
    user = User.get_or_none(User.id == current_user.id)
    if not user:
        flash('No user found.','warning')
        return redirect(url_for('users.edit', id = current_user.id))

    user.private = True

    if not user.save():
        flash("Can't change your account to private accound",'warning')
        return redirect(url_for('users.edit', id = current_user.id))

    flash('Successfully converted into private account','success')
    return redirect(url_for('users.edit', id = current_user.id))


