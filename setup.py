import os 
import tempfile

dir_path = os.path.dirname(os.path.realpath(__file__))
username = os.getlogin()
home = os.path.expanduser("~")

linkmap = {
	"jmeter.properties":"/opt/jmeter/bin/",
	"config":"/home/haswell/.i3/",
	".zshrc":home,
	".Xresources":home,
	".xprofile":home,
	".xinitrc":home,
	".gitconfig":home,
	"pacman.conf":"/etc/"
}



def symlink_force(target, link_name):
    '''
    Create a symbolic link link_name pointing to target.
    Overwrites link_name if it exists.
    https://stackoverflow.com/questions/55740417/atomic-ln-sf-in-python-symlink-overwriting-exsting-file
    '''

    # os.replace() may fail if files are on different filesystems
    link_dir = os.path.dirname(link_name)

    while True:
        temp_link_name = tempfile.mktemp(dir=link_dir)
        try:
            os.symlink(target, temp_link_name)
            break
        except FileExistsError:
            pass
    try:
        os.replace(temp_link_name, link_name)
    except OSError:  # e.g. permission denied
        os.remove(temp_link_name)
        raise

if __name__ == "__main__":
	for file in linkmap:
		src = os.path.join(dir_path, file)
		dest = os.path.join(linkmap[file], file)
		symlink_force(src, dest)
		print("Symbolic link for",file,"created ")

