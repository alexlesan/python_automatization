import os, errno, sys, config
import argparse
import subprocess
import time

#parser arguments
parser = argparse.ArgumentParser(description='Create new local project')
parser.add_argument('--name', type=str, help='Name of the project')
parser.add_argument('--open', type=int, nargs='?', const=1, help='Open the editor with the project')


# make the directory of the project
def make_dir(domain):
    try:
        path_dir = config.PATH+domain
        os.mkdir(path_dir, config.ACCESS_RIGHTS)
        os.chmod(path_dir, config.ACCESS_RIGHTS)
        print ("Successfully created the directory: "+path_dir)
        make_nginx_file(domain)

    except OSError as e:
        str_error = e.strerror
        if e.errno == errno.EEXIST:
            str_error = "\tThe directory already exists."

        str = "\tCoudn't create the directory: "+path_dir+"."
        print(str)
        print(str_error)

# make the nginx site-availables file and link to enabled-sites
def make_nginx_file(domain):
    try:
        filename_loc = domain+".loc"
        full_path = config.NGINX_SITE_AVAILABLES_PATH+filename_loc
        site_enabled_path = config.NGINX_SITE_ENABLED_PATH+filename_loc

        #replace in file template and copy to nginx
        temp_file = open(config.TEMPLATE_VH, 'r')
        dest_file = open(full_path, 'w')
        file_lines = temp_file.readlines()

        for line in file_lines:
            res = line.replace("{PROJECT_NAME}", domain)
            dest_file.write(res.replace("{SERVER_NAME}", filename_loc))

        temp_file.close()
        dest_file.close()

        #create the symlink to site-enabled
        os.symlink(full_path, site_enabled_path)
        print("Symlink was created.")
        #update the hosts file
        update_hosts_file(domain)

        #restart the nginx server
        restart_nginx()

    except OSError as e:
        print (e.strerror)

# update the hosts file with new virutal host url
def update_hosts_file(domain):
    try:
        str_line = "\n127.0.0.1\t"+domain.lower()+".loc"
        with open(config.HOSTS_FILE_PATH, 'a') as f:
            f.write(str_line)
        print("Hosts file was updated.")

    except OSError as e:
        print(e.strerror)

# restart the engin server after modifications
def restart_nginx():
    try:
        #restart the nginx
        command_str = "sudo systemctl restart nginx"
        os.system(command_str)
        print("The nginx server was restarted successfully")

    except:
        print("Coudn't restart the nginx server")


# check and run the command
if __name__ == '__main__':
    param = vars(parser.parse_args())
    domain = param['name'].lower()
    open_editor = param['open']
    if domain != '':
        make_dir(domain)
        if open_editor == 1:
            # open the project in atom editor
            print("\t Opening the Atom editor...")
            # atom_cmd = ["atom", config.PATH+domain]
            # subprocess.Popen(atom_cmd).wait()
            os.system('atom '+config.PATH+domain)
            time.sleep(1)
            print("\t The process was finished.")
    else:
        print("No domain name was provided.")
