import random

class WordleSolver:
    valid_answers = []
    guessScores = {}

    def __init__(self):
        self.valid_answers = self.load_answers()
        self.valid_guesses = self.load_guesses()

    def load_answers(self):
        lines = []
        with open('word_lists/valid_answers.txt', 'r') as file:
            for word in file.read().splitlines():
                lines.append(word)
                self.guessScores[word] = 0
        return lines
    
    def load_guesses(self):
        lines = []
        with open('word_lists/valid_guesses.txt', 'r') as file:
            for word in file.read().splitlines():
                lines.append(word)
                self.guessScores[word] = 0
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
        return sorted_guesses[0:5]
        
    def calculate_guess_points(self, guess, answer):
        guess_chars = [*guess]
        answer_chars = [*answer]
        score = 0

        doneGreens = False
        while not doneGreens:
            if len(guess_chars) == 0:
                doneGreens = True
                break
            for i in range(0, len(guess_chars)):
                if guess_chars[i] == answer_chars[i]:
                    score = score + 3
                    guess_chars.pop(i)
                    answer_chars.pop(i)
                    break
                elif i == len(guess_chars) - 1:
                    doneGreens = True
                    break
        
        doneYellows = False
        while not doneYellows:
            # print(guess_chars)
            # print(answer_chars)
            if len(guess_chars) == 0:
                doneYellows = True
                break
            for i in range(0, len(guess_chars)):
                if guess_chars[i] in answer_chars:
                    score = score + 1
                    answer_chars.remove(guess_chars[i])
                    guess_chars.remove(guess_chars[i])
                    break
                elif i == len(guess_chars) - 1:
                    doneYellows = True
                    break
            
        return score
    
    def find_best_initial_guesses_for_answer_count(self, count):
        for i in range(0, count):
            answer = self.choose_random_answer()
