import random

def hangman():
    # List of words to choose from
    words = ['python', 'programming', 'computer', 'algorithm', 'database', 'network']
    word = random.choice(words)
    word_letters = set(word)  # Letters in the word
    alphabet = set('abcdefghijklmnopqrstuvwxyz')
    used_letters = set()  # Letters guessed by the user
    max_wrong = 6  # Maximum number of incorrect guesses allowed
    wrong_guesses = 0

    # Display the hangman stages
    hangman_stages = [
        """
           ------
           |    |
                |
                |
                |
                |
        ==========""",
        """
           ------
           |    |
           O    |
                |
                |
                |
        ==========""",
        """
           ------
           |    |
           O    |
           |    |
                |
                |
        ==========""",
        """
           ------
           |    |
           O    |
          /|    |
                |
                |
        ==========""",
        """
           ------
           |    |
           O    |
          /|\\   |
                |
                |
        ==========""",
        """
           ------
           |    |
           O    |
          /|\\   |
          /     |
                |
        ==========""",
        """
           ------
           |    |
           O    |
          /|\\   |
          / \\   |
                |
        =========="""
    ]

    while wrong_guesses < max_wrong and len(word_letters) > 0:
        # Display current state
        print(hangman_stages[wrong_guesses])
        print('\nWord:', ' '.join(letter if letter in used_letters else '_' for letter in word))
        print('Used letters:', ' '.join(sorted(used_letters)))
        print(f'Wrong guesses left: {max_wrong - wrong_guesses}')

        # Get user input
        guess = input('Guess a letter: ').lower()
        if len(guess) != 1:
            print('Please enter a single letter.')
        elif guess not in alphabet:
            print('Please enter a valid letter.')
        elif guess in used_letters:
            print('You already guessed that letter.')
        else:
            used_letters.add(guess)
            if guess in word_letters:
                word_letters.remove(guess)
            else:
                wrong_guesses += 1
                print('Incorrect guess.')

    # Game outcome
    print(hangman_stages[wrong_guesses])
    if wrong_guesses == max_wrong:
        print(f'Game Over! The word was: {word}')
    else:
        print('Word:', word)
        print('Congratulations, you won!')

if __name__ == '__main__':
    print('Welcome to Hangman!')
    hangman()
    while input('Play again? (y/n): ').lower() == 'y':
        hangman()