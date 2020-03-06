from flask import Blueprint, render_template, request, redirect, url_for, session,flash
from flask_login import current_user, login_required
from instagram_web.util.braintree import gateway
from models.donations import Donations
from models.user import User
from models.user_images import Image
import os
import requests

donations_blueprint = Blueprint('donations',
                            __name__,
                            template_folder='templates')

def send_simple_message(sender,reciever,amount):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxda765cad09c94ef0900b089909d980a8.mailgun.org/messages",
        auth=("api", os.getenv('MAILGUN_API_KEY')),
        data={"from": "Nextagram <nextagram_testing@gmail.com>",
              "to": ["zhongvei@gmail.com"],
              "subject": "Appreciation for donation",
              "text": f"Thank you for your donation! Successfully donated RM{amount} to {reciever} from {sender}"})

@donations_blueprint.route('/<img_id>', methods = ['GET'])
@login_required
def new(img_id):
    client_token = gateway.client_token.generate()
    image = Image.get_or_none(Image.id == img_id)
    return render_template('/donations/new.html',image = image, client_token = client_token)

@donations_blueprint.route('<img_id>', methods = ['POST'])
@login_required
def create(img_id):

    nonce = request.form.get('payment_method_nonce')

    amount = request.form.get('amount')

    result = gateway.transaction.sale({
    "amount": amount,
    "payment_method_nonce": nonce,
    "options": {
      "submit_for_settlement": True
    }
    })

    if result.is_success:
        donation = Donations(amount = amount, image = img_id, user = current_user.id )
        image = Image.get_or_none(Image.id == img_id)
        user = User.get_or_none(User.id == image.user_id)
        donation.save()
        if not donation.save():
            flash(u'Data not saved in database!','warning')
            return redirect(url_for('donations.new'))
        #mailgun
        # send_simple_message(amount = amount, sender = current_user.name, reciever = user.name)
        flash(u'Donation is made','success')
        return redirect(url_for('users.index'))

    else:
        flash(u'Donation not successfully made, please check the amount of your donation','warning')
        return redirect(url_for('users.index'))