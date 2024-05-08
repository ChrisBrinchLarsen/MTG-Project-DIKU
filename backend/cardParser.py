import re
import datetime as dt

def matchTrait(trait: str, source: str):
    return re.search(r'"'+ trait + r'":"(.*?)",', source)

def getTrait(trait: str, source: str) -> str:
    traitMatch = matchTrait(trait, source)
    if traitMatch != None:
        return traitMatch.group(1)
    else:
        return ""

# Strips away 4119 broken entries
def checkMissingData(card:dict) -> bool:
    importantTraits = ["name"
                      ,"releaseDate"
                      ,"collectorID"
                      ,"imageSmall"
                      ,"imageNormal"
                      ,"imageLarge"
                      ,"setAcro"
                      ,"combinedMana"
                      ,"oracleText"
                      ,"setName"
                      ,"setType"
                      ,"rarity"
                      ,"layout"
                      ,"artist"
                      ]
    for trait in importantTraits:
        if card[trait] == "":
            return True
    badLayouts = {"split", "transform", "modal_dfc", "double_faced_token", "art_series", "adventure"}
    if card["layout"] in badLayouts: return True
    return False

def parseCards(file:str):
    cards = []
    with open("data/"+file, 'r', encoding='cp437') as file:
        lines = file.read().split('\n')
        for line in lines:
            if line == '[' or line == ']': continue # Skip first and last line

            # Misc Traits
            collectorID_ = getTrait("collector_number",line) # We can't make these ints due to "★" and various exceptions
            flavorText_  = getTrait("flavor_text"     ,line).replace("\\", "") # Cleaning up strings
            oracleText_  = getTrait("oracle_text"     ,line)        
            #exactMana_   = getTrait("mana_cost"       ,line)
            priceEUR_    = getTrait("eur"             ,line)
            if priceEUR_ == "":
                priceEUR_ = 0.0
            imageSmall_  = getTrait("small"           ,line)
            imageNormal_ = getTrait("normal"          ,line)
            imageLarge_  = getTrait("large"           ,line)
            setAcro_     = getTrait("set"             ,line)
            setName_     = getTrait("set_name"        ,line)
            setType_     = getTrait("set_type"        ,line)
            rarity_      = getTrait("rarity"          ,line)
            layout_      = getTrait("layout"          ,line)
            artist_      = getTrait("artist"          ,line)
            name_        = getTrait("name"            ,line)
            layout_      = getTrait("layout"          ,line)
            
            # Types
            typeLine     = getTrait("type_line"       ,line).encode().decode("unicode-escape").replace(u"Î\x93Ã\x87Ã¶", "-").split(" - ")
            subTypes_ = []
            if len(typeLine) != 1:
                subTypes_ = typeLine[1].split(" ")
            leftTypes = typeLine[0].split(" ")
            validTypes = {"Creature"
                        ,"Sorcery"
                        ,"Summon"
                        ,"Interrupt"
                        ,"Instant"
                        ,"Artifact"
                        ,"Battle"
                        ,"Conspiracy"
                        ,"Emblem"
                        ,"Enchantment"
                        ,"Hero"
                        ,"Land"
                        ,"Phenomenon"
                        ,"Plane"
                        ,"Planeswalker"
                        ,"Scheme"
                        ,"Tribal"
                        ,"Vanguard"
                        }
            types_ = []
            superTypes_ = []
            for type in leftTypes:
                if type in validTypes:
                    types_.append(type)
                else:
                    superTypes_.append(type)

            # Keywords
            keywords_ = []
            keywordsMatch = re.search(r'"keywords":(\[.*?\]),', line)
            if keywordsMatch != None:
                keywords_ = eval(keywordsMatch.group(1))

            # Color identities
            colors_ = []
            colorsMatch = re.search(r'"colors":(\[.*?\]),', line)
            if colorsMatch != None:
                colors_ = eval(colorsMatch.group(1))

                

            # Combined Mana
            combinedMana_         = 0
            combinedManaMatch     = re.search(r'"cmc":(\d+\.\d?),', line)
            if combinedManaMatch != None:
                combinedMana_     = float(combinedManaMatch.group(1))

            # Release Date
            releaseDate_           = dt.datetime.min # Default value ?
            dateMatch              = re.search(r'"released_at":"(\d+)-(\d+)-(\d+)",', line)
            if dateMatch != None:
                (year, month, day) = (int(dateMatch.group(1)), int(dateMatch.group(2)), int(dateMatch.group(3)))
                releaseDate_       = dt.datetime(year, month, day)
            
            cardAttr = dict(
                name         = name_,
                releaseDate  = releaseDate_,
                superTypes   = superTypes_,
                types        = types_,
                subTypes     = subTypes_,
                keywords    = keywords_,
            #    exactMana    = exactMana_,
                combinedMana = combinedMana_,
                oracleText   = oracleText_,
                collectorID  = collectorID_,
                flavorText   = flavorText_,
                priceEUR     = priceEUR_,
                imageSmall   = imageSmall_,
                imageNormal  = imageNormal_,
                imageLarge   = imageLarge_,
                setAcro      = setAcro_,
                setName      = setName_,
                setType      = setType_,
                rarity       = rarity_,
                layout       = layout_,
                artist       = artist_,
                colors       = colors_,
            )
            isBadCard = checkMissingData(cardAttr)
            if isBadCard: continue  # This could be optimized so we early exit as soon as we receive a bad trait

            cards.append(cardAttr)

    # Sorting by date and then name to prepare for duplicate removal
    sortedByDate = sorted(cards, key=lambda x: x["releaseDate"])
    sortedByNameDate = sorted(cards, key=lambda x: x["name"])

    # Removing 61571 duplicates, keeping only the original prints
    noDupesCards = []
    for x in range(len(sortedByNameDate)):
        currentName = sortedByNameDate[x]["name"]
        if (x != len(sortedByNameDate)-1):
            nextName = sortedByNameDate[x+1]["name"]
            if currentName == nextName: continue
            else: noDupesCards.append(sortedByNameDate[x])
        else: noDupesCards.append(sortedByNameDate[x])
    return noDupesCards