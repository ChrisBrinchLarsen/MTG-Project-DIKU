import re
import datetime as dt

# Refactored regex format that we repeated a lot pulled out into a function
# Looks for instances of "trait:"?", where the question mark is the thing we're
# capturing, and trait can take any trait name.
def match_trait(trait: str, source: str):
    return re.search(r'"'+ trait + r'":"(.*?)",', source)

# Value for a regex search that gives us a default empty string if no matches are
# found instead of the special None value.
def get_trait(trait: str, source: str) -> str:
    trait_match = match_trait(trait, source)
    if trait_match != None:
        return trait_match.group(1)
    else:
        return ""

# Takes a card definition as a dictionary, returns True if the card is broken
# in the dataset or has some property that makes it bad for our use case, false
# otherwise.
def check_bad_card(card:dict) -> bool:
    # A valid card needs to have a value in all of these traits
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
    
    # If it doesn't have a value in one of the important traits, the card is broken
    for trait in important_traits:
        if card[trait] == "":
            return True
    
    # We don't deal with these card layouts because they offer ambiguity in how
    # they would be compared against other cards
    bad_layouts = {"split", "transform", "modal_dfc", "double_faced_token", "art_series", "adventure"}

    # Cards from these sets aren't considered 'proper magic cards' and stick out
    # like a sore thumb in our game when included.
    bad_set_types = {"alchemy", "funny", "token", "memorabilia", "minigame", "box", "vanguard"}

    # Cards with these types don't have the traits that we need to compare cards
    bad_types = {"token", "emblem", "conspiracy"}

    # Filtering all the above bad traits
    if card["layout"] in bad_layouts: return True
    if card["setType"] in bad_set_types: return True
    for bad_type in bad_types:
        if bad_type in card["types"]: return True
    
    # Cards only meant for online play not included
    if "alchemy" in card["promoTypes"]: return True

    # Card is good!
    return False

# We take a file downloaded from https://scryfall.com/docs/api/bulk-data
# in the "Default Cards" category. We return an array of every cards earliest
# print and some important traits about that card in a dictionary representing
# the card.
def parse_cards(file:str):
    print("\nParsing cards. This might take a moment...")

    # This array will hold all of our cards as dictionaries
    cards = []

    # We open the file with a niche encoding to deal with "★" symbols in collector IDs
    with open("data/"+file, 'r', encoding='cp437') as file:
        # Each line in the dataset represents a card
        lines = file.read().split('\n')

        # For every card in our dataset
        for line in lines:
            # First and last line don't contain a card, but only opening and closing
            # square brackets.
            if line == '[' or line == ']': continue # Skip first and last line

            # Fetching various traits from our card
            collectorID_ = get_trait("collector_number",line) # We can't make these ints due to "★" and various exceptions
            flavorText_  = get_trait("flavor_text"     ,line).replace("\\", "") # Cleaning up strings
            oracleText_  = get_trait("oracle_text"     ,line)        
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
            
            # The typeline contains all type information, but we need to extract superTypes, types and subTypes. So we
            # first split on the dash which separates the superTypes/Type field from the subtypes field, giving us easy
            # access to the subtypes.
                                                             # This complicated sequence of steps simply replaces any — with - in typelines and splits
            typeLine     = get_trait("type_line"       ,line).encode().decode("unicode-escape").replace(u"Î\x93Ã\x87Ã¶", "-").split(" - ")
            

            subTypes_ = []
            if len(typeLine) != 1:
                subTypes_ = typeLine[1].split(" ")

            # Getting all superTypes/types in an array
            left_types = typeLine[0].split(" ")

            # Since there's only a small finite number of types we list them here
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
            # If a type on the left matches our list of types it must be a type
            # otherwise it must be a superType
            for type in left_types:
                if type in validTypes:
                    types_.append(type)
                else:
                    superTypes_.append(type)

            # Keywords
            keywords_ = []
            keywords_match = re.search(r'"keywords":(\[.*?\]),', line)
            if keywords_match != None:
                # Since our dataset denotes keywords as: "keywords":["Paradox","Foretell"]
                # we can use the eval function to directly interpret the string as an
                # array
                keywords_ = eval(keywords_match.group(1))

            # Color identities
            colors_ = []
            colors_match = re.search(r'"colors":(\[.*?\]),', line)
            if colors_match != None:
                # Same logic as for keywords
                colors_ = eval(colors_match.group(1))  
            if len(colors_) == 0:
                # If card has no colors it must be colorless    
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

            # Constructing the attribute fields of our card
            card_attr = dict(
                name         = name_,
                releaseDate  = releaseDate_,
                superTypes   = superTypes_,
                types        = types_,
                subTypes     = subTypes_,
                keywords     = keywords_,
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

            # We check if the card violates any of our rules for being a valid card
            is_bad_card = check_bad_card(card_attr)
            if is_bad_card: continue  # This could be optimized so we early exit as soon as we receive a bad trait

            # If card is valid we append it to the end of our list of cards
            cards.append(card_attr)

    # Sorting by date and then name to prepare for duplicate removal
    sorted_by_date      = sorted(cards, key=lambda x: x["releaseDate"])
    sorted_by_name_date = sorted(sorted_by_date, key=lambda x: x["name"])

    # Removing duplicates, keeping only the original prints
    no_dupes_cards = []
    # We run through numbers corresponding to indexes in our total card list
    for x in range(len(sorted_by_name_date)):
        # We get the name of the current card
        current_name = sorted_by_name_date[x]["name"]
        # If we're not at the last card
        if (x != len(sorted_by_name_date)-1):
            # Save the next cards name
            next_name = sorted_by_name_date[x+1]["name"]
            # If our current card has the same name as the following card, the
            # following card must be of an earlier release, so we skip the current
            if current_name == next_name: continue
            # The names were different so our current card is the last card with
            # that name, we add it to our list of non-duplicates
            else: no_dupes_cards.append(sorted_by_name_date[x])
        # We add the final card
        else: no_dupes_cards.append(sorted_by_name_date[x])

    print("Finished parsing...")

    # We return no duplicates only keeping the original prints of every valid
    # card
    return no_dupes_cards