"""
提供绝对路径
"""
import os


def get_project_path():
    current_file =  os.path.abspath(__file__)
    project_path = os.path.dirname(os.path.dirname(current_file))
    return project_path

def get_abs_path(relative_path: str) -> str:
    project_path = get_project_path()
    return os.path.join(project_path, relative_path)

if __name__ == '__main__':
    print(get_abs_path(__file__))