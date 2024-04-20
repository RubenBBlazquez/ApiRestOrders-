import json


def safe_loads(json_string: str):
    """
    Load a JSON string safely

    Parameters
    ----------
    json_string: str
        JSON string to be parsed

    Returns
    -------
    dict
        Parsed JSON string

    Raises
    ------
    json.JSONDecodeError
        If the JSON string is not valid even after replacing single quotes with double quotes
    """
    try:
        return json.loads(json_string)
    except json.JSONDecodeError:
        corrected_json_string = json_string.replace("'", '"')
        return json.loads(corrected_json_string)
