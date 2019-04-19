

class SDSTextDirectoryNotFound(Exception):
    def __init__(self, target_directory):
        Exception.__init__(self, f'{target_directory} for pre-extracted txt files does not exist')


class SDSDirectoryInvalidName(Exception):
    def __init__(self, directory):
        Exception.__init__(self, (f"'{directory}' is not a valid directory name. "
                                    "Directory name must match a supported "
                                    "manufacturer key. "
                                    "See sdsparser.Configs.SUPPORTED_MANUFACTURERS."))
