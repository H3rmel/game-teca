import os

from gameteca import app

"""
    Retrieves the image file name for a given ID.

    Parameters:
        id (int): The ID of the image.

    Returns:
        str: The image file name if found, otherwise 'default_cover.jpg'.
"""
def get_image(id):
    for name_archive in os.listdir(app.config['UPLOAD_PATH']):
        if f'cover{id}' in name_archive:
            return name_archive
    
    return 'default_cover.jpg'


"""
    Deletes an image from the server.

    Parameters:
        id (int): The ID of the image to be deleted.

    Returns:
        None
"""
def delete_image(id):
    archive = get_image(id)
    
    if archive != 'default_cover.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], archive))