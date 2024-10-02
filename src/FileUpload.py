# Purpose: This file keeps track of the previous script & image uploaded by the user, specifically its name, extension, and contents.
class FileUpload():
    def __init__(self):
     self.default = None
     self.prevUpload = self.default
     self.sendFile = None
     self.image = None

    def set_prevUpload(self, file_ext, file_contents, file_name):
     self.prevUpload = (file_ext, file_contents, file_name)
     
    def didUserUploadFile(self):
        if self.default == self.prevUpload:
            return False
        else:
            return True
        
    def didUserUploadImage(self):
        if self.image is None:
            return False
        else:
            return True
    