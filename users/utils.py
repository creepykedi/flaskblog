import secrets, os
from PIL import Image
from flask import url_for, current_app
from flaskblog import mail
from flask_mail import Message


def save_picture(form_picture):
    random_hex = secrets.token_hex(8) # 8 bytes
    # split name of file to name and extension. assign name to _ since we dont need it
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    # creating path to picture from full path to package directory + pic filename from folder
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    # resize pic to fit, using PIL
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    # save pic to filesystem
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    # to reset token we can pass seconds to expire, or leave blank to use default(we set 1800)
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@flaskblog.com', recipients=[user.email])
    # external means url outside of application
    msg.body = f""" To reset your password, visit the following link:
    {url_for('reset_token', token=token, _external=True)}

    If you didn't make this request then just ignore this email.
    """
    mail.send(msg)