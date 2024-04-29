import re
import datetime as dt

with open("data/cardData.json", 'r', encoding='cp437') as file:
    lines = file.read().split('\n')
    layoutTypes = set()
    cards = []
    for line in lines:
        name_ = re.search(r'"name":"(.*?)"', line).group(1)
        dateMatch = re.search(r'"released_at":"(\d+)-(\d+)-(\d+)"', line)
        (year, month, day) = (int(dateMatch.group(1)), int(dateMatch.group(2)), int(dateMatch.group(3)))
        releaseDate_ = dt.datetime(year, month, day)
        rarity_ = re.search(r'"rarity":"(.*?)"', line).group(1)
        manaCost_ = re.search(r'"mana_cost":"(.*?)"', line).group(1)
        layout_ = re.search(r'"layout":"(.*?)"', line).group(1)
        superType_ = ""
        subType_ = ""
        oracleText_ = ""
        flavorText_ = ""
        setName_ = ""
        setType_ = ""
        collectorID_ = ""
        artist_ = ""
        priceEUR_ = ""
        imageUrl_ = ""

        layoutType = re.search(r'"layout":"(\w+)"', line).group(1)
        layoutTypes.add(layoutType)
        cardAttr = dict(
            name = name_,
            releaseDate = releaseDate_,
            rarity = rarity_,
            manaCost = manaCost_,
            layout = layout_
        )
        cards.append(cardAttr)
    print(layoutTypes)
    print(cards[3847])
