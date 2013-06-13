from collections import Counter
import nltk
import re

#sentence = "Is it getting better? Or do you feel the same? Will it make it easier on you now? You got someone to blame You say, one love, one life When it's one need in the night One love, we get to share it Leaves you baby if you don't care for it Did I disappoint you? Or leave a bad taste in your mouth? You act like you never had love And you want me to go without Well it's too late tonight To drag the past out into the light We're one but we're not the same We get to carry each other, carry each other One! Have you come here for forgiveness? Have you come to raise the dead? Have you come here to play Jesus? To the lepers in your head Did I ask too much? More than a lot You gave me nothin' now it's all I got We're one but we're not the same Well we hurt each other then we do it again You say love is a temple, love a higher law Love is a temple, love the higher law You ask me to enter but then you make me crawl And I can't be holdin' on to what you got When all you got is hurt One love, one blood One life, you got to do what you should One life, with each other Sisters, brothers One life but we're not the same We get to carry each other, carry each other One One"

#sentence = "But there's a side to you that I never knew, never knew All the things you'd say, they were never true, never true And the games you'd play, you would always win, always win But I set fire to the rain Watched it pour as I touched your face Well, it burned while I cried 'Cause I heard it screaming out your name, your name When laying with you I could stay there Close my eyes, feel you here forever You and me together, nothing is better 'Cause there's a side to you that I never knew, never knew All the things you'd say, they were never true, never true And the games you's play, you would always win, always win But I set fire to the rain Watched it pour as I touched your face Well, it burned while I cried 'Cause I heard it screaming out your name, your name I set fire to the rain And I threw us into the flames When we fell, something died"

#sentence = "Say your prayers little one\nDon't forget my son To include everyone I tuck you in, warm within\nKeep you free from sin 'Til the sandman he comes Sleep with one eye open Gripping your pillow tight Exit light Enter night Take my hand We're off to never-never land Something's wrong, shut the light Heavy thoughts tonight And they aren't of Snow White Dreams of war, dreams of liars Dreams of dragon's fire And of things that will bite, yeah"

#sentence = "[00:14.49] See the stone set in your eyes\n[00:31.39] See the thorn twist in your side\n[00:35.47] I wait for you\n[00:40.11] Sleight of hand and twist of fate\n[00:48.29] On a bed of nails she makes me wait\n[00:53.13] And I wait without you\n[00:57.96] With or without you\n[01:02.42] With or without you\n[01:08.17] Through the storm, we reach the shore\n[01:14.48] You give it all but I want more\n[01:19.12] And I'm waiting for you\n[01:24.32] With or without you\n[01:28.42] With or without you\n[01:32.87] I can't live with or without you\n[01:43.09] And you give yourself away\n[01:56.46] And you give yourself away\n[02:00.73] And you give, and you give\n[02:05.39] And you give yourself away\n[02:09.84] My hands are tied, my body bruised\n[02:17.83] She's got me with nothing to win\n[02:22.47] And nothing left to lose\n[02:26.93] And you give yourself away\n[02:31.40] And you give yourself away\n[02:35.66] And you give, and you give\n[02:39.93] And you give yourself away\n[02:44.58] With or without you\n[02:47.55] With or without you\n[02:52.00] I can't live\n[02:57.03] With or without you\n[03:01.30] With or without you\n[03:22.84] With or without you\n[03:27.49] I can't live\n[03:32.31] With or without you\n[03:36.59] With or without you\n[03:41.24]"
#sentence = "[00:14.49] See the stone set in your eyes\n[00:31.39] See the thorn twist in your side"


def get_words(sentence):
    lines = sentence.split('\n')

    good_lines = []

    for line in lines:
        pattern = re.compile('\[[0-9]{2}:[0-9]{2}.[0-9]{2}\]')
        text = re.sub(pattern, '', line)
        if not text:
            time = line
        else:
            time = line.split(text)[0].strip()
        good_lines.append((time, text))

    clean_text = sentence.replace('\n', ' ')

    tokens = nltk.word_tokenize(clean_text)

    tagged = nltk.pos_tag(tokens)

    good_list = []

    for item in tagged:
        if item[1] in ['NN', 'NNS', 'VB']:
            good_list.append(item[0])

    c = Counter(good_list)

    time_lines = []

    print 'good_lines:', good_lines

    for line in good_lines:
        for item in c.iteritems():
            if item[0] in line[1].split(' ') and item[1] > 1:
                item = item + (line[0],)
                time_lines.append(item)

    print 'time_lines:', time_lines

    good_time_lines = dict()

    for item in time_lines:
        word = item[0]
        occur = item[1]
        time = item[2]
        if time not in good_time_lines:
            good_time_lines[time] = [(word, occur)]
        else:
            good_time_lines[time].append((word, occur))
    print good_time_lines
    return good_time_lines
