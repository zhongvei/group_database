from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from models.user_images import Image
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
from instagram_web.util.helpers import upload_file_to_s3

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')

@images_blueprint.route('/<username>/upload_my_image', methods= ['POST'])
@login_required
def create(username):
    file = request.files["user_file"]
    user = User.get_or_none(User.id == current_user.id)
    image = Image(image_path = file.filename, user_id = user.id)
    upload_file_to_s3(file)
    image.save()
    flash(u'Image saved successfully!' ,'success')
    return redirect(url_for('users.show', username = username))

