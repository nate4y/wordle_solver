from wordle_util import WordleSolver

if __name__ == "__main__":
    ws = WordleSolver()

    # Calculate and Store Initial Guess Scores
    regenerate_initial_guesses = False
    if regenerate_initial_guesses:
        initial_scores = ws.find_best_initial_guesses_for_answer_count(5000)
        ws.write_initial_guess_averages_to_file(initial_scores)

    answer = ws.choose_random_answer()
    ws.play(answer)