import dropbox


dbx = dropbox.Dropbox('nsRYGtrBcn0AAAAAAAAAAYUluU8qJX3ntIkardL8W5mGRLpCao3JPRB3yvjet6kF')


# def create(key, value):
#     dbx.files_create_folder(f'/{key}', autorename=False)
#     with open('w.txt', 'rb') as f:  ###
#         dbx.files_upload(f.read(), f"/{key}/{f}")
#
# create('ppapaala', 'sad')

"""
Helpers to deal with dropbox actions.
"""
import dropbox
import re
import logging


def upload_file(path, file):
    try:
        dbx.files_upload(file.read(), f'/{path}/value')
    except:
        pass


def read_file(path):
    _, f = dbx.files_download(f'/{path}/value')
    f = f.content
    return f


def dropbox_path_exists(path):
    """Checks if a given dropbox path exists.
    Args:
        path: string representation of the objects path.
        dbx: A dropbox api connection object.

    Returns True if the path exists else False.
    """
    path = f'/{path}'
    try:
        return dbx.files_get_metadata(path) is not None
    except dropbox.exceptions.ApiError as e:
        error_object = e.error
        if isinstance(error_object, dropbox.files.GetMetadataError) and error_object.is_path():
            base_error = error_object.get_path()
            if isinstance(base_error, dropbox.files.LookupError) and base_error.is_not_found():
                return False
            else:
                raise base_error
        else:
            raise error_object


def create_directory_at_path(path):
    """Creates a directory at the path. Expects that this does not point to a file.
    Args:
        path: string representation of the objects path with a leading "/".
        dbx: A dropbox api connection object.
    """
    # Check that the path does not end with a file extension.
    path = f'/{path}'
    if re.search(r"\.[^.]*$", path) is not None:
        raise ValueError("The path needs to be a directory path and not a file path. "
                         "{path} appears to be a file path.")
    # Create folder and disregard the dropbox.files.FolderMetadata object that's returned.
    _ = dbx.files_create_folder(path)
    logging.info(f"Created directory at path: \"{path}\"")


def get_directory_contents(directory):
    """Calls dropbox to retrieve contents of a directory.
    Args:
        directory: string value representing the dir path.

    Returns:
        A list of strings representing the file names in the directory path.
    """
    directory = f'/{directory}'
    content_to_return = []
    try:
        folder_contents = dbx.files_list_folder(directory)
    except dropbox.exceptions.ApiError as e:
        error_object = e.error
        if isinstance(error_object, dropbox.files.ListFolderError):
            base_error = error_object.get_path()
            if isinstance(base_error, dropbox.files.LookupError) and base_error.is_not_found():
                raise Exception(f"Dropbox cannot locate the object at path \"{directory}\".")
            else:
                raise base_error
        else:
            raise error_object

    # Get the dropbox objects contained within the folder
    directory_contents = folder_contents.entries
    while folder_contents.has_more:
        cursor = folder_contents.cursor
        folder_contents = dropbox.dropbox.Dropbox.files_list_folder_continue(cursor)
        directory_contents += folder_contents.entries

    # Save contents to file lists
    for fobj in directory_contents:
        if isinstance(fobj, dropbox.files.FileMetadata):
            content_to_return.append(fobj.name)
        else:
            logging.warn(f"The object type for \"{fobj.name}\" is not currently supported. "
                         "The object was not moved to a destination directory.")

    return content_to_return

def delete_file_from_path(path):
    path = f'/{path}'
    dbx.files_delete(path)