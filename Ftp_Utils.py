import ftplib
import os
import File_Utils as f_utils
import threading


# All the paths passed to methods should be absolute

class FileNotFoundError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class FTP_UTIL(ftplib.FTP):
    def __init__(self, host, username=None, password=None):
        self.username = username
        self.password = password
        self.host = host
        ftplib.FTP.__init__(self, host, username, password)
        if not username:
            self.login()
        self._cwd = '/'
        self.ensure_connection()

    def ensure_connection(self):
        try:
            self.pwd()
        except:
            ftplib.FTP.__init__(self, self.host, self.username, self.password)
            if not self.username:
                self.login()
            self.cwd(self._cwd)

    def cwd(self, dirname):
        self.ensure_connection()
        self._cwd = dirname
        ftplib.FTP.cwd(self, dirname)

    @staticmethod
    def filename_from_absolute(abspath):
        replacements = ('/', '\\')
        temp = abspath
        for r in replacements:
            temp = temp.replace(r, '@@')
        tokens = temp.split('@@')
        return tokens[-1]

    def download_files_with_extensions(self, local_folder, ftp_folder, file_types, ensure_connection=True):
        """
        :param ensure_connection:
        :param local_folder: Folder on local system where files will be donwloaded
        :param ftp_folder: Folder on ftp where files will be looked for
        :param file_types: List of file extensions that will be downloaded. '' means all extensionless files,
        '.' means all files.
        :return:
        """
        if ensure_connection:
            self.ensure_connection()
        _, files = self.listdir(ftp_folder)

        for f in files:
            ext = self.__get_extension(f)
            # ext of the form <.ext> or '' (empty string indicating all extensionless files)
            if ext in file_types:
                ftp_abs_path = ftp_folder + '/' + f
                self.download_file_from_ftp(local_folder, ftp_abs_path, False)

    def download_all_files(self, local_folder, ftp_folder, ensure_connection=True):
        """
        Downloads all files in the ftp_folder to local folder
        :param ensure_connection:
        :param local_folder: Local folder on the system where files will be donwloaded
        :param ftp_folder: Folder on the ftp from where files will be downloaded
        :return:
        """
        if ensure_connection:
            self.ensure_connection()
        _, files = self.listdir(ftp_folder)
        for f in files:
            ftp_abs_path = ftp_folder + '/' + f
            self.download_file_from_ftp(local_folder, ftp_abs_path, False)

    def download_file_from_ftp(self, localfolder,  ftp_abs_path, ensure_connection=True):
        """
        :param ensure_connection:
        :param localfolder: Folder on local system where file will be downloaded
        :param ftp_abs_path: Absolute path of file on ftp that is to be downloaded
        :return: null
        """
        if ensure_connection:
            self.ensure_connection()
        filename = FTP_UTIL.filename_from_absolute(ftp_abs_path)
        localfile = open(os.path.join(localfolder, filename), 'wb')
        try:
            self.retrbinary('RETR %s' % ftp_abs_path, localfile.write)
        except ftplib.error_perm as e:
            print e
            raise FileNotFoundError("Couldn't find " + filename)
        localfile.close()

    def upload_files_with_extensions(self, local_folder, ftp_folder, file_types, ensure_connection=True):
        """
        Uploads files with given extension. '' means all extensionless files
        :param ensure_connection:
        :param local_folder: Folder on the local system
        :param ftp_folder: Folder on the ftp
        :param file_types: List of filetypes to upload. '' means extensionless files,
        '.' means all files.
        :return:
        """
        if ensure_connection:
            self.ensure_connection()

        _, files = f_utils.listdir(local_folder)  # lists files and folders in cwd
        for f in files:
            ext = self.__get_extension(f)
            if ext in file_types:
                self.upload_file_to_ftp(os.path.join(local_folder, f), ftp_folder, False)

    def upload_all_files(self, local_folder, ftp_folder, ensure_connection=True):
        """
        Upload all files in the local folder to the ftp_folder
        :param ensure_connection:
        :param local_folder: Local folder on the system whose all files will be uploaded
        :param ftp_folder: Folder on ftp where all files will be uploaded
        :return:
        """
        if ensure_connection:
            self.ensure_connection()
        _, files = f_utils.listdir(local_folder)  # lists files and folders in cwd
        for f in files:
            abs_filepath = os.path.join(local_folder, f)
            self.upload_file_to_ftp(abs_filepath, ftp_folder, False)

    def upload_file_to_ftp(self, abs_filepath, ftp_folder, ensure_connection=True):
        """
        Upload a file to ftp
        :param ensure_connection:
        :param abs_filepath: Absolute filepath on local system
        :param ftp_folder: Folder on ftp where file will be uploaded
        :return:
        """
        if ensure_connection:
            self.ensure_connection()
        if not os.path.isfile(abs_filepath):
            open(abs_filepath, 'a').close()  # file didn't exist , so create an empty file
        filename = FTP_UTIL.filename_from_absolute(abs_filepath)
        ftp_file = ftp_folder + '/' + filename
        self.storbinary('STOR ' + ftp_file, open(abs_filepath, 'rb'))

    def delete_files_with_extensions(self, ftp_folder, file_types, ensure_connection=True):
        """
        Delete all the files with given extensions in the ftp folder
        :param ensure_connection:
        :param ftp_folder: Folder on the FTP
        :param file_types: List of file types. '' means extensionless files,
        '.' means all files.
        :return:
        """
        if ensure_connection:
            self.ensure_connection()

        _, files = self.listdir(ftp_folder)

        for f in files:
            ext = self.__get_extension(f)
            # ext of the form <.ext> or '' (empty string indicating all extensionless files)
            if ext in file_types:
                self.delete(ftp_folder + '/' + f)

    def delete_all_files(self, ftp_folder, ensure_connection=True):
        """
        Deletes all files
        :param ensure_connection:
        :param ftp_folder: Folder on ftp from where all files will be deleted
        :return:
        """
        if ensure_connection:
            self.ensure_connection()
        _, files = self.listdir(ftp_folder)
        for f in files:
            self.delete(ftp_folder + '/' + f)

    def delete_file_from_ftp(self, abs_filepath, ensure_connection=True):
        """
        Deletes file from ftp
        :param ensure_connection:
        :param abs_filepath:
        :return:
        """
        if ensure_connection:
            self.ensure_connection()
        self.delete(abs_filepath)

    def __get_extension(self, filename, ensure_connection=True):
        if ensure_connection:
            self.ensure_connection()
        tokens = filename.split('.')
        ext = tokens[-1]
        if len(tokens) == 1:
            # file has no extension
            ext = ''
        else:
            ext = '.' + ext
        return ext

    def path_exists(self, absolute_path, ensure_connection=True):
        """
        Returns true if the given absolute folder path exists
        :param ensure_connection:
        :param absolute_path: Absolute folder path on FTP
        :return: Boolean
        """
        lock = threading.Lock()
        with lock:
            if ensure_connection:
                self.ensure_connection()
            _pwd = self.pwd()
            exists = True
            try:
                self.cwd(absolute_path)
            except ftplib.error_perm, resp:
                exists = False
            self.cwd(_pwd)

        return exists

    def ensure_directory(self, absolute_path, ensure_connection=True):
        """
        Makes the folder structure if not exists
        :param ensure_connection:
        :param absolute_path: Absoulute path of the folder
        :return:
        """
        lock = threading.Lock()
        with lock:
            if ensure_connection:
                self.ensure_connection()
            _cwd = self.pwd()
            folders = absolute_path.split('/')
            folders[:] = [f for f in folders if f is not '']  # removes empty strings
            self.cwd('/')  # at the root
            for folder in folders:
                try:
                    self.cwd(folder)
                except ftplib.error_perm, resp:
                    self.mkd(folder)
                    self.cwd(folder)

            self.cwd(_cwd)

    def listdir(self, absolute_path, ensure_connection=True):
        """
        Returns {Directories, Files}
        :param ensure_connection:
        :param absolute_path: Absolute path on the ftp
        :return:
        """
        lock = threading.Lock()
        with lock:
            if ensure_connection:
                self.ensure_connection()
            _cwd = self.pwd()
            file_list, dirs, nondirs = [], [], []
            if not self.path_exists(absolute_path):
                return [], []
            else:
                self.cwd(absolute_path)
                self.retrlines('LIST', lambda x: file_list.append(x.split()))
                for info in file_list:
                    if 'dir' in info[2].lower():
                        #     this is directory
                        dirs.append(' '.join(info[3:]))
                    else:
                        nondirs.append(' '.join(info[3:]))
                    # name = info[8:]
                    # name = ' '.join(name)
                    # ls_type, name = info[0], name
                    # if ls_type.startswith('d'):
                    #     
                    # else:
                    #     nondirs.append(name)
            self.cwd(_cwd)

        return dirs, nondirs
