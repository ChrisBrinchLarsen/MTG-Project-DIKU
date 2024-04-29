import re
import datetime as dt

with open("data/cardData.json", 'r', encoding='cp437') as file:
    lines = file.read().split('\n')
    cards = []
    for line in lines:
        # Flavor Text
        flavorText_        = "" # Default value if no flavor text exists on the card
        flavorMatch        = re.search(r'"flavor_text":"(.*?)",', line)
        if flavorMatch    != None:
            flavorText_    = flavorMatch.group(1)

        # Price
        priceEUR_          = 0.0 # Default value if the price is unavailable
        priceEurMatch      = re.search(r'"eur":"(.*?)",', line)
        if priceEurMatch  != None:
            priceEUR_      = float(priceEurMatch.group(1))
            
        # Release Date
        dateMatch          = re.search(r'"released_at":"(\d+)-(\d+)-(\d+)",', line)
        (year, month, day) = (int(dateMatch.group(1)), int(dateMatch.group(2)), int(dateMatch.group(3)))
        releaseDate_       = dt.datetime(year, month, day)

        # Misc info
        collectorID_       = re.search(r'"collector_number":"(.*?)",', line).group(1) # We can't int() convert this due to "★"
        oracleText_        = re.search(r'"oracle_text":"(.*?)",'     , line).group(1)
        manaCost_          = re.search(r'"mana_cost":"(.*?)",'       , line).group(1)
        imageUrl_          = re.search(r'"large":"(.*?)",'           , line).group(1)
        setCode_           = re.search(r'"set":"(.*?)",'             , line).group(1)
        setName_           = re.search(r'"set_name":"(.*?)",'        , line).group(1)
        setType_           = re.search(r'"set_type":"(.*?)",'        , line).group(1)
        rarity_            = re.search(r'"rarity":"(.*?)",'          , line).group(1)
        layout_            = re.search(r'"layout":"(.*?)",'          , line).group(1)
        artist_            = re.search(r'"artist":"(.*?)",'          , line).group(1)
        name_              = re.search(r'"name":"(.*?)",'            , line).group(1)

        # Types
        superType_         = ""
        subType_           = ""

        cardAttr = dict(
            name        = name_,
            releaseDate = releaseDate_,
            rarity      = rarity_,
            manaCost    = manaCost_,
            layout      = layout_,
            imageUrl    = imageUrl_,
            oracleText  = oracleText_,
            setCode     = setCode_,
            setName     = setName_,
            setType     = setType_,
            collectorID = collectorID_,
            flavorText  = flavorText_,
            artist      = artist_,
            priceEUR    = priceEUR_
        )
        cards.append(cardAttr)
    print(cards[0])
