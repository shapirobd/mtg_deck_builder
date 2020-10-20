from flask import Blueprint, render_template

second = Blueprint('second', __name__, static_foler='static',
                   template_folder='templates')


@second.route('/home')
@second.route('/')
def welcome():
    """
    If we're not logged in, show the welcome page to login/signup.
    If we are logged in, show the user's home page.
    """
    if not g.user:
        return render_template('welcome.html')

    return redirect('/home')
