def wpm(words, time): # plain words per minute (including errors)
    gross_wpm = (words)/(time/60) # /5 because a word is considered 5 characters
    return round(gross_wpm, 2)

def error_rate(errors, correct_chars, total_chars):
    # error_rate = errors / (time/60) 
    print(errors)
    print(correct_chars+1)
    print(total_chars)
    error_rate = (((correct_chars+1)-errors)/total_chars) * 100
    #error_rate = (errors/correct_chars) * 100
    return round(error_rate, 1)  

def net_wpm(gross_wpm, error_rate): # words per minute - errors (accuracy)
    # net_wpm = gross_wpm - error_rate 
    net_wpm = gross_wpm - error_rate
    return round(net_wpm, 1)

def chpm(time, characters_typed):
    "Or words * 5 but that seems inaccurate"
    chpm = characters_typed / (time/60)
    return round(chpm, 1)