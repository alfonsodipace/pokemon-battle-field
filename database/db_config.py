from configparser import ConfigParser


def get_db_info(filename, section):
    """
    Get the database information from the db_info.ini file
    :param filename: the name of the file
    :param section: the section of the file
    :return: the database information
    """
    # instantiating the parser object
    parser = ConfigParser()
    parser.read(filename)

    db_info = {}
    if parser.has_section(section):
        # items() method returns (key,value) tuples
        key_val_tuple = parser.items(section)
        for item in key_val_tuple:
            db_info[item[0]] = item[1]  # index 0: key & index 1: value

    return db_info
