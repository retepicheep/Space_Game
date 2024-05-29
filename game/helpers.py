import json
import os


def handle_json(json_file, method, keywords=None, update_data=None):
    """This function handles reading from and writing to JSON files.

    Arguments:
    json_file -- the path to the JSON file
    method -- the file operation mode ('read' for read, 'update' for write)
    keywords -- the keys to extract data for (used in read mode to extract specific data or read entire file,
               and in write mode to update specific data)
    update_data -- the data to write (used only in write mode)
    """

    if method == "read":
        try:
            with open(json_file, "r") as f:
                data = json.load(f)
                if keywords:
                    result = data
                    for key in keywords:
                        result = result.get(key, {})
                    return result
                return data
        except FileNotFoundError:
            print(
                f"The file '{json_file}' was not found. Please make sure it is in the correct directory."
            )
        except json.JSONDecodeError:
            print(f"The file '{json_file}' is not a valid JSON file.")
        except KeyError:
            print(f"The key '{keywords}' was not found in the JSON file.")

    elif method == "update":
        try:
            with open(json_file, "r+") as f:
                data = json.load(f)
                if keywords and update_data is not None:
                    d = data
                    for key in keywords[:-1]:
                        d = d.setdefault(key, {})
                    d[keywords[-1]] = update_data
                    f.seek(0)
                    f.truncate()
                    json.dump(data, f, indent=4)
                else:
                    print("No keywords or update_data provided for writing operation.")
        except FileNotFoundError:
            print(
                f"The file '{json_file}' was not found. Please make sure it is in the correct directory."
            )
        except json.JSONDecodeError:
            print(f"The file '{json_file}' is not a valid JSON file.")

    return None
