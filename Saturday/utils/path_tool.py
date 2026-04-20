"""
为整个工程提供统一的绝对路径
"""
import os

"""
获取工程所在的根目录
return：字符串根目录
"""
def get_project_root():

#获取当前文件的绝对路径
    current_file = os.path.abspath(__file__)
#获取工程的根目录，先获取当前文件的文件夹的绝对路径
    current_dir = os.path.dirname(current_file)
#获取工程的根目录
    project_root= os.path.dirname(current_dir)

    return project_root
"""
传递相对路径，得到绝对路径
"""
def get_abs_path(relative_path:str):

    project_root = get_project_root()
    return os.path.join(project_root,relative_path)
