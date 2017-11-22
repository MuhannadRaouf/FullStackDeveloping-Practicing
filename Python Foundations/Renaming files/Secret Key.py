import os
def rename_file():
    files_list = os.listdir(r"F:\Full stack developing\Lesson 2\prank")
    print(files_list)
    os.chdir(r"F:\Full stack developing\Lesson 2\prank")
    for file_name in files_list:
        os.rename(file_name, file_name.strip("0123456789"))
rename_file()
