from typing import TypedDict


class ParsingError(Exception):
    """Error of parsing"""
    pass


class ParsingResult(TypedDict, total=False):
    """
    The return of the parsing function.

    Keys:
        width (int): The width of the maze.
        height (int): The height of the maze.
        entry (tuple[int, int]): Entry cell coordinate (x, y) .
        exit (tuple[int, int]): Exit cell coordinate (x, y).
        output_file (str): File where to store the maze structure.
        perfect (bool): whethere th maze is perfect or not (loop or not).
        seed (int): Optional argument to generate a maze based on a seed.
    """
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int


def parsing(filename: str) -> ParsingResult:
    """
    Parse the input file.

    Raises:
        ParsingError: If input file format is invalid.

    Args:
        filename (str): Path to the input file.

    Returns:
        dic (ParsingResult): The dictionary with all maze information.
    """
    dic: ParsingResult = {}

    # store the mandatory input
    mandatory = ["WIDTH",
                 "HEIGHT",
                 "ENTRY",
                 "EXIT",
                 "OUTPUT_FILE",
                 "PERFECT"]

    with open(filename, "r") as c:
        all_file = c.read()
        # Check the presence of all mandatory
        for option in mandatory:
            if option not in all_file:
                raise ParsingError(f"Mandatory option {option} was not found!")

        c.seek(0)
        for line in c:

            # Chech if a mandatory is commented or not
            for i in mandatory:
                if line.startswith("#" + i):
                    raise ParsingError("Cannot comment a "
                                       f"mandatory variable: {i}")

            if '#' in line:
                continue

            elif '=' not in line:
                raise ParsingError("Wrong format, expected: key=value "
                                   f"in line '{line.strip()}'")

            # Width and Heigh parsing
            for i in ["WIDTH", "HEIGHT"]:
                if i in line:
                    key, value = line.split("=", 1)
                    try:
                        int_value: int = int(value.strip())
                    except ValueError:
                        raise ParsingError(f"'{key}' accept only numbers "
                                           f"not: '{value.strip()}'")
                    if i == "WIDTH":
                        dic["width"] = int_value
                    else:
                        dic["height"] = int_value
                    continue

            # Entry and Exit parsing
            for i in ["ENTRY", "EXIT"]:
                if i in line:
                    if ',' in line:
                        key, tup = line.split("=", 1)
                        v_1, v_2 = tup.split(",", 1)
                        try:
                            value_1: int = int(v_1.strip())
                            value_2: int = int(v_2.strip())
                        except ValueError:
                            raise ParsingError(f"'{key}' accept only numbers "
                                               f"not: '{tup.strip()}'")
                        if i == "ENTRY":
                            dic["entry"] = (value_1, value_2)
                        else:
                            dic["exit"] = (value_1, value_2)
                        continue
                    else:
                        raise ParsingError(f"Wrong format for {i}, "
                                           "expected: key=(value_1, value_2)")

            # Output file parsing
            if "OUTPUT_FILE" in line:
                k, v = line.split("=", 1)
                name: str = v.strip()

                if not name.endswith(".txt"):
                    raise ParsingError(f"filename must be a valid .txt, "
                                       f"got '{name.strip()}'")
                dic["output_file"] = name
                continue

            # Perfect parsing
            elif "PERFECT" in line:
                k, v = line.split("=", 1)
                perfect = v.strip()
                if perfect == "True":
                    dic["perfect"] = True
                elif perfect == "False":
                    dic["perfect"] = False
                else:
                    raise ParsingError("Only True or False are "
                                       "allowed for PERFECT")
                continue

            # Seed parsing
            elif "SEED" in line:
                key, value = line.split("=", 1)
                if not value.strip():
                    continue
                try:
                    seed = int(value.strip())
                    if seed <= 10 or not (0 <= seed % 10 <= 2):
                        raise ValueError
                except ValueError:
                    raise ParsingError("The seed need to be a valid integer "
                                       "greater than 10, whose last digit is "
                                       "0, 1 or 2")
                dic["seed"] = seed
                continue

    # verify if the entry and exit are in the range of the width and heigh
    if not (0 <= dic['entry'][0] < dic['width']
            and 0 <= dic['entry'][1] < dic['height']):
        raise ParsingError("The entry need to be "
                           "in the range of the maze - 1\n"
                           "Entry out of range")
    if not (0 <= dic['exit'][0] < dic['width']
            and 0 <= dic['exit'][1] < dic['height']):
        raise ParsingError("The exit need to be "
                           "in the range of the maze - 1\n"
                           "Exit out of range")

    # Verify that the width and height let us display the 42 pattern
    if dic['width'] < 9 or dic['height'] < 7:
        print("[INFO]: The given maze size is too small "
              "to display the 42 pattern")
    return dic
