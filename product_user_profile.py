import nltk

dry_class = ["dry skin", "from drying out", "dry and combination skin",
             "dry weather", "dry winter", "dry condition", "dry, flaky skin",
             " dryness", "dry spots", "dry, itchy skin", "dry winter skin"]

oily_class = ["oily skin", "oily and combination skin", "not oily", 
              "oily/combination skin"]

#For a category, calculate score of that category
#by counting the number of times a term in that category
#is mentioned in the reviews and multiply it by the
#normalized rating
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

    list_of_text = item_dict["Reviews"]
    total_reviews = len(list_of_text)

    #This is to smooth out the case where there are too few reviews
    smooth_reviews = total_reviews +100

    for review_text in list_of_text:
        
        new_text = review_text[0].lower()
        rev_rating = review_text[1]

        dry_skin += category_score(new_text,dry_class,rev_rating)
        oily_skin += category_score(new_text,oily_class,rev_rating)
        combination_skin += category_score(new_text,combination_class,rev_rating)
        sensitivity += category_score(new_text,sensitive_class,rev_rating)

    return [dry_skin/smooth_reviews, oily_skin/smooth_reviews, combination_skin/smooth_reviews, sensitivity/smooth_reviews]