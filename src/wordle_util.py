import random
import csv 

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
                self.guessScores[word] = []
        return lines
    
    def load_guesses(self):
        lines = []
        with open('word_lists/valid_guesses.txt', 'r') as file:
            for word in file.read().splitlines():
                lines.append(word)
                self.guessScores[word] = []
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
            score = self.calculate_guess_points(guess, answer)
            self.guessScores[guess].append(score)
            guesses[guess] = self.calculate_guess_points(guess, answer)
        
        for guess in self.valid_answers:
            score = self.calculate_guess_points(guess, answer)
            self.guessScores[guess].append(score)
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
                    score = score + 2
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
        #print("\n*** ANSWERS ***")
        print(f'\nSimulating inital guesses for {count} answers.')
        print('************************************************\n')
        for i in range(0, count):
            if (i + 1) % 100 == 0:
                print(f'{i + 1} initial guess simulations completed.')
            answer = self.choose_random_answer()
            #print(answer)
            self.simulate_guesses(answer)

        print("\n***********************************************\n")
        
        return self.calculate_and_sort_average_scores()

    def calculate_and_sort_average_scores(self):
        guessAverages = {}
        for guess in self.guessScores:
            totalScore = 0
            for score in self.guessScores[guess]:
                totalScore += score
            guessAverages[guess] = totalScore / len(self.guessScores[guess])
    
        return sorted(guessAverages.items(), key=lambda x:x[1], reverse=True)
    
    def write_initial_guess_averages_to_file(self, averages):
        with open('results/initial_guess_averages.csv', 'w') as f:
            for guess in averages:
                f.write(f'{guess[0]},{guess[1]}\n')

    def load_best_x_initial_guesses(self, count):
        initial_guesses = []
        with open('results/initial_guess_averages.csv', 'r') as f:
            reader = csv.reader(f)
            counter = 0
            for row in reader:
                if counter > count:
                    break
                initial_guesses.append(row[0])
                counter += 1

        return initial_guesses
    
    def generate_guess(self, green_letters, yellow_letters, gray_letters):
        word_heirarchy = self.load_best_x_initial_guesses(10000)
        if len(green_letters) == 0:
            if len(yellow_letters) == 0:
                if len(gray_letters) == 0:
                    return self.load_best_x_initial_guesses(1)[0]
                else:
                    for word in word_heirarchy:
                        valid = True
                        for c in gray_letters:
                            if c in word:
                                valid = False
                                break
                        if valid:
                            return word
            else:
                for word in word_heirarchy:
                    valid = True
                    for yc in yellow_letters:
                        for gc in gray_letters:
                            if yc not in word or gc in word:
                                valid = False
                                break
                    if valid:
                        return word
        else:
            for word in word_heirarchy:
                valid = True
                chars = [*word]

                for g in green_letters:
                    if chars[green_letters[g]] != g:
                        valid = False
                        break
                    for yc in yellow_letters:
                        if yc not in word:
                            valid = False
                            break
                    for gc in gray_letters:
                        if gc in word:
                            valid = False
                            break
                if valid:
                    return word
                
    def calculate_greens(self, guess, answer):
        green_letters = {}
        for i in range(0, len(guess)):
            if guess[i] == answer[i]:
                green_letters[guess[i]] = i
        return green_letters
    
    def calculate_yellows(self, guess, answer):
        yellow_letters = []
        for i in range(0, len(guess)):
            if guess[i] in answer and guess[i] != answer[i]:
                yellow_letters.append(guess[i])
        return yellow_letters
    
    def calculate_gray(self, guess, answer):
        gray_letters = []
        for c in guess:
            if c not in answer:
                gray_letters.append(c)
        return gray_letters
                
    def play(self, answer):
        guessCount = 0
        guess = random.choice(self.load_best_x_initial_guesses(5))
        print(f'ANSWER: {answer}\n')
        gray = []
        while guess != answer and guessCount < 50:
            print(guess)

            green = self.calculate_greens(guess, answer)
            print(f'Green: {green}')

            yellow = self.calculate_yellows(guess, answer)
            print(f'Yellow: {yellow}')

            gray.extend(self.calculate_gray(guess, answer))
            print(f'Gray: {gray}')


            guess = self.generate_guess(green, yellow, gray)
            guessCount += 1
            print('\n')
        
        green = self.calculate_greens(guess, answer)
        print(f'Green: {green}')

        yellow = self.calculate_yellows(guess, answer)
        print(f'Yellow: {yellow}')

        gray.extend(self.calculate_gray(guess, answer))
        print(f'Gray: {gray}')

        print(f'\nGuessed {guess} in {guessCount + 1} guesses')