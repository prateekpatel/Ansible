from optparse import OptionParser
import ftplib
import os


f = ftplib.FTP('ppmitc-ftp', 'xbuild', 'xbuild')


def get_files(directory_name, dest_path='/root/playbook/output',
              source_path_to_file='/Docker/env/apache-ant-1.8.4/'):
    """

    :param directory_name:
    :param dest_path:
    :param source_path_to_file:
    :return:
    """
    print(directory_name)
    print(type(directory_name))

    print("changing path as per the given source path ---- %s" % source_path_to_file)
    f.cwd(source_path_to_file)
    current_path = f.pwd()
    print("This is the current working directory------> %s" % current_path)
    for directory in directory_name:
        f.cwd(directory)
        files = f.nlst()
        for filename in files:
            host_file = os.path.join(
                dest_path, filename)
            try:
                with open(host_file, 'wb') as local_file:
                    f.retrbinary('RETR ' + filename, local_file.write)
                    print("%s file got copied" % filename)
                    #os.system('ansible-playbook gitinstall2.yml --extra-vars "package=jdk-6u29-windows-i586.exe  deployment_start_time=`date`"')
                    os.system('ansible-playbook gitinstall2.yml --extra-vars "package=activation.jar  deployment_start_time=`date` ftp=ftp://ppmitc-ftp/ source_path_to_file=/Docker/env/apache-ant-1.8.4/ directory_name=lib/"')
                    exit(1)
            except ftplib.error_perm:
                pass
            # finally:
            #     f.cwd(current_path)

    f.quit()


parser = OptionParser(usage="usage: %prog [OPTIONS]")


parser.add_option("-s", "--ftp_server", type='string',
                  help="please provide the ftp server name",
                  dest="ftp_server")
parser.add_option("-d", "--directory", type="string",
                  action="append",
                  help=", seperated list of the directories name "
                       "which will be used to download the files",
                  dest="directory_name")


(options, args) = parser.parse_args()

if options.ftp_server and options.directory_name:
    print(type(options.ftp_server))
    print(options.directory_name)
    print(get_files(options.directory_name))
elif options.ftp_server:
    print("i m in the ftp server section")
    for dir_name in options.directory_name:
        print("get all the files and called ansible playbook")
else:
    parser.print_help()

