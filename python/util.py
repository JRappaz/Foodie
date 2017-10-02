def removeSpace(text):
    text = ''.join(text.split("\n"))
    split = text.split(" ")
    text = ""
    for part in split:
        if part != "":
            text += part + " "
    text = text[:-1]
    return text