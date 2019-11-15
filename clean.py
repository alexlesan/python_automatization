import os
import errno
import sys
import config
import argparse

# parser arguments
parser = argparse.ArgumentParser(
    description='Clean the project from localhost')
parser.add_argument('--name', type=str, help='Name of the project')

# check if the project's folder exists in www


def check_www_folder_exists(domain_name):
    folder_path = config.PATH + domain_name
    if os.path.exists(folder_path):
        print("The folder exists, will continue the cleaning.")
        return True
    else:
        print("The folder wasn't found in www.")
        return False

# remove all data about the project


def clean_data(domain):
    try:
        check_www_folder_exists(domain)
        # remove the folder from www
        clean_www_folder(domain)
        # remove configs from nginx server
        clean_nginx_files(domain)
        # remove line from hosts file
        clean_hosts_file(domain)

    except OSError as e:
        print(e.strerror)

# remove the project's folder from www


def clean_www_folder(domain_name):
    try:
        # delete the folder from www
        folder_path = config.PATH + domain_name
        my_command = "rm -rf " + folder_path
        os.system(my_command)
        print("The folder was removed")

    except OSError as e:
        print(e.strerror)

# clean nginx files


def clean_nginx_files(domain_name):
    try:
        # delete sites-availables and sites-enabled files
        file_name = domain_name + config.LOCAL_DOMAIN_EXT
        sites_available_path = config.NGINX_SITE_AVAILABLES_PATH + file_name
        sites_enabled_path = config.NGINX_SITE_ENABLED_PATH + file_name
        my_command = "rm -rf " + sites_available_path + " " + sites_enabled_path
        os.system(my_command)
        print("Nginx configuration files were removed.")

    except OSError as e:
        print(e.strerror)


# clean the hosts file
def clean_hosts_file(domain_name):
    try:
        domain = domain_name + config.LOCAL_DOMAIN_EXT
        hosts_path = config.HOSTS_FILE_PATH
        with open(hosts_path, 'r+') as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                if domain not in line:
                    file.write(line)
            file.truncate()

        print("The domain was removed from hosts file")

    except OSError as e:
        print(e.strerror)


# run methods to clean project
if __name__ == '__main__':
    param = vars(parser.parse_args())
    domain = param['name'].lower()
    print("Started the cleaning process.")
    clean_data(domain)
    #clean_hosts_file(domain)
    print("Finished the cleaning process.")
else:
    print("No name of the project was specified.")
