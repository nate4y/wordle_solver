import random

class WordleSolver:
    valid_answers = []

    def __init__(self):
        self.valid_answers = self.load_answers()
        self.valid_guesses = self.load_guesses()

    def load_answers(self):
        lines = []
        with open('word_lists/valid_answers.txt', 'r') as file:
            for word in file.read().splitlines():
                lines.append(word)
        return lines
    
    def load_guesses(self):
        lines = []
        with open('word_lists/valid_guesses.txt', 'r') as file:
            for word in file.read().splitlines():
                lines.append(word)
        return lines

    def check_valid_guess(self, guess):
        if guess in self.valid_answers:
            return True
        else:
            if guess in self.valid_guesses:
                return True
            else:
                return False
            
    def choose_random_answer(self):
        return random.choice(self.valid_answers)
    
    def simulate_guesses(self, answer):
        guesses = {}
        for guess in self.valid_guesses:
            guesses[guess] = self.calculate_guess_points(guess, answer)
        
        for guess in self.valid_answers:
            guesses[guess] = self.calculate_guess_points(guess, answer)

        return guesses

    def find_best_guesses(self, answer):
        guesses = self.simulate_guesses(answer)
        sorted_guesses = sorted(guesses.items(), key=lambda x:x[1], reverse=True)
        return sorted_guesses[0:3]
        
    def calculate_guess_points(self, guess, answer):
        guess_chars = [*guess]
        answer_chars = [*answer]
        score = 0

        for i in range(0, len(guess_chars)):
            if guess_chars[i] == answer_chars[i]:
                score = score + 3
            
        
        return score