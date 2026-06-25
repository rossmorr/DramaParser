import re
import sys
import time

import cmv_algorithm
import script_getters
import summary_functions


def main():
    # global variables are used to store the play, check for some false inputs and for termination purposes
    play = None
    contents = None
    personae = None
    correct_input = True
    drama_imported = False
    drama_imported_home_error = False
    term = False

    # MENU SCREEN
    print ("\u001B[1mDrama Analysis System\u001B[0m\n")

    while True:
        print("Select an option:")

        print("\u001B[1m1.\u001B[0m Import a drama from a text file.")
        print("\u001B[1m2.\u001B[0m Print a summary report.")
        print("\u001B[1m3.\u001B[0m Output the summary report to a text file.")
        print("\u001B[1m4.\u001B[0m View details of a drama act.")
        print("\u001B[1m5.\u001B[0m Search inside a drama scene.")
        print("\u001B[1m6.\u001B[0m Unique words estimate.")
        print("\u001B[1m7.\u001B[0m Exit.\n")

        if drama_imported_home_error:
            print("A file must be imported before using that feature.\n")
            drama_imported_home_error = False
        if not correct_input:
            print ("Please select from one of the suggested inputs.\n")

        choice = input("")

        # INPUT FILE SCREEN
        # this screen will attempt to get the play, and checks it has an appropriate contents and personae section
        # if these do not exist, an error message is displayed
        # this function calls the import text function for file import, which then calls from script_getters

        if choice == "1":
            drama_imported_home_error = False
            correct_input = True
            file = import_text()
            if not file:
                continue
            play = script_getters.get_play(file)
            contents = script_getters.get_contents(file)
            personae = script_getters.get_personae(file)
            if not contents or not personae:
                print(f"File not acceptable, {'contents' if not contents else 'personae'} not found.")
                time.sleep(1.5)
                continue
            drama_imported = True

        # FIRST SUMMARY SCREEN
        # this screen calls functions in the summary functions file, and then handles the responses, formats and outputs them

        elif choice == "2":
            correct_input = True
            if not drama_imported:
                drama_imported_home_error = True
                continue
            acts_scenes = summary_functions.get_acts_scenes(contents)
            acts = 0
            scenes = 0
            for act in acts_scenes:
                acts += 1
                for scene in acts_scenes[act]:
                    scenes += 1
            print("Number of acts: " + str(acts))
            print("Number of scenes: " + str(scenes) + "\n")
            print ("Top 20 Words:")
            chars = summary_functions.get_characters(personae)
            words = summary_functions.get_word_frequencies(play, chars)
            ranking = sorted(words, key=words.get, reverse=True)
            for i, word in enumerate(ranking):
                if i< 20:
                    print ("\u001B[1m" +str(i+1) + ". " + "\u001B[0m" + word.capitalize() + ": " + str(words[word]))
                else:
                    print()
                    break
            print("Character names: ")
            for i, char in enumerate(chars):
                print("\u001B[1m" + str(i+1) + ". " + "\u001B[0m" +str(char))
            print()
            returning = input("1. Return to home screen.\n2. Exit.\n")
            while returning != "1" and returning != "2":
                returning = input("1. Return to home screen.\n2. Exit.\n")
            if returning == "1":
                continue
            break

            # SUMMARY SCREEN FILE CREATION
            # functions the same as section 2 but instead of print commands, outputs to a file
            # due to the output file being a txt file, the formatting for bold characters was removed

        elif choice == "3":
            correct_input = True
            if not drama_imported:
                drama_imported_home_error = True
                continue
            with open("summary_drama.txt", "w", encoding="utf-8") as f:
                f.write ("Summary Report of the Drama:\n\n")
                acts_scenes = summary_functions.get_acts_scenes(contents)
                acts = 0
                scenes = 0
                for act in acts_scenes:
                    acts += 1
                    for scene in acts_scenes[act]:
                        scenes += 1
                f.write("Number of acts: " + str(acts)+ "\n")
                f.write("Number of scenes: " + str(scenes)+ "\n\n")
                f.write ("Top 20 Words:"+ "\n")
                chars = summary_functions.get_characters(personae)
                words = summary_functions.get_word_frequencies(play, chars)
                ranking = sorted(words, key=words.get, reverse=True)
                for i, word in enumerate(ranking):
                    if i< 20:
                        f.write(str(i+1) + ". " + word.capitalize() + ": " + str(words[word])+ "\n")
                    else:
                        break
                f.write("\nCharacter names: \n")
                for i, char in enumerate(chars):
                    f.write(str(i+1) + ". " + str(char) + "\n")
            print("FILE CREATED")
            returning = input("1. Return to home screen.\n2. Exit.\n")
            while returning != "1" and returning != "2":
                returning = input("1. Return to home screen.\n2. Exit.\n")
            if returning == "1":
                continue
            break

            # SECOND SUMMARY SCREEN
            # takes an act number, validates it and then calls the character utterances function
            # this function is used to get a word count by counting all the words in utterances and to find who has
            # the most utterances by counting them up
            # it separately calls the scene names function to get the scenes

        elif choice == "4":
            correct_input = True
            if not drama_imported:
                drama_imported_home_error = True
                continue
            home = False
            act_choice = input("Enter act number (Positive integers only): ")
            while not act_choice.isdigit():
                print("Please enter a valid number\n")
                act_choice = input("Enter act number (Positive integers only): ")

            play_for_analysis = summary_functions.remove_square_brackets(play)
            act = script_getters.get_act(play_for_analysis, int(act_choice))

            while not act:
                returning = input("Act not found\n1. Retry\n2. Return to home screen.\n"
                                  "3. Exit\n")
                if returning not in ["1", "2", "3"]:
                    print("Please select from a given option.\n")
                    continue
                elif returning == "1":
                    act_choice = input("Enter act number (Positive integers only): \n")
                    # Validate act_choice is a number
                    while not act_choice.isdigit():
                        print("Please enter a valid number.\n")
                        act_choice = input("Enter act number (Positive integers only): \n")
                    act = script_getters.get_act(play_for_analysis, int(act_choice))
                elif returning == "2":
                    home = True
                    break
                elif returning == "3":
                    term = True
                    break
            if term:
                break
            if home:
                home = False
                continue
            char_utterances = summary_functions.get_char_utterances(act)
            utterance_count = 0
            word_count = 0
            for char in char_utterances.keys():
                for utterance in char_utterances[char]:
                    utterance_count += 1
                    utterance_split = utterance.split()
                    for word in utterance_split:
                        word_count += 1
            lengths = {k: len(v) for k, v in char_utterances.items()}
            max_key = max(lengths, key=lengths.get)
            max_val = lengths[max_key]
            max_chars = ""
            for char, length in lengths.items():
                if length == max_val:
                    max_chars += char + ", "
            min_key = min(lengths, key=lengths.get)
            min_val = lengths[min_key]
            min_chars = ""
            for char, length in lengths.items():
                if length == min_val:
                    min_chars += char + ", "
            max_chars = max_chars[:-2]
            min_chars = min_chars[:-2]
            scene_names = summary_functions.get_scene_names(act)

            print("Number of words: " + str(word_count))
            print("Number of utterances: " + str(utterance_count) + "\n")

            print("Character(s) who speak the most: " + max_chars + " - " + str(max_val) + " utterances.")
            print("Character(s) who speak the least: " + min_chars + " - " +str(min_val) + " utterances." + "\n")

            print("Names of scenes:")
            for i, name in enumerate(scene_names.values()):
                print(str(i+1) + ". " + name)
            print()
            returning = input("1. Return to home screen.\n2. Exit.\n")
            while returning != "1" and returning != "2":
                returning = input("1. Return to home screen.\n2. Exit.\n")
            if returning == "1":
                continue
            break

        # PLAY SEARCH SCREEN
        # act and scene numbers are accepted, these are then loaded and used for searching phrases in a scene, and
        # searching for the first and last lines of a character, by calling functions from summary_functions

        elif choice == "5":
            correct_input = True
            if not drama_imported:
                drama_imported_home_error = True
                continue
            home = False
            act_num = input("Enter act number (Positive integers only): ")
            while not act_num.isdigit():
                print("Please enter a valid number\n")
                act_num = input("Enter act number (Positive integers only): ")
            play_for_analysis = summary_functions.remove_square_brackets(play)
            act = script_getters.get_act(play_for_analysis, int(act_num))

            while not act:
                returning = input("Act not found\n1. Retry\n2. Return to home screen.\n3. Exit\n")
                if returning not in ["1", "2", "3"]:
                    print("Please select from a given option.\n")
                    continue
                elif returning == "1":
                    act_choice = input("Enter act number (Positive integers only): \n")
                    # Validate act_choice is a number
                    while not act_choice.isdigit():
                        print("Please enter a valid number.\n")
                        act_choice = input("Enter act number (Positive integers only): \n")
                    act = script_getters.get_act(play_for_analysis, int(act_choice))
                elif returning == "2":
                    home = True
                    break
                elif returning == "3":
                    term = True
                    break
            if term:
                break
            if home:
                home = False
                continue

            scene_num = input("Enter scene number (Positive integers only): ")
            while not scene_num.isdigit():
                print("Please enter a valid number.\n")
                scene_num = input("Enter scene number (Positive integers only): ")
            scene = script_getters.get_scene(act, int(scene_num))

            while not scene:
                returning = input("Scene not found\n1. Retry\n2. Return to home screen.\n3. Exit\n")
                if returning not in ["1", "2", "3"]:
                    print("Please select from a given option.\n")
                    continue
                elif returning == "1":
                    scene_num = input("Enter scene number (Positive integers only): \n")
                    # Validate scene_num is a number
                    while not scene_num.isdigit():
                        print("Please enter a valid number.\n")
                        scene_num = input("Enter scene number (Positive integers only): \n")
                    scene = script_getters.get_scene(act, int(scene_num))
                elif returning == "2":
                    home = True
                    break
                elif returning == "3":
                    term = True
                    break
            if term:
                break
            if home:
                home = False
                continue
            print()
            phrase_to_search = input("Search for word/phrase: ")
            phrase_occurrences = summary_functions.phrase_in_scene(scene,phrase_to_search)
            number_of_phrase = 0
            output = []
            for line_count, whole_line in phrase_occurrences.items():
                to_output = ""
                split_line_count = line_count.split()
                phrase_count = int(split_line_count[1])
                number_of_phrase += phrase_count
                for x in range(phrase_count):
                    to_output += str(number_of_phrase-phrase_count +x +1) + ". /"
                to_output = to_output[:-1]
                to_output += whole_line
                output.append(to_output)
            print("Found " + str(number_of_phrase) + " occurrences:")
            for line in output:
                print(line, end= "")
            print()
            char_to_search = input("Search for utterances by a character: ").upper()
            char_utterances = summary_functions.get_char_utterances(scene)
            while char_to_search not in char_utterances:
                returning = input("Character not found.\n1. Retry\n2. Return to home screen.\n3. Exit.\n")
                if returning not in ["1", "2", "3"]:
                    print("Please select from a given option.\n")
                    continue
                elif returning == "1":
                    char_to_search = input("Search for utterances by a character: ").upper()
                elif returning == "2":
                    home = True
                    break
                elif returning == "3":
                    term = True
                    break
            if term:
                break
            if home:
                home = False
                continue
            list_of_utterances = char_utterances[char_to_search]
            print ("F " + list_of_utterances[0])
            print ("L " + list_of_utterances[len(list_of_utterances)-1])
            print()
            returning = input("1. Return to home screen.\n2. Exit.\n")
            while returning != "1" and returning != "2":
                returning = input("1. Return to home screen.\n2. Exit.\n")
            if returning == "1":
                continue
            break

            # CMV UNIQUE WORD ESTIMATE SCREEN
            # converts the play into a string to simulate the idea from the article of feeding the play in a word at a time
            # them calls the algorithm to estimate the unique words

        elif choice == "6":
            correct_input = True
            if not drama_imported:
                drama_imported_home_error = True
                continue
            play_as_string = cmv_algorithm.get_play_as_string(play)
            print("CMV unique words estimated: " + str(cmv_algorithm.unique_words_estimate(play_as_string)))
            returning = input("1. Return to home screen.\n2. Exit.\n")
            while returning != "1" and returning != "2":
                returning = input("1. Return to home screen.\n2. Exit.\n")
            if returning == "1":
                continue
            break

            # EXIT APPLICATION
        elif choice == "7":
            correct_input = True
            break

            # If the user does not enter one of the options, the correct input flag is set so that an error message
            # will be displayed when the menu reruns
        else:
            correct_input = False


# IMPORTS TEXT
# validates a users input against what is expected for a play file (.txt)
# it will attempt to open this file and return it, using boolean flags to control error messages and flow of logic

def import_text():
    file_found = False
    script_text = None
    text_file_flag = True
    file_flag = True

    while not file_found:
        try:
            print("Please enter the name of the file including the extension \n"
                               r"e.g. 'Romeo-and-Juliet_William-Shakespeare.txt'." + "\n" +
                               "Please note this program only accepts .txt files.\n")
            if not text_file_flag:
                print ("Must be a text file check name ends .txt, or type 'x' to return.\n")
            if not file_flag:
                print ("File could not be found. Please check file name is correct, or type 'x' to return.\n")
                file_flag = True
            sys.stdin.flush()
            user_input = input()
            if user_input.lower() == 'x':
                return None
            text_file_flag = user_input[-4:] == ".txt"
            if not text_file_flag:
                continue


            f = open(user_input, "r", encoding="utf-8")
            script_text = f.readlines()
            file_found = True
        except FileNotFoundError:
            file_flag = False

    return script_text

if __name__ == "__main__":
    main()
