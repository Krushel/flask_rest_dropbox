import dropbox
import re
import logging


dbx = dropbox.Dropbox('')



def upload_file(path, file):
    dbx.files_upload(file.read(), f'/{path}/value')


def read_file(path):
    _, f = dbx.files_download(f'/{path}/value')
    f = f.content
    return f


def dropbox_path_exists(path):
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
    path = f'/{path}'
    if re.search(r"\.[^.]*$", path) is not None:
        raise ValueError("The path needs to be a directory path and not a file path. "
                         "{path} appears to be a file path.")
    _ = dbx.files_create_folder(path)
    logging.info(f"Created directory at path: \"{path}\"")


def delete_file_from_path(path):
    path = f'/{path}'
    dbx.files_delete(path)
