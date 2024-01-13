from wordle_util import WordleSolver

if __name__ == "__main__":
    ws = WordleSolver()
    for i in range(0, 1):
        answer = ws.choose_random_answer()
        best_guesses = ws.find_best_guesses(answer)
        print(f'\n***ANSWER****\n{answer}')
        print('\n***BEST INITIAL GUESSES ***')
        for guess in best_guesses:
            print(f'{guess[0]}: {guess[1]}')
