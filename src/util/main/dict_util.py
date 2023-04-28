def combine_dict(dict1: dict, dict2: dict) -> dict:
    """
    Combining two dictionnaries into one

    :param dict1: First dictionary
    :param dict2: Second dictionary
    :return: Combination of both dictionary
    """
    if dict2 == {}:
        return dict1
    else:
        for maps in dict2.items():
            for element in maps[1]:
                try:
                    dict1[maps[0]].append(element)
                except:
                    dict1[maps[0]] = [element]

        return dict1
