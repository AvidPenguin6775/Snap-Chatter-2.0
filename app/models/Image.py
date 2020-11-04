from app.classes.Database import Database
from app.classes.Upload import Upload
from app.models.User import User
from flask import session
from flask import current_app as flask_app
import uuid, time

class Image():

# 
    def __init__(self):
        return None

 # Simple DB Request for images with a limit of 20
    def get_images(self, limit=20):
        # Inital Variable Values
        error = None
        images = False

        try:
            # Pull images from database with the limit in place.
            database = Database()
            images = database.get_images(limit)

        except Exception as err:
            flask_app.logger.info(err)
            error = err

        if error:
            raise Exception(error)
        else:
            # Successfully returned pyrebase objects
            return images
    # Gets the images for the catergory that gets passed in.
    # Limits the results set to 20 images
    def get_category_images(self, category, limit=20):
        
        # Inital Variable Values
        error = None
        images = False
        
        #Tries to get the images
        try:
            database = Database()
            images = database.get_category_images(category, limit)
        # Failed to get images raise a exception 
        except Exception as err:
            flask_app.logger.info(err)
            error = err
        # Check if we have an error
        if error:
            # We have error, pass it back to the controller
            raise Exception(error)
        else:
            # We have no errors, return images
            return images

    def get_image(self, image_id):
        # Inital Variable Values
        error = None
        image = False
        #Tries to pull image id
        try:
            database = Database()
            image = database.get_image(image_id)
        # Failed to get images raise a exception.
        except Exception as err:
            flask_app.logger.info(err)
            error = err
        #Check if we have an error
        if error:
            # We have error, pass it back to controller
            raise Exception(error)
        else:
            # We have no errors, return images
            return image

    def delete_image(self, image_id):
        # Inital Variable Values
        error = None
        # Tries to delete image id in database.
        try:
            database = Database()
            database.delete_image(image_id)
        # Failed to get delete image raise a exception
        except Exception as err:
            flask_app.logger.info(err)
            error = err

        if error:
            # We have error, pass it back to controller
            raise Exception(error)
        else: 
            # We have no errors, return
            return
    #Pulls user specific images with a limit of 20
    def get_user_images(self, limit=20):
        # Inital Variable Values
        error = None
        images = False
        user_id = False
        #Checks for images that have been uploaded by the sesson user.
        if (session['user'] and session['user']['localId']):
            user_id = session['user']['localId']
        try:
            #Pulls images from database with a limit of 20 
            #and has the same user_id
            database = Database()
            images = database.get_images(limit, user_id)

        except Exception as err:
            # We have error, pass it back to controller
            flask_app.logger.info(err)
            error = err

        if error:
            # We have error, pass it back to controller
            raise Exception(error)
        else:
            # We have no errors, return images
            return images
    #Creates request to server for image upload
    def upload(self, request):
        # sets data base variables to the form requests infomation.
        image_id        = str(uuid.uuid1())
        name            = request.form['name']
        description     = request.form['description']
        category        = request.form['category']
        image_filter    = request.form['filter']

        # Validates required registration fields
        error = None
        user_id = False
        # Pulls session user and local_Id to attack to image.
        # Also checks in their is a user login in the session.
        if (session['user'] and session['user']['localId']):
            user_id     = session['user']['localId']
            user_name   = session['user']['first_name'] + " " + session['user']['last_name']
            user_avatar = session['user']['avatar']
        else: 
            # Displays readable error
            error = 'You must be logged in to upload an image.'
            # Checks request file for a image file
        if 'image' not in request.files:
            # If image file isnt found display readable error.
            error = 'A file is required.'
        else:
            #Re-request the image file.
            file = request.files['image']
        #List of readable errors
        if not error:
            # If file isnt present display error
            if file.filename == '':
                error = 'A file is required.'
                # If name blank display error
            elif not name:
                error = 'An name is required.'
                # If Description is blank display error
            elif not description:
                error = 'A description is required.'
                # If category is blank display error
            elif not category:
                error = 'A category is required.'
            else:
                try:
                    # sets image data to all the data that makes up the image
                    uploader = Upload()
                    upload_location = uploader.upload(file, image_id)
                    image_data = {
                        "id":                   image_id,
                        "upload_location":      '/' + upload_location,
                        "user_id":              user_id,
                        "user_name":            user_name,
                        "user_avatar":          user_avatar,
                        "name":                 name,
                        "description":          description,
                        "category":             category,
                        "filter":               image_filter,
                        "created_at":           int(time.time())
                    }
                    database = Database()
                    # Uploads and saves image data to database
                    uploaded = database.save_image(image_data, image_id)
                except Exception as err:
                    error = err
        if error:
            # We have error, pass it back to controller 
            # and display a readable error in git
            flask_app.logger.info('################ UPLOAD ERROR #######################')
            flask_app.logger.info(error)
            raise Exception(error)
        else:
            # We have no errors, return image_id
            return image_id

    def update(self, image_id, request):
        
        # sets data base variables to the form requests infomation.
        name            = request.form['name']
        description     = request.form['description']
        category        = request.form['category']
        image_filter    = request.form['filter']
        created_at      = request.form['created_at'] 
        upload_location = request.form['upload_location']  

        # Validates required registration fields
        error = None
        user_id = False
        # Pulls session user and local_Id to attack to image.
        # Also checks in their is a user login in the session.
        if (session['user'] and session['user']['localId']):
            user_id     = session['user']['localId']
            user_name   = session['user']['first_name'] + " " + session['user']['last_name']
            user_avatar = session['user']['avatar']
        else: 
            # display error if the user isnt logged in
            error = 'You must be logged in to update an image.'
        # Readable Errors
        if not error:
            # If infomation is missing display readable error
            if not name:
                error = 'An name is required.'
            elif not description:
                error = 'A description is required.'
            elif not category:
                error = 'A category is required.'
            else:
                # Updates the image data of the image before sending to database.
                try:
                    image_data = {
                        "id":                   image_id,
                        "upload_location":      upload_location,
                        "user_id":              user_id,
                        "user_name":            user_name,
                        "user_avatar":          user_avatar,
                        "name":                 name,
                        "description":          description,
                        "category":             category,
                        "filter":               image_filter,
                        "created_at":           created_at
                    }
                    database = Database()
                    # uploads image data and image id to database.
                    uploaded = database.save_image(image_data, image_id)
                except Exception as err:
                    error = err
        if error:
            # We have error, pass it back to controller 
            # and display a readable error in git
            flask_app.logger.info('################ UPDATE ERROR #######################')
            flask_app.logger.info(error)
            raise Exception(error)
        else:
            # Return data 
            return