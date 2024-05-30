import re
import datetime as dt

def match_trait(trait: str, source: str):
    return re.search(r'"'+ trait + r'":"(.*?)",', source)

def get_trait(trait: str, source: str) -> str:
    trait_match = match_trait(trait, source)
    if trait_match != None:
        return trait_match.group(1)
    else:
        return ""

# Strips away 4119 broken entries
def check_missing_data(card:dict) -> bool:
    important_traits = ["name"
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
    for trait in important_traits:
        if card[trait] == "":
            return True
    bad_layouts = {"split", "transform", "modal_dfc", "double_faced_token", "art_series", "adventure"}
    bad_set_types = {"alchemy", "funny", "token", "memorabilia", "minigame", "box", "vanguard"}
    bad_types = {"token", "emblem", "conspiracy"}
    if card["layout"] in bad_layouts: return True
    if card["setType"] in bad_set_types: return True
    for bad_type in bad_types:
        if bad_type in card["types"]: return True
    if "alchemy" in card["promoTypes"]: return True
    return False

def parse_cards(file:str):
    print("\nParsing cards. This might take a moment...")
    cards = []
    with open("data/"+file, 'r', encoding='cp437') as file:
        lines = file.read().split('\n')
        for line in lines:
            if line == '[' or line == ']': continue # Skip first and last line

            # Misc Traits
            collectorID_ = get_trait("collector_number",line) # We can't make these ints due to "★" and various exceptions
            flavorText_  = get_trait("flavor_text"     ,line).replace("\\", "") # Cleaning up strings
            oracleText_  = get_trait("oracle_text"     ,line)        
            #exactMana_   = get_trait("mana_cost"       ,line)
            priceEUR_    = get_trait("eur"             ,line)
            if priceEUR_ == "":
                priceEUR_ = 0.0
            imageSmall_  = get_trait("small"           ,line)
            imageNormal_ = get_trait("normal"          ,line)
            imageLarge_  = get_trait("large"           ,line)
            setAcro_     = get_trait("set"             ,line)
            setName_     = get_trait("set_name"        ,line)
            setType_     = get_trait("set_type"        ,line)
            rarity_      = get_trait("rarity"          ,line)
            layout_      = get_trait("layout"          ,line)
            artist_      = get_trait("artist"          ,line)
            name_        = get_trait("name"            ,line).replace("'", "''")
            layout_      = get_trait("layout"          ,line)
            
            # Types
            typeLine     = get_trait("type_line"       ,line).encode().decode("unicode-escape").replace(u"Î\x93Ã\x87Ã¶", "-").split(" - ")
            subTypes_ = []
            if len(typeLine) != 1:
                subTypes_ = typeLine[1].split(" ")
            left_types = typeLine[0].split(" ")
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
            for type in left_types:
                if type in validTypes:
                    types_.append(type)
                else:
                    superTypes_.append(type)

            # Keywords
            keywords_ = []
            keywords_match = re.search(r'"keywords":(\[.*?\]),', line)
            if keywords_match != None:
                keywords_ = eval(keywords_match.group(1))

            # Color identities
            colors_ = []
            colors_match = re.search(r'"colors":(\[.*?\]),', line)
            if colors_match != None:
                colors_ = eval(colors_match.group(1))  
            if len(colors_) == 0:
                colors_ = ["C"]

            # Combined Mana
            combinedMana_         = 0
            combined_mana_match     = re.search(r'"cmc":(\d+\.\d?),', line)
            if combined_mana_match != None:
                combinedMana_     = float(combined_mana_match.group(1))

            # Release Date
            releaseDate_           = dt.datetime.min # Default value ?
            dateMatch              = re.search(r'"released_at":"(\d+)-(\d+)-(\d+)",', line)
            if dateMatch != None:
                (year, month, day) = (int(dateMatch.group(1)), int(dateMatch.group(2)), int(dateMatch.group(3)))
                releaseDate_       = dt.datetime(year, month, day)
            
            # Promo types
            promotypes_ = []
            promotypes_match = colors_match = re.search(r'"promo_types":(\[.*?\]),', line)
            if promotypes_match != None:
                promotypes_ = eval(promotypes_match.group(1))

            card_attr = dict(
                name         = name_,
                releaseDate  = releaseDate_,
                superTypes   = superTypes_,
                types        = types_,
                subTypes     = subTypes_,
                keywords    = keywords_,
            #   exactMana    = exactMana_,
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
                promoTypes   = promotypes_
            )
            is_nad_card = check_missing_data(card_attr)
            if is_nad_card: continue  # This could be optimized so we early exit as soon as we receive a bad trait

            cards.append(card_attr)

    # Sorting by date and then name to prepare for duplicate removal
    sorted_by_date = sorted(cards, key=lambda x: x["releaseDate"])
    sorted_by_name_date = sorted(cards, key=lambda x: x["name"])

    # Removing 61571 duplicates, keeping only the original prints
    no_dupes_cards = []
    for x in range(len(sorted_by_name_date)):
        current_name = sorted_by_name_date[x]["name"]
        if (x != len(sorted_by_name_date)-1):
            next_name = sorted_by_name_date[x+1]["name"]
            if current_name == next_name: continue
            else: no_dupes_cards.append(sorted_by_name_date[x])
        else: no_dupes_cards.append(sorted_by_name_date[x])

    print("Finished parsing...")

    return no_dupes_cards