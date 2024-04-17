import sys
from os import listdir
import shlex


class Flag:
    def __init__(self, f_name: str, f_type: type, f_comment: str):
        self.f_name = f_name
        self.f_type = f_type
        self.f_comment = f_comment

class FlagData:
    def __init__(self, s_name:str, flag: Flag, data):
        self.s_name = s_name
        self.flag = (flag, data)
    

class WP:

    flags: Flag = []
    shortcuts = [] # Contains tuple with sc[0] = sc_name, sc[1] = list of ShortcutFlag


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
    

    def parse_data(self, line: str, parse_shortcut: bool):
        if self.default_defined and not parse_shortcut:
            raise Exception("Default flags were already defined.")
        
        data_list = shlex.split(line)
        flag_list: FlagData = []
        s_name = data_list[0]
        for i in range(1, len(data_list), 2):
            found = False
            for j in range(len(self.flags)):
                try:
                    if data_list[i] == self.flags[j].f_name:
                        if self.flags[j].f_type ==  int:
                            data = int(data_list[i + 1])
                        elif self.flags[j].f_type == float:
                            data = float(data_list[i + 1])
                        else:
                            data = str("\"" + data_list[i + 1] + "\"")
                        
                        flag_list.append(FlagData(self.flags[j].f_name, self.flags[j], data))
                        found = True
                except:
                    raise Exception("Data type invalid. Expected: " + self.flags[j].f_type.__name__ + ", got: " + data_list[i + 1])
            if not found:
                raise Exception("Flag not defined: " + data_list[i])

        if parse_shortcut:   
            self.shortcuts.append((data_list[0], flag_list))
        else:
            if len(flag_list) != len(self.flags):
                raise Exception("Default should have a value for each flag.")
            
            self.default = flag_list
            self.default_defined = True                     


    def __init__(self, config_file):
        self.default_defined = False
        for line in config_file.readlines():
            if line.startswith("./"):
                self.executable = line
            elif line.startswith('-'):
                self.parse_flag(line)
            elif line.startswith('='):
                self.parse_data(line, True)
            elif line.startswith('>'):
                self.parse_data(line, False)
            elif line in ["", "\n"]:
                pass
            else:
                raise Exception("Unexpected token encountered: " + line.split()[0])
    
    def print(self):
        print("Executable: " + self.executable)

        print("Supported flags:")
        for flag in self.flags:
            print(flag.f_name + " <" + flag.f_type.__name__ + "> => " + flag.f_comment)

        print("\nSupported shortcuts:")
        for sc in self.shortcuts:
            print(sc[0], end=" ")
            for flag in sc[1]:
                print(flag.s_name + " " + str(flag.flag[1]), end=" ")
          
        print("\n\nDefault call:")
        # TODO: executable contains newline or something
        print(self.executable[:-1], end=" ")
        for flag in self.default:
            print(flag.s_name + " " + str(flag.flag[1]), end=" ")
        print()

def main():
    if "wconfig" not in listdir():
        raise Exception("wconfig not found, program terminated.")
    
    wp = WP(open("wconfig", 'r'))

    if len(sys.argv) > 1 and sys.argv[1] == '?':
        wp.print()

    

if __name__ == "__main__":
    main()