from random import choice

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

# 🔤 Sample words
words = ["fl*p", "plant", "gr*nt", "h*lla", "chart"]
target = choice(words)
normalized_target = target.replace("*", "").lower()
max_attempts = len(normalized_target) + 1

print("(Debug) Target word (with censor):", target)

for _ in range(max_attempts):
    guess = input(f"Enter a {len(normalized_target)}-letter guess: ").lower()
    if len(guess) != len(normalized_target):
        print("Invalid length.")
        continue

    result = evaluate_guess(guess, normalized_target)
    display = "".join({
        "green": "🟩",
        "yellow": "🟨",
        "gray": "⬜"
    }[r] for r in result)

    print(f"{guess.upper()} {display}")

    if guess == normalized_target:
        print("✅ Correct!")
        break
else:
    print(f"❌ Out of attempts. The word was: {target}")
