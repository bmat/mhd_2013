from collections import Counter
import get_words
import nltk
import re

sentence = "Say your prayers little one\nDon't forget my son To include everyone I tuck you in, warm within\nKeep you free from sin 'Til the sandman he comes Sleep with one eye open Gripping your pillow tight Exit light Enter night Take my hand We're off to never-never land Something's wrong, shut the light Heavy thoughts tonight And they aren't of Snow White Dreams of war, dreams of liars Dreams of dragon's fire And of things that will bite, yeah"

sentence = "[00:14.49] See the stone set in your eyes\n[00:31.39] See the thorn twist in your side\n[00:35.47] I wait for you\n[00:40.11] Sleight of hand and twist of fate\n[00:48.29] On a bed of nails she makes me wait\n[00:53.13] And I wait without you\n[00:57.96] With or without you\n[01:02.42] With or without you\n[01:08.17] Through the storm, we reach the shore\n[01:14.48] You give it all but I want more\n[01:19.12] And I'm waiting for you\n[01:24.32] With or without you\n[01:28.42] With or without you\n[01:32.87] I can't live with or without you\n[01:43.09] And you give yourself away\n[01:56.46] And you give yourself away\n[02:00.73] And you give, and you give\n[02:05.39] And you give yourself away\n[02:09.84] My hands are tied, my body bruised\n[02:17.83] She's got me with nothing to win\n[02:22.47] And nothing left to lose\n[02:26.93] And you give yourself away\n[02:31.40] And you give yourself away\n[02:35.66] And you give, and you give\n[02:39.93] And you give yourself away\n[02:44.58] With or without you\n[02:47.55] With or without you\n[02:52.00] I can't live\n[02:57.03] With or without you\n[03:01.30] With or without you\n[03:22.84] With or without you\n[03:27.49] I can't live\n[03:32.31] With or without you\n[03:36.59] With or without you\n[03:41.24]"
#sentence = "[00:14.49] See the stone set in your eyes\n[00:31.39] See the thorn twist in your side"

def get_time_in_secs(time):
    (mins, secs) = time.split(':')
    return float(secs) + int(mins)*60

def get_lyrics(sentence):
    lines = sentence.split('\n')
    good_lines = []

    for line in lines:
        pattern = re.compile('\[[0-9]{2}:[0-9]{2}.[0-9]{2}\]')
        text = re.sub(pattern, '', line)
        if not text:
            time = line
        else:
            time = line.split(text)[0].strip()
        time = time[1:-1]
        time = get_time_in_secs(time)
        text = text[1:]
        good_lines.append((time, text))

    return good_lines

def get_image_lyrics(keywords, lyrics):
    #lyrics = get_lyrics(sentence)
    #print lyrics
    image_lyrics = []
    #keywords = get_words.get_keywords(sentence)
    print keywords
    for line in lyrics:
        for keyword in keywords:
            if keyword in line[1]:
                image_lyrics.append(line)
                break
    print image_lyrics
    return image_lyrics

def get_image_lyrics_2(keywords, lyrics):
    #lyrics = get_lyrics(sentence)
    #print lyrics
    image_lyrics = []
    #keywords = get_words.get_keywords(sentence)
    print keywords
    for line in lyrics:
        for subline in line[1].split(','):
            subline = (line[0], subline)
            for keyword in keywords:
                if keyword in subline[1]:
                    image_lyrics.append(subline)
                    break
    print image_lyrics
    return image_lyrics
