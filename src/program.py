from wordle_util import WordleSolver

if __name__ == "__main__":
    ws = WordleSolver()
    answer = ws.choose_random_answer()
    print(f'\n***ANSWER****\n{answer}')
    best_guesses = ws.find_best_guesses(answer)
    print('\n***BEST GUESSES ***')
    for guess in best_guesses:
        print(f'{guess[0]}: {guess[1]}')
