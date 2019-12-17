


# pick a folder you have ...
def get_size(path):
    folder = path
    size = 0
    for (path, dirs, files) in os.walk(folder):
        for file in files:
            filename = os.path.join(path, file)
            size += os.path.getsize(filename)
            size = size / 1024 * 1024.0
            size = size / 1048576
    return size