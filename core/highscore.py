import os

user_home = os.path.expanduser("~")

high_score_file_path = os.path.join(user_home, "Documents", "high_score.txt")

def update_high_score(new_high_score):
    if not os.path.exists(high_score_file_path):
        with open(high_score_file_path, "w") as file:
            file.write(str(new_high_score))
    else:
        with open(high_score_file_path, "r") as file:
            current_high_score = int(file.read())
        
        if new_high_score > current_high_score:
            with open(high_score_file_path, "w") as file:
                file.write(str(new_high_score))

def get_high_score():
    if not os.path.exists(high_score_file_path):
        return 0
    else:
        with open(high_score_file_path, "r") as file:
            return int(file.read())
        
def reset_high_score():
    with open(high_score_file_path, "w") as file:
        file.write(str(0))