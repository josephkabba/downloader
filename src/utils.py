def create_save_format(id: str, duration: str, title: str, new_data = True) -> str:
    if new_data:
        return id + "###" + duration + "###" + "pending" + "###" + title
    else:
        return id + "###" + duration + "###" + "downloaded" + "###" + title


def format_name(name: str) -> str: 
    name = name.replace("/", "")
    name = name.replace("\\", "")
    name = name.replace("?", "")
    name = name.replace("*", "")
    name = name.replace("\"", "")
    name = name.replace("<", "")
    name = name.replace(">", "")
    name = name.replace(":", "")
    name = name.replace("|", "")
    name = name.replace(".", "")
    name = name.replace(" ", "_")
    return name