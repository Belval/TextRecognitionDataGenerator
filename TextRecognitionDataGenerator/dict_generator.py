from random import randint
import os


def rand_sequence(characters, sequence_length):
    """
    Create random sequences of characters with given length from pool of characters
    :param characters: string from which to sample characters
    :param sequence_length: int with length of sequence to be returned
    :return: string with random sequence
    """
    sequence = ''
    for _ in range(sequence_length):
        r = randint(1, len(characters)) - 1
        sequence += (characters[r])
    return sequence


def get_char_pool(char_pool_arg):
    char_pool = ''
    if "let" in char_pool_arg:
        char_pool += "ABCDEFGHIJKLMNOPQRSTUVXYZ"
    if "num" in char_pool_arg:
        char_pool += "0123456789"
    if "sym" in char_pool_arg:
        char_pool += ".,-+:*%/"

    return char_pool


def write_random_dict(char_pool_arg, char_per_seq_min, char_per_seq_max, n_new_sequences=None, new_dict=None,
                      base_dict=None):
    """
    Writes a ned dictionary in dict/ that is then used by 'run.py -l mydict' to generate images
    :param char_pool_arg: String including any combination of "let","num","sym" to include letters, numbers, symbols
    :param char_per_seq_min: Minimum sequence length
    :param char_per_seq_max: Maximum sequence length
    :param n_new_sequences: New sequences to be created
    :param new_dict: Name of .txt-File containing new dictionary to be created
    :param base_dict: Name of .txt-File on which to base new dict
    """

    if base_dict and not base_dict.endswith('.txt'):
        base_dict += '.txt'
    if new_dict and not new_dict.endswith('.txt'):
        new_dict += '.txt'

    # If no name for new dict is given, use argument for char_pool, e.g. "letnumsym.txt"
    if not new_dict:
        new_dict = char_pool_arg + '.txt'
    output_file = os.path.join("dicts", new_dict)

    char_pool = get_char_pool(char_pool_arg)
    if not base_dict and not n_new_sequences:
        # If n_new_sequences == None, but base_file != None: Create as many new sequences as words in base_file
        raise ValueError("Specify either base_file or n_new_sequences")

    with open(output_file, 'w') as f:
        # If base_file is specified, add those words to output_file first
        if base_dict:
            input_file = os.path.join("dicts", base_dict)
            with open(input_file, 'r') as b:
                line_count = 0
                for line in b:
                    f.write(line)
                    # f.write(line.capitalize())
                    # f.write(line.upper())
                    line_count += 1

                # Create as many new sequences as existing words
                if not n_new_sequences:
                    n_new_sequences = line_count

        # Create new random sequences from string "chars"
        for i in range(int(n_new_sequences)):
            sequence_length = randint(char_per_seq_min, char_per_seq_max)
            sequence = rand_sequence(char_pool, sequence_length)
            f.write(sequence + '\n')


if __name__ == '__main__':
    write_random_dict("letnumsym", char_per_seq_min=2, char_per_seq_max=10, n_new_sequences=1e5)
    write_random_dict("letnumsym", char_per_seq_min=2, char_per_seq_max=10, new_dict="en_letnumsym", base_dict="en")
