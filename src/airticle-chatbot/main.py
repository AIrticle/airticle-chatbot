from my_dir import my_file
import my_file_2

def get_10():
    return my_file.get_5() * 2

def get_14():
    return my_file_2.get_7() * 2

if __name__ == "__main__":
    print("Hello world")
    print("get_10():", get_10())
    print("get_14():", get_14())