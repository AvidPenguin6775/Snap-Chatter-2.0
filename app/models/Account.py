from app.classes.Database import Database
from app.classes.Upload import Upload
from app.models.User import User
from flask import session, flash
from flask import current_app as flask_app

class Account():

    def __init__(self):
        self.user = User()
        return None

    def register(self, request):
        """ 
        Registration method. 
    
        Processes POST request, and registers user in Firebase on success

        Parameters: 
            request (obj): The POST request object
    
        Raises: 
            error (Exception): Error from failed Firebase request
    
        """

        # Extract required fields from POST request
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['password_confirm']

        # Validates required registration fields
        error = None
        if not email:
            error = 'An email is required.'
        elif not password:
            error = 'Password is required.'
        elif 6 > len(password):
            error = 'Your password must be at least 6 characters long.'
        elif not password_confirm:
            error = 'Password confirmation is required.'
        elif password != password_confirm:
            error = 'Password and password confirmation should match.'
        else:
            try:
                user_data = {
                    "localId": "",
                    "email": email,
                    "first_name": "",
                    "last_name": "",
                    "avatar": ""
                }
                # Attempt to process valid registration request
                database = Database()
                user_auth = database.register(user_data, password)
            except Exception as err:
                # Raise error from failed Firebase request
                error = err
        if error:
            # Raise error from failed Firebase request
            raise Exception(error)
        else:
            # Return on success
            return
        # Requests infomation about login infomation from database.
    def login(self, request):
        if request.method == 'POST':
            # reuqests form infomation for email, and password.
            email = request.form['email']
            password = request.form['password']

            error = None
            if not email:
                # No email gotten in the request, push readable error
                error = 'An email is required.'
            elif not password:
                # No password pulled in the request, push readable error
                error = 'Password is required.'
            else:
                try:
                    # Pulls infomation about email and password from database.
                    database = Database()
                    user = database.login(email, password)
                    # TODO Remove for production
                    #flask_app.logger.info(user)
                    self.user.set_user(user)
                except Exception as err:
                    error = err

        if error:
            raise Exception(error)
        else:
            return
        # Requests infomation about firstname and lastname.
    def update(self, request):
        if request.method == 'POST':
            # request form infomation for firstname, and lastname.
            first_name = request.form['firstname']
            last_name = request.form['lastname']

            error = None
            if not first_name:
                # If error / empty field with the firstname will display readable error
                error = 'A first name is required.'
            elif not last_name:
                # If error / empty field with the lastname will display readable error
                error = 'A last name is required.'
            else:
                # If avatar is in request files
                if 'avatar' in request.files:
                    # Request the avatar files
                    file = request.files['avatar']
                    if file.filename:
                        # Pulls avatar, user and localid from session data. 
                        uploader = Upload()
                        avatar = uploader.upload(file, session['user']['localId'])
                        session['user']['avatar'] = "/" + avatar.strip("/")
                try:
                    # sets session users firstname and lastname to firstname and lastname.
                    session['user']['first_name'] = first_name
                    session['user']['last_name'] = last_name
                    database = Database()
                    user_auth = database.update_user(session['user'])
                    session.modified = True
                except Exception as err:
                    error = err

        if error:
            raise Exception(error)
        else:
            return
        # Like function code.
    def like(self, image_id, like, request):
                
        changed = False
        #Checks in the image like data is true or false 
        # and displays the approriate heart.
        likes = session['user']['likes']
        #If like = true and the image_id isnt in likes in the database 
        #add it to database with like being set to true
        if like == 'true':
            if image_id not in likes:
                likes.append(image_id)
                changed = True
        else:
            # If Image_id is in likes, remove image_id from likes.
            if image_id in likes:
                likes.remove(image_id)
                changed = True

        if changed:
            # If changed change appearance of the heart on screen 
            # by pulling the data from the database
            session['user']['likes'] = likes
            database = Database()
            database.update_user(session['user'])
            session.modified = True

        return changed
        
        # Logsout by unseting the user in the session.
    def logout(self):
        self.user.unset_user()

