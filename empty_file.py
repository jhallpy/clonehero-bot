import os
import shutil

folder_path = "data/images"


def clear_file():
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            os.rmdir(file_path)
        else:
            print("Error deleting files.")


# def clear_trash():
#     trash_folder = os.path.expanduser("~\\Recycle Bin")
#     for filename in os.listdir(trash_folder):
#         file_path = os.path.join(trash_folder, filename)
#         if os.path.isfile(file_path):
#             os.unlink(file_path)
#         elif os.path.isdir(file_path):
#             shutil.rmtree(file_path)
#         else:
#             print("Error emptying recycling.")


if __name__ == "__main__":
    clear_file()
    # clear_trash()
