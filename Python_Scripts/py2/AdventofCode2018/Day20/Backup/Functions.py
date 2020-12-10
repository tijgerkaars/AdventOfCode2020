def parse(regex, symbol):
    new_string = ""
    rest_string = ""
    for i,each in enumerate(regex):
        if each == symbol:
            new_string = regex[:i]
            if symbol == "(":
                rest_string = regex[(i+1):len(regex)-2] + "$"
            elif symbol == "|":
                rest_string = regex[(i+1):]
            break
    return new_string, rest_string
