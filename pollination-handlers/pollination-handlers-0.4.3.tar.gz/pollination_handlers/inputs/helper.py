import os
import tempfile
import uuid


def get_tempfile(extension, file_name=None):
    """Get full path to a temporary file with extension."""
    file_name = str(uuid.uuid4())[:6] if file_name is None \
        or file_name == '-' else file_name
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, '%s.%s' % (file_name, extension))
    return file_path
