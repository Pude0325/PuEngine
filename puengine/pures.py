import re as _re
class PuRes:
    keyRule = r"^@[a-zA-Z_0-9\.]*:"
    typeRule = r"<[a-zA-Z0-9_]*>"
    valueRule = r"\".*\""
    noteRule = r"^\$.*;$"

    @staticmethod
    def PuResTypeError(line, path, type):
        print("PuResError: " + line + " in " + path + " is not " + type + " class.")

    @staticmethod
    def __string(value : str):
        return value.replace("\\n", "\n")

    @staticmethod
    def __number(value):
        try:
            num = float(value)
            return num
        except ValueError as e:
            num = None
            return num


    @staticmethod
    def __boolen(value: str):
        if (value.lower() == 'true'):
            return True

        elif (value.lower() == 'false'):
            return False

        else:
            return None

    @staticmethod
    def __tuple(arg:str):
        ru = []
        t_ru = []
        for i in range(len(arg)):
            if _re.search(r'[0-9]',arg[i]):
                t_ru.append(arg[i])
            elif arg[i] == ',':
                ind = 1
                num = len(t_ru) - 1
                tt_ru = 0
                while(num >= 0):
                    tt_ru += int(t_ru[num]) * ind
                    ind = ind*10
                    num -= 1
                ru.append(tt_ru)
                t_ru.clear()
            elif arg[i] == ')':
                ind = 1
                num = len(t_ru) - 1
                tt_ru = 0
                while(num >= 0):
                    tt_ru += int(t_ru[num]) * ind
                    ind = ind*10
                    num -= 1
                ru.append(tt_ru)
                t_ru.clear()
                return tuple(ru)
            elif arg[i] == '(' or  arg[i] == ' ':
                pass
            else:
                assert False, Exception("Error")
        assert False, Exception("Error")


    typeToFunc = {
        "string": __string,
        "number": __number,
        "boolen": __boolen,
        "tuple": __tuple
    }

    @staticmethod
    def Load(filepath: str, loadnote: bool, savetype = True):
        file = open(filepath, "r+", encoding='utf-8')
        sl = file.readlines()
        ru = {"__note": []}
        def ErrorToNote(line:str):
            if (not loadnote): return
            ru["__note"].append(line.replace('\n', ''))
        i = 1
        for s in sl:
            if (s[0] == '@'):
                text = _re.search(PuRes.keyRule, s)
                if (text == None):
                    print("PuResError: Type is null in line " + str(i))
                    ErrorToNote(s)
                    i += 1
                    continue

                key = text.group().replace('@', '').replace(':', '')

                text = _re.search(PuRes.typeRule, s)
                if (text == None):
                    print("PuResError: Type is null in line " + i)
                    ErrorToNote(s)
                    i += 1
                    continue
                type = text.group().replace('<', '').replace('>', '')

                text = _re.search(PuRes.valueRule, s)
                if (text == None):
                    print("PuResError: Value is null in line" + i)
                    ErrorToNote(s)
                    i += 1
                    continue
                value = text.group().replace('"', '').replace('"', '')

                if (type == 's' or type == 'string'):
                    ru[key] = PuRes.typeToFunc['string'](value)
                    if (savetype): ru["__" + key] = type
                elif (type == 'b' or type == 'bollen'):
                  ruv = PuRes.typeToFunc['boolen'](value)
                  if (ruv != None):
                    ru[key] = ruv
                    if (savetype): ru["__" + key] = type

                  else:
                    print("PuResError: Type is not boolen in line " + str(i))
                    ErrorToNote(s)
                    i += 1
                    continue
                elif (type == 'n' or type == 'number'):
                    ruv = PuRes.typeToFunc['number'](value)
                    if (ruv != None):
                        ru[key] = ruv
                        if (savetype): ru["__" + key] = type
                    else:
                        print("PuResError: Type is not number in line " + str(i))
                        ErrorToNote(s)
                        i += 1
                        continue
                else:
                    try:
                        ruv = PuRes.typeToFunc[type](value)
                        ru[key] = ruv
                        if (savetype): ru["__" + key] = type
                    except:
                        print("PuResError: Type is not " + type + " in line " + str(i))
                        ErrorToNote(s)
                        i += 1
                        continue
            elif (s[0] == '$' and loadnote):
                note = _re.search(PuRes.noteRule, s)
                if (note == None):
                    print("PuResError: Note format error line " + i)
                    ErrorToNote(s)
                    i += 1
                    continue
                ru["__note"].append(note.group().replace('$', '').replace(';', ''))
            i += 1
        # print(ru)
        return ru
    @staticmethod
    def Save(dic, filepath, saveNote):
        data = ""
        for key in dic:
            if (key[0] == '_'): continue
            data += f"@{key}: <{dic['__'+key]}> \"{dic[key]}\";\n"
        if (saveNote):
            for i in range(len(dic["__note"])):
                data += f"${dic['__note'][i]};\n"
        with (open(filepath, 'w+', encoding='utf-8') as f):
            f.write(data)
        return data
