import sys
from os import listdir
import shlex


class Flag:
    def __init__(self, f_name: str, f_type: type, f_comment: str):
        self.f_name = f_name
        self.f_type = f_type
        self.f_comment = f_comment
    

class WP:

    flags = []


    def parse_flag(self, flag_string):
        flag_list = shlex.split(flag_string)
        if len(flag_list) != 3:
            raise Exception("Flag in unsupported format.")
        
        f_name = flag_list[0][1:]
        if (flag_list[1] in ["int", "integer"]):
            f_type = int
        elif (flag_list[1] in ["str", "string"]):
            f_type = str
        elif (flag_list[1] in ["float", "double"]):
            f_type = float
        else:
            raise Exception("Unsupported type encountered while parsing flag.")
        
        self.flags.append(Flag(f_name, f_type, flag_list[2]))


    def __init__(self, config_file):
        for line in config_file.readlines():
            if line.startswith("./"):
                self.executable = line
            elif line.startswith('-'):
                self.parse_flag(line)
            elif line.startswith('='):
                self.parse_shortcut()
            elif line in ["", "\n"]:
                pass
            else:
                raise Exception("Unexpected token encountered.")
            






def main():
    if "wconfig" not in listdir():
        raise Exception("wconfig not found, program terminated.")
    
    wp = WP(open("wconfig", 'r'))

    for flag in wp.flags:
        print("-" + flag.f_name + " <" + flag.f_type.__name__ + "> " + flag.f_comment)
    

if __name__ == "__main__":
    main()