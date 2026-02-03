class ParsingError(Exception):
    pass


def parsing(filename: str) -> dict:
    dic = {}

    mandatory = ["WIDTH",
                 "HEIGHT",
                 "ENTRY",
                 "EXIT",
                 "OUTPUT_FILE",
                 "PERFECT"]

    with open(filename, "r") as c:
        all_file = c.read()
        for key in mandatory:
            if key not in all_file:
                raise ParsingError(f"Mandatory option {key} was not found!")

        c.seek(0)
        for line in c:
            tup = None

            for i in mandatory:
                if line.startswith("#" + i):
                    raise ParsingError(f"Cannot comment a mandatory variable: {i}")
        
            if '#' in line:
                continue
            
            elif '=' not in line:
                raise ParsingError(f"Wrong format, expected: key=value in line '{line.strip()}'")
        

            for i in ["WIDTH", "HEIGHT"]:
                if i in line:
                    key, value = line.split("=", 1)
                    try:
                        value = int(value.strip())
                    except ValueError:
                        raise ParsingError(f"'{key}' accept only numbers not: '{value.strip()}'")

            for i in ["ENTRY", "EXIT"]:
                if i in line:
                    if ',' in line:
                        key , tup = line.split("=", 1)
                        value_1, value_2 = tup.split(",", 1)
                        try:
                            value_1 = int(value_1.strip())
                            value_2 = int(value_2.strip())
                        except ValueError:
                            raise ParsingError(f"'{key}' accept only numbers not: '{tup.strip()}'")
                    else:
                        raise ParsingError(f"Wrong format for {i}, expected: key=(value_1, value_2)")

            if "OUTPUT_FILE" in line:
                key, value = line.split("=", 1)
                value = value.strip()

                if not value.endswith(".txt"):
                    raise ParsingError(f"filename must be a valid .txt, got '{value.strip()}'")
            
            elif "PERFECT" in line:
                key, value = line.split("=", 1)
                value = value.strip()
                if value == "True":
                    value = True
                elif value == "False":
                    value = False
                else:
                    raise ParsingError("Only True or False are allowed for PERFECT")
            
            elif "SEED" in line:
                key, value = line.split("=", 1)
                value = value.strip()
                if not value:
                    continue

            if not tup:
                dic.update({key.lower(): value})
            else:
                dic.update({key.lower(): (value_1, value_2)})

    if not (0 <= dic['entry'][0] < dic['width'] and 0 <= dic['entry'][1] < dic['height']):
        raise ParsingError("The entry need to be in the range of the maze - 1\n"
                           "Entry out of range")
    if not (0 <= dic['exit'][0] < dic['width'] and 0 <= dic['exit'][1] < dic['height']):
        raise ParsingError("The exit need to be in the range of the maze - 1\n"
                           "Exit out of range")
    return dic
