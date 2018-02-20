import os
import threading


def move_files_with_extensions(src_dir, dest_dir, extentions):
    """
    :param src_dir: absolute path of source directory
    :param dest_dir: absolute path of destination directory
    :param extentions: List of extensions
    :return:
    """
    ensure_directory(dest_dir)
    dest = os.path.abspath(dest_dir)
    for ext in extentions:
        src = os.path.abspath(src_dir + '/*')
        if ext == '':
            # copy all files without any extention
            ext = '.'
        src = src + ext
        os.system('move /Y ' + src + ' ' + dest + ' > nul')


def move_all_files(src_dir, dest_dir):
    """
    Move all files in src_dir to dest_dir
    :param src_dir: Source Directory
    :param dest_dir: Destination Directory
    :return:
    """
    _, files = listdir(src_dir)
    file_types = []
    for f in files:
        ext = __get_extension(f)
        if ext not in file_types:
            file_types.append(ext)

    ensure_directory(dest_dir)
    dest = os.path.abspath(dest_dir)
    for ext in file_types:
        src = os.path.abspath(src_dir + '/*')
        if ext == '':
            # copy all files without any extention
            ext = '.'
        src = src + ext
        os.system('move /Y ' + src + ' ' + dest + ' > nul')


def move_file(abs_path, dest_dir):
    """
    Move single file to dest_dir
    :param abs_path: Absolute path of file
    :param dest_dir: Destination Directory
    :return:
    """
    os.system('move /Y ' + os.path.abspath(abs_path) + ' ' + os.path.abspath(dest_dir) + ' > nul')


def copy_files_with_extensions(src_dir, dest_dir, extentions):
    """
    Copy files from source directory to destination directory
    :param src_dir: Source directory on local system
    :param dest_dir: Destination directory on local system
    :param extentions: List of extensions
    :return:
    """
    ensure_directory(dest_dir)
    dest = os.path.abspath(dest_dir)
    for ext in extentions:
        src = os.path.abspath(src_dir + '/*')
        if ext == '':
            # copy all files without any extention
            ext = '.'
        src = src + ext
        os.system('copy ' + src + ' ' + dest + ' /y' + ' > nul')


def copy_all_files(src_dir, dest_dir):
    """
    Copy all files in src_dir to dest_dir
    :param src_dir: Source Directory
    :param dest_dir: Destination Directory
    :return:
    """
    _, files = listdir(src_dir)
    file_types = []
    for f in files:
        ext = __get_extension(f)
        if ext not in file_types:
            file_types.append(ext)

    ensure_directory(dest_dir)
    dest = os.path.abspath(dest_dir)
    for ext in file_types:
        src = os.path.abspath(src_dir + '/*')
        if ext == '':
            # copy all files without any extention
            ext = '.'
        src = src + ext
        command = 'copy ' + src + ' ' + dest + ' /y' + ' > nul'
        os.system(command)


def copy_file(src_path, dest_dir):
    """
    Copy single file to dest_dir
    :param src_path: Absolute path of file
    :param dest_dir: Destination Directory
    :return:
    """
    os.system('copy ' + os.path.abspath(src_path) + ' ' + os.path.abspath(dest_dir) + ' /y > nul')


def move_merge_folders(src_dir, dest_dir):
    """
    Moves and merges all folders in src_dir to dest_dir
    :param src_dir: Source Directory
    :param dest_dir: Destination Directory
    :return:
    """
    folders, _ = listdir(src_dir)
    for folder in folders:
        dest_path = os.path.abspath(dest_dir + '/' + folder)
        src_path = os.path.abspath(src_dir + '/' + folder)
        ensure_directory(dest_path)
        os.system('xcopy ' + src_path + ' ' + dest_path + ' /s /y' + ' > nul')
        remove_directory(src_path)


def copy_merge_folders(src_dir, dest_dir):
    """
    Copy folders from src_dir to dest_dir
    :param src_dir: Absolute path of source directory
    :param dest_dir: Absolute path of destination directory
    :return:
    """
    folders, _ = listdir(src_dir)
    for folder in folders:
        dest_path = os.path.abspath(dest_dir + '/' + folder)
        src_path = os.path.abspath(src_dir + '/' + folder)
        ensure_directory(dest_path)
        os.system('xcopy ' + src_path + ' ' + dest_path + ' /s /y' + ' > nul')


def write_filenames_with_extensions_to_file(src_dir, dest_file, extentions):
    """
    Writes Names of files with given extensions in src_folder to dest_file
    :param src_dir: Source directory to look into
    :param dest_file: Name of destination file
    :param extentions: List of extensions
    :return:
    """
    files = set()
    _, local_files = listdir(src_dir)
    for f in local_files:
        ext = __get_extension(f)
        if ext in extentions:
            files.add(f)

    write_to = open(dest_file, 'w')
    for name in files:
        write_to.write(name + '\n')

    write_to.close()


def write_all_filenames_to_file(src_dir, dest_file):
    """
    Writes Names of files with given extensions in src_folder to dest_file
    :param src_dir: Source directory to look into
    :param dest_file: Name of destination file
    :return:
    """
    _, files = listdir(src_dir)

    write_to = open(dest_file, 'w')
    for name in files:
        write_to.write(name + '\n')

    write_to.close()


def extract_zips(src_folder, dest_folder, delete_zips=True):
    """
    Extract the zip in the src_folder to dest_folder
    :param src_folder: Source Directory
    :param dest_folder: Destination Directory
    :param delete_zips: If true deletes the zips from src_folder
    :return:
    """
    zip_files = [f for f in os.listdir(src_folder) if f.endswith('.zip')]
    for zip_file in zip_files:
        zip_file = os.path.join(src_folder, zip_file)
        os.system('7z e ' + zip_file + ' -o' + dest_folder + ' -y' + ' > nul')
        if delete_zips:
            os.remove(zip_file)  # remove the zip file


def __get_extension(filename):
    tokens = filename.split('.')
    ext = tokens[-1]
    if len(tokens) == 1:
        # file has no extension
        ext = ''
    else:
        ext = '.' + ext
    return ext


def zip_files_with_extensions(src_folder, dest_path, file_types):
    """
    Zip given filetypes in src_folder into dest_path{zipfile}
    :param src_folder: Source Directory
    :param dest_path: Path of ZipFile
    :param file_types: List of fileTypes
    :return:
    """

    ext_string = ''
    for ftype in file_types:
        if ftype is not '':
            ext_string = ext_string + '*' + ftype + ' '
    lock = threading.Lock()
    with lock:
        _cwd = os.getcwd()
        os.chdir(src_folder)
        command = '7z a -t7z ' + os.path.abspath(dest_path) + ' ' + ext_string + ' -y' + ' > nul'
        os.system(command)

        # take care of extensionless files
        if '' in file_types:
            _, files = listdir(src_folder)
            for f in files:
                if __get_extension(f) is '':
                    command = '7z a -t7z ' + os.path.abspath(dest_path) + ' ' + f + ' -y' + ' > nul'
                    os.system(command)
        os.chdir(_cwd)


def zip_all_files(src_folder, dest_path):
    """
    Zip all the files in the folder
    :param src_folder: Source folder
    :param dest_path: Destination path of the zip
    :return:
    """
    ext_string = ''
    file_types = __get_file_types_in_folder(src_folder)
    for ftype in file_types:
        if ftype is not '':
            ext_string = ext_string + '*' + ftype + ' '
    lock = threading.Lock()
    with lock:
        _cwd = os.getcwd()
        os.chdir(src_folder)
        command = '7z a -t7z ' + os.path.abspath(dest_path) + ' ' + ext_string + ' -y' + ' > nul'
        os.system(command)

        # take care of extensionless files
        if '' in file_types:
            _, files = listdir(src_folder)
            for f in files:
                if __get_extension(f) is '':
                    command = '7z a -t7z ' + os.path.abspath(dest_path) + ' ' + f + ' -y' + ' > nul'
                    os.system(command)
        os.chdir(_cwd)


def __get_file_types_in_folder(src_folder):
    _, files = listdir(src_folder)
    file_types = []
    for f in files:
        ext = __get_extension(f)
        if ext not in file_types:
            file_types.append(ext)

    return file_types


def delete_files_except_extensions(src_folder, file_types):
    """
    Delete files except given extensions from src_folder
    :param src_folder: Source Folder
    :param file_types: List of file types
    :return:
    """
    _, files = listdir(src_folder)
    for f in files:
        tokens = f.split('.')
        ext = tokens[-1]
        if ext is f:
            # doens't have any extension
            ext = ''
        else:
            ext = '.' + ext

        if ext not in file_types:
            delete_file(src_folder + '/' + f)


def delete_files_with_extensions(src_folder, file_types):
    """
    Delete files with given extensions from src_folder
    :param src_folder: Source Folder
    :param file_types: List of file types
    :return:
    """
    for ext in file_types:
        src = os.path.abspath(src_folder)
        src = os.path.join(src, '*')
        if ext is '':
            src = src + '.'
            os.system('del /Q ' + src + ' > nul')  # delete all files without any extention
        else:
            src = src + ext
            os.system('del /Q ' + src + ' > nul')  # delete all files with ext extention


def delete_all_files(src_folder):
    """
    Deletes all files in the src_folder
    :param src_folder: Source Folder
    :return:
    """
    path = os.path.abspath(src_folder)
    path = os.path.join(path, '*.*')
    os.system('del ' + path + ' /Q')


def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)


def rename_file_extensions(src_folder, old_ext, new_ext):
    """
    Rename files in src_folder with old_ext to new_ext
    :param src_folder: Absolute path of source folder
    :param old_ext: Old Extension
    :param new_ext: New Extension
    :return:
    """
    src = os.path.abspath(src_folder)
    src = os.path.join(src, '*')

    if old_ext is '':
        src = src + '.'
        os.system("ren " + src + " *" + new_ext + ' > nul')  # rename unnamed samples to new_ext
    else:
        if new_ext is '':
            new_ext = '.'
        src = src + old_ext
        os.system("ren " + src + " *" + new_ext + ' > nul')


def ensure_directory(name):
    """
    Make directory structure if not exists
    :param name: Absolute path of directory
    :return:
    """
    if not os.path.exists(name):
        os.makedirs(name)


def remove_directory(directory):
    """
    Remove the directory and its contents
    :param directory: path of the directory to be removed
    :return:
    """
    directory = os.path.abspath(directory)
    os.system('rd /q /s ' + directory)


def listdir(directory):
    """
    List {Directories, Files}
    :param directory: Absolute path of the source directory to look into
    :return:
    """
    file_list, dirs, nondirs = [], [], []

    file_list = os.listdir(directory)
    for f_name in file_list:
        if os.path.isdir(os.path.join(directory, f_name)):
            dirs.append(f_name)
        else:
            nondirs.append(f_name)

    return dirs, nondirs


def absdir(file):
	"""
	:param file: __file__ should be explicitely passed
	:return: filepath of the file that this function is called in from whatever context
	"""
	absp = os.path.abspath(file)
	return os.path.dirname(absp)
