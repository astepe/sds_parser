

class FileMatchNotFound(Exception):
    def __init__(self, file_name, target_directory):
        Exception.__init__(self, f'No matching .txt file found for {file_name} in {target_directory}')


class TextDirectoryDoesNotExist(Exception):
    def __init__(self, target_directory):
        Exception.__init__(self, f'No matching txt directory found for {target_directory}')


class ManufacturerNotSupported(Exception):
    def __init__(self, manufacturer_name):
        Exception.__init__(self, f'{manufacturer_name} is not a currently supported manufacturer')
