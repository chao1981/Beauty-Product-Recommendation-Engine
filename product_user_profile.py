#For a category, calculate score of that category
#by counting the number of times a term in that category
#is mentioned in the reviews and multiply it by the
#normalized rating
dry_class = ["dry skin", "from drying out", "dry and combination skin",
             "dry weather", "dry winter", "dry condition", "dry, flaky skin",
             " dryness", "dry spots", "dry, itchy skin", "dry winter skin",
             "dry sensitive skin"]

oily_class = ["oily skin", "oily and combination skin", "not oily", 
              "oily/combination skin", "oily/acne prone", "oily/acnes prone",
              "oily prone", "combination oily"]

combination_class = ["combination skin","combination/", "combination oily skin", 
                     "combination dry skin", "combination acne-prone skin"]

sensitive_class = ["sensitive"]

acne_class = ["acne", "break out", "broke out", "pimple", "black head", "breakout", "blemish", "blackheads"]

anti_aging_class = ["anti-aging", " aging", "wrinkle", "fine lines"]

redness_class = ["redness", "red spot", "rosacea"]

sunscreen_class = ["sunscreen", "sun protection"]
def category_score(text,category,rating):
    score = 0
    for term in category:
        score += text.count(term) * (rating - 3)
    return score


#Base on reviews of a product, built a the profile of
#the user that like this produc
def product_profiler(item_dict):
    dry_skin = 0
    oily_skin = 0
    combination_skin = 0
    sensitivity = 0
    acne = 0
    aging = 0
    sunscreen = 0
    redness = 0

    list_of_text = item_dict["Reviews"]
    total_reviews = len(list_of_text)

    #This is to smooth out the case where there are too few reviews
    smooth_reviews = total_reviews +100
    
    #Dictionary for the item with category score
    #item_score = {item_dict.keys()[0]:item_dict.values()[0][0]}
    item_score = {}

    for review_text in list_of_text:
        
        new_text = review_text[0].lower()
        rev_rating = review_text[1]

        dry_skin += category_score(new_text,dry_class,rev_rating)
        oily_skin += category_score(new_text,oily_class,rev_rating)
        combination_skin += category_score(new_text,combination_class,rev_rating)
        sensitivity += category_score(new_text,sensitive_class,rev_rating)
        acne += category_score(new_text,acne_class,rev_rating)
        aging += category_score(new_text,anti_aging_class,rev_rating)
        sunscreen += category_score(new_text,sunscreen_class,rev_rating)
        redness += category_score(new_text,redness_class,rev_rating)
        
    dry_score = dry_skin/smooth_reviews
    oily_score = oily_skin/smooth_reviews
    combination_score = combination_skin/smooth_reviews
    sensitivity_score = sensitivity/smooth_reviews
    acne_score = acne/smooth_reviews
    aging_score = aging/smooth_reviews
    sunscreen_score = sunscreen/smooth_reviews
    redness_score = redness/smooth_reviews
    
    item_score["dry_skin_score"] = dry_score
    item_score["oily_skin_score"] = oily_score
    item_score["combination_skin_score"] = combination_score
    item_score["sensitive_score"] = sensitivity_score
    item_score["acne_score"] = acne_score
    item_score["anti_aging_score"] = aging_score
    item_score["sunscreen_score"] = sunscreen_score
    item_score["redness_score"] = redness_score
    
    return item_score