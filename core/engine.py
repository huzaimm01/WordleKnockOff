def evaluate_guess(guess, answer):
    result = ["gray"] * len(answer)
    answer_chars = list(answer)
    guess_chars = list(guess)

    for i in range(len(guess_chars)):
        if guess_chars[i] == answer_chars[i]:
            result[i] = "green"
            answer_chars[i] = None
            guess_chars[i] = None

    for i in range(len(guess_chars)):
        if guess_chars[i] and guess_chars[i] in answer_chars:
            result[i] = "yellow"
            answer_chars[answer_chars.index(guess_chars[i])] = None

    return result
