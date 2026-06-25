import re

# COUNTS THE NUMBER OF ACTS/SCENES
# parses through the contents looking for SCENE and ACT lines and adds these and their names to a dictionary for return

def get_acts_scenes(contents):
    acts_scenes = {}
    current_act = 0
    act_reset = False
    current_scenes = 0
    for the_line in contents:
        line = the_line.strip().lower()
        if line.startswith("act") and act_reset == False:
            current_act += 1
            acts_scenes["Act" + str(current_act)] = []
            act_reset = True
        if line.startswith("scene") and act_reset == True:
            current_scenes += 1
            acts_scenes["Act" + str(current_act)].append("Scene" + str(current_scenes))
            act_reset = True
        if line == "":
            current_scenes = 0
            act_reset = False
    return acts_scenes

# GETS THE NUMBER OF EACH WORD IN THE PLAY
# goes through the play, filtering out lines that don't appear to be spoken by characters (such as scenes, acts, char names)
# removes punctuation except for apostrophes inside words and then adds them to a word count dictionary {word:count}

def get_word_frequencies(play, characters):
    play = remove_square_brackets(play)
    words = {}
    for the_line in play:
        if the_line.startswith("SCENE ") or the_line.startswith("ACT ") \
                or the_line.strip().rstrip('.').isupper():
                # or the_line.strip().rstrip('.') in characters: #issue with this, not all characters in characters
            continue
        clean_line = ""
        for i, ch in enumerate(the_line):
            if ch.isalnum() or ch.isspace():
                clean_line += ch
            elif ch == "’":
                if (0 < i < len(the_line)-1
                        and the_line[i-1].isalpha()
                        and the_line[i+1].isalpha()):
                    clean_line += ch
            else:
                clean_line += " "

        line = clean_line.strip().lower()
        split_line = line.split()
        for word in split_line:
            if word not in words.keys():
                words[word] = 1
            else:
                words[word] += 1

    return words

# GETS CHARACTERS IN THE PLAY
# goes through a provided dramatis personae, splitting it by commas and then looking for items which are capitalised,
# these indicate named or important characters

def get_characters(dramatis_personae):
    chars = []
    for the_line in dramatis_personae:
        line_stripped = the_line.strip()
        if not line_stripped:
            continue
        line_split = re.split(r'[;,]', line_stripped)
        for name_line in line_split:
            name = name_line.strip().rstrip('.')
            name_buffer = ""
            for possible_name in name.split():
                if possible_name.isupper():
                    name_buffer += possible_name + " "
            name_buffer = name_buffer.strip()
            if name_buffer not in chars and name_buffer:
                chars.append(name_buffer.strip())

    return chars

# GET ALL UTTERANCES OF CHARACTERS IN AN ACT OR A SCENE (WORKS FOR BOTH AS THEY ARE FUNDAMENTALLY SIMILAR)
# goes through the text, and considers grouped text to be part of a single utterance, empty lines will terminate
# the utterance, a fully uppercase line of the correct structure will be considered a character for following text
# this text is stored alongside the character in a list in the dictionary, or added to the list if one exists

def get_char_utterances(act):
    char_utterance = {}
    capturing = False
    current_utterance = ""
    current_speaker = ""
    for the_line in act:
        line = the_line.strip()
        if line == "":
            if current_utterance:
                char_utterance[current_speaker].append(current_utterance)
                current_utterance = ""
            capturing = False
            current_speaker = ""
        if line!= "":
            no_punctuation = line.rstrip('.')
            if no_punctuation.isupper() and not capturing: #no_punctuation.upper is considered a character name
                if no_punctuation.startswith("ACT") or no_punctuation.startswith("SCENE"):
                    continue
                capturing = True
                current_speaker = no_punctuation
                if no_punctuation not in char_utterance.keys():
                    char_utterance[no_punctuation] = []
                continue
            if capturing:
                current_utterance += (" " + line if current_utterance else line)
    return char_utterance

# GETS SCENE NAMES
# goes through the act and looks for "SCENE" lines, these are then returned once all are identified

def get_scene_names(act):
    scenes = {}
    for the_line in act:
        line = the_line.strip()
        if line.startswith("SCENE"):
            to_add = line.split(".",1)
            if len(to_add) ==2:
                scenes[to_add[0].strip()] = to_add[1]
            else:
                scenes[to_add[0].strip()] = "No Description"
    return scenes

# GETS PHRASES IN SCENES
# goes through the scene, looking for regex which matches the phrase exactly (this is done to avoid picking up words
# within words (e.g. thou in without)
# These are added into a dictionary of occurrences with the structure {line number, number of occurrences: line}
# it is done like this to avoid duplicate keys which could occur with number of occurrences, or lines along

def phrase_in_scene(scene,phrase):
    occurrences = {}
    pattern = r"\b" + re.escape(phrase.lower()) + r"\b"

    for i, line in enumerate(scene):
        if line.startswith("SCENE ") or line.startswith("ACT ")\
                or line.strip().rstrip('.').isupper() or phrase == '':
            continue
        count = len(re.findall(pattern, line.lower()))
        if count > 0:
            occurrences[str(i) + " " + str(count)] = line #line number how many occurs

    return occurrences

# REMOVES SQUARE BRACKETS
# square brackets and their contents are identified and replaced with nothing using regex,
# to do this over potential multiple lines, the play is converted to a string and the re.dotall flag is applied
# then the play is reassembled into a list using keepends to keep the \n in the strings as they denote
# new lines when read

def remove_square_brackets(play):
    play_text = "".join(play)
    pattern = r"\[.*?\]"

    text = re.sub(pattern, "", play_text, flags=re.DOTALL)

    return text.splitlines(keepends = True)
