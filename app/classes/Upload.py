import os
from flask import Flask, flash, request, redirect, url_for
from flask import current_app as flask_app
from app import SITE_ROOT

class Upload():
    """
    Allows for PNG, JPG, JPEG, GIF to be uploaded on the website
    """
    def __init__(self):
        self.extensions = {'png', 'jpg', 'jpeg', 'gif'}

    # Checks for allowed extention of PNG, JPG, JPEG, 
    # and GIF if something else it doesnt allows upload 
    # and displays the values of the allowed file types
    def upload(self, file, filename):
        allowed_extension = self.allowed_file(file.filename)
        if allowed_extension:
            fullname = filename + '.' + allowed_extension
            destination = os.path.join('static/uploads', fullname)
            file.save(os.path.join(SITE_ROOT, destination))
            return destination
        else:
            raise Exception("Only allowed filetypes: ".join(self.extensions.values()))

    # Explodes the last dot to a list and 
    # checks it against a list of allowed file extenstions.
    def allowed_file(self, filename):
        if ('.' in filename and filename.rsplit('.', 1)[1].lower() in self.extensions):
            return filename.rsplit('.', 1)[1].lower()
        return False