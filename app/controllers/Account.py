from flask import Blueprint, flash, redirect, render_template, request, url_for, session, jsonify
from flask import current_app as flask_app
from app.models.Account import Account

bp = Blueprint('account', __name__, url_prefix='', static_folder='../static')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """ 
    Registration controller. 
  
    Presents the registration view and handles registration requests. 
  
    Returns: 
    obj: Either render_template or redirect
  
    """

    if request.method == 'POST':
        error = None
        try:
            # Get account singleton and try register user
            account = Account()
            user = account.register(request)
        except Exception as err:
            # Registration error to be flashed
            error = err
        if error:
            flash(str(error))
        else:
            # Registration successful so redirect
            flash("Please login to get started!")
            return redirect(url_for('account.login'))

    return render_template('account/register.html')
    
@bp.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        error = None
        try:
            # Get account singleton and try login
            account = Account()
            user = account.login(request)
        except Exception as err:
            # Login error to be flashed
            error = err
        if error:
            flash(str(error))
        else:
            # Login successful so redirect
            flash("Welcome back!")
            return redirect(url_for('account.profile'))

    return render_template('account/login.html')
    
@bp.route('/profile', methods=['GET', 'POST'])
def profile():

    if request.method == 'POST':
        error = None
        try:
            # Get account singleton and update account infomation request.
            account = Account()
            user = account.update(request)
            flash("Your details have been updated")
        except Exception as err:
            # Flash Proflie Update Error
            error = err
        if error:
            flash(str(error))

    return render_template('account/profile.html')
    
@bp.route('/logout')
def logout():
    # Logs out account and redirects to home page.
    account = Account()
    account.logout()
    return redirect(url_for('home.index'))

@bp.route('/like', methods=['GET'])
def like():
    # Requests Image_Id and sends it to flask and proccess the image to liked status on the account.
    image_id = request.args.get('image_id')
    like = request.args.get('like')
    flask_app.logger.info('## LIKE VAL CT ##')
    flask_app.logger.info(request.args.get('like'))
    # Pulls like infomation 
    flask_app.logger.info(like)
    response = ''

    try:
        # Pulls account singleton and sends Image Id, Like (True or False), and the request to change the liked status
        account = Account()
        response = account.like(image_id, like, request)
        # Returns Error as a string
    except Exception as err:
        response = str(err)
    
    return jsonify(response)
