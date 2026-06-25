# GETS CONTENTS OF PLAY
# this is done by using "Contents" and "Dramatis personae" as markers for the beginning and end of the contents section
# the contents are sliced according to these markers

def get_contents(script_text):

    found_contents_start = False
    found_contents_end = False

    for i, line in enumerate(script_text):
        if line.strip() == "Contents":
            found_contents_start = True
            script_text = script_text[i:]
            break

    for i, line in enumerate(script_text):
        if line.strip() == "Dramatis Personæ" or line.strip() == "Dramatis Personae":
            found_contents_end = True
            script_text = script_text[:i]
            break

    if found_contents_start and found_contents_end:
        return script_text

    else: return None

# GETS PERSONAE OF PLAY
# this is done by using "Dramatis personae" and "Scene" as markers for the beginning and end of the personae section
# the personae is sliced according to these markers

def get_personae(script_text):

    found_personae_start = False
    found_personae_end = False

    for i, line in enumerate(script_text):
        if line.strip() == "Dramatis Personæ" or line.strip() == "Dramatis Personae":
            found_personae_start = True
            script_text = script_text[i+1:]
            break

    for i, line in enumerate(script_text):
        if line.strip().startswith("SCENE"):
            found_personae_end = True
            script_text = script_text[:i]
            break

    if found_personae_end and found_personae_start:
        return script_text
    else: return None

# GETS PLAY
# this is done by finding the first "scene" after the dramatis personae and starting the play there, then looking for *** END
# the play is sliced according to these markers

def get_play(script_text):
    for i, line in enumerate(script_text):
        if line.strip() == "Dramatis Personæ" or line.strip() == "Dramatis Personae" :
            script_text = script_text[i:]
            break

    for i, line in enumerate(script_text):
        if line.strip().startswith("SCENE"):
            script_text = script_text[i+1:]
            break

    for i, line in enumerate(script_text):
        if line.strip() == "":
            script_text = script_text[i:]
            break

    for i, line in enumerate(script_text):
        if line.strip().startswith("*** END"):
            script_text = script_text[:i]
            break

    return script_text

# GETS ACTS OF PLAY
# This is done by searching through the play for the correct act, then the capturing flag is set and the end of that
# act is searched for, the list is then sliced accordingly

def get_act(play, act_num):
    act = None
    current_act = 0
    last_act_line = 0
    capturing = False
    for i, line in enumerate(play):
        if line.strip().startswith("ACT ") and capturing == False:
            last_act_line = i
            current_act += 1
            if act_num == current_act:
                capturing = True

        elif line.strip().startswith("ACT ") and capturing == True:
            act = play[last_act_line:i]
            break
    if capturing and act is None:
        act = play[last_act_line:]
    return act

# GETS SCENES OF PLAY
# This is done by searching through the act for the correct scene, then the capturing flag is set and the end of that
# scene is searched for, the list is then sliced accordingly

def get_scene(act, scene_num):
    scene = None
    current_scene = 0
    last_scene_line = 0
    capturing = False
    for i, line in enumerate(act):
        if line.strip().startswith("SCENE ") and capturing == False:
            last_scene_line = i
            current_scene += 1
            if scene_num == current_scene:
                capturing = True

        elif line.strip().startswith("SCENE ") and capturing == True:
            scene = act[last_scene_line:i]
            break

    if capturing and scene is None:
        scene = act[last_scene_line:]
    return scene


