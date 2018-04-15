def parse(message):
    split = message.clean_content.split(' ')
    return split.pop(0), split
