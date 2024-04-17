import sys
from os import listdir
import shlex


class Flag:
    def __init__(self, f_name: str, f_type: type, f_comment: str):
        self.f_name = f_name
        self.f_type = f_type
        self.f_comment = f_comment

class FlagData:
    def __init__(self, name:str, flag: Flag, data):
        self.name = name
        self.flag = (flag, data)
    

class WP:

    # MEMBER VARIABLES /////////////////////////////////////////////////////////

    flags: Flag = []
    shortcuts = [] # Contains tuple with sc[0] = sc_name, sc[1] = list of ShortcutFlag

    # WCONFIG PARSERS //////////////////////////////////////////////////////////

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
    

    def parse_data(self, data_list: list):
        flag_list: FlagData = []
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
  
        return flag_list
    
    # RUN PREPPING /////////////////////////////////////////////////////////////

    def merge_shortcut_with_default(self, s_name: str) -> list:
        for sc in self.shortcuts:
            if s_name == sc[0]:
                return self.merge_with_default(sc[1])

    def merge_with_default(self, user_list: list) -> list:
        for d_flag in self.default:
            if d_flag.name not in [u.name for u in user_list]:
                user_list.append(d_flag)
        
        return user_list

    def order(self, user_list: list) -> list:
        for i in range(len(self.flags)): # len(flags) should equal len(user_list)
            for j in range(i, len(user_list)):
                if user_list[j].name == self.flags[i].f_name:
                    if i != j:
                        user_list[i], user_list[j] = user_list[j], user_list[i]
                    break
        
        return user_list
    
    def convert_to_call(self, flag_list: list) -> str:
        call = self.executable[:-1] + " "
        for flag in flag_list:
            call += str(flag.flag[1]) + " "
        
        return call
                     

    # CONSTRUCTOR //////////////////////////////////////////////////////////////

    def __init__(self, config_file):
        self.default_defined = False
        for line in config_file.readlines():
            data_list = shlex.split(line)
            if line.startswith("./"):
                self.executable = line
            elif line.startswith('-'):
                self.parse_flag(line)
            elif line.startswith('='):
                self.shortcuts.append((data_list[0], self.parse_data(data_list)))
            elif line.startswith('>'):
                if self.default_defined:
                    raise Exception("Default flags were already defined.")
                self.default = self.parse_data(data_list)
                self.default_defined = True
                if len(self.default) != len(self.flags):
                    raise Exception("Default does not contain correct amount of flags.")

            elif line in ["", "\n"]:
                pass
            else:
                raise Exception("Unexpected token encountered: " + line.split()[0])
    
    # OTHER FUNCTIONS //////////////////////////////////////////////////////////

    def print(self):
        sys.stderr.write("Executable: " + self.executable + "\n")

        sys.stderr.write("Supported flags:\n")
        for flag in self.flags:
            sys.stderr.write(flag.f_name + " <" + flag.f_type.__name__ + "> => " + flag.f_comment + "\n")

        sys.stderr.write("\nSupported shortcuts:\n")
        for sc in self.shortcuts:
            sys.stderr.write(sc[0] + " ")
            for flag in sc[1]:
                sys.stderr.write(flag.name + " " + str(flag.flag[1]) + " ")
          
        sys.stderr.write("\n\nDefault call:\n")
        # TODO: executable contains newline or something
        sys.stderr.write(self.executable[:-1] + " ")
        for flag in self.default:
            sys.stderr.write(flag.name + " " + str(flag.flag[1]) + " ")
        sys.stderr.write("\n")

def main() -> str:
    if "wconfig" not in listdir():
        raise Exception("wconfig not found.")
    
    wp = WP(open("wconfig", 'r'))

    if len(sys.argv) == 1:
        if not wp.default_defined:
            raise Exception("No default flags were defined in wconfig")
        user_flags = wp.default
    elif len(sys.argv) > 1 and sys.argv[1] == '?':
        wp.print()
        return ""
    elif len(sys.argv) == 2:
        if sys.argv[1].startswith('='):
            user_flags = wp.merge_shortcut_with_default(sys.argv[1])
    else:        
        user_flags = wp.parse_data(sys.argv)
        user_flags = wp.merge_with_default(user_flags)
            

    user_flags = wp.order(user_flags)
    print(wp.convert_to_call(user_flags))
    

if __name__ == "__main__":
    main()