import sys
from os import listdir
import shlex


class Flag:
    def __init__(self, f_name: str, f_type: type, f_comment: str):
        self.f_name = f_name
        self.f_type = f_type
        self.f_comment = f_comment

class ShortcutFlag:
    def __init__(self, s_name:str, flag: Flag, data):
        self.s_name = s_name
        self.flag = (flag, data)
    

class WP:

    flags: Flag = []
    shortcuts = []


    def parse_flag(self, flag_string):
        flag_list = shlex.split(flag_string)
        if len(flag_list) != 3:
            raise Exception("Flag in unsupported format.")
        
        f_name = flag_list[0]
        if (flag_list[1] in ["int", "integer"]):
            f_type = int
        elif (flag_list[1] in ["str", "string"]):
            f_type = str
        elif (flag_list[1] in ["float", "double"]):
            f_type = float
        else:
            raise Exception("Unsupported type encountered while parsing flag.")
        
        self.flags.append(Flag(f_name, f_type, flag_list[2]))

    def parse_shortcut(self, shortcut_string):
        shortcut_list = shlex.split(shortcut_string)
        flag_list: ShortcutFlag = []
        s_name = shortcut_list[0]
        for i in range(1, len(shortcut_list), 2):
            for j in range(len(self.flags)):
                if shortcut_list[i] == self.flags[j].f_name:
                    if self.flags[j].f_type ==  int:
                        data = int(shortcut_list[i + 1])
                    elif self.flags[j].f_type == float:
                        data = float(shortcut_list[i + 1])
                    else:
                        data = shortcut_list[i + 1]
                    
                    flag_list.append(ShortcutFlag(self.flags[j].f_name, self.flags[j], data))
        
        self.shortcuts.append((shortcut_list[0], flag_list))


    def __init__(self, config_file):
        for line in config_file.readlines():
            if line.startswith("./"):
                self.executable = line
            elif line.startswith('-'):
                self.parse_flag(line)
            elif line.startswith('='):
                self.parse_shortcut(line)
            elif line in ["", "\n"]:
                pass
            else:
                raise Exception("Unexpected token encountered.")
            

def main():
    if "wconfig" not in listdir():
        raise Exception("wconfig not found, program terminated.")
    
    wp = WP(open("wconfig", 'r'))

    for flag in wp.flags:
        print(flag.f_name + " <" + flag.f_type.__name__ + "> ->" + flag.f_comment)

    for sc in wp.shortcuts:
        print(sc[0], end=" ")
        for flag in sc[1]:
            print(flag.s_name + " " + str(flag.flag[1]), end=" ")
        print("\n")
    

if __name__ == "__main__":
    main()