tag_beer_category = [
    "beer",
    "cider",
    "mini_keg",
    "wine",
    "fortified_wine",
    "sparkling_wine",
    "bib",
    "box",
    "food",
    "misc",
]
tag_spirit_category = ["spirit", "arranged"]


def format_tag_list(tag_list):
    tag_beer_list = []
    tag_spirit_list = []
    for article, nb_tag in tag_list:
        # article['nb_tag'] = nb_tag
        if article["ratio_category"] in tag_beer_category:
            tag_beer_list.append((article, nb_tag))
        elif article["ratio_category"] in tag_spirit_category:
            tag_spirit_list.append((article, nb_tag))

    return tag_beer_list, tag_spirit_list
