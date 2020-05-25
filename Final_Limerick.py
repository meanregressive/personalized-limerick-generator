import random
from datamuse import datamuse
import urllib.request


def main():
    """
    This program generates a random customized limerick.

    It does this by:
     (i)    asking the user for a name,
     (ii)   extracting the last syllable of the user's name (rule-based),
     (iii)  identifying words that rhyme with the syllable, using Datamuse
     (iv)   randomly choosing from a list of best-suited rhyming words (checks against list of common nouns)
     (v)    plugging the rhyming word into a limerick template,
            randomly chosen from a set of 10 pre-defined limerick templates.

    The program then asks for feedback from the user
    and continues for as long as the user chooses.

    All limericks composed by program author Deboleena Rakshit.

    This program is likely to be extended in future
    to match names with rhyming words more effectively and
    potentially to auto-generate the limerick templates themselves.

    Thanks for your interest in the program!

    Note: You will need to install Datamuse if not already installed.
    The code for doing this on Python 3 is below.

    $ python3 -m pip install python-datamuse
    """
    display_welcome()
    play = True

    while play:
        name = get_name()
        to_rhyme = last_syll(name)
        rhyme_list = get_rhyming_words(to_rhyme)

        if rhyme_list == []:
            # If no suitable matches found, check if user wants to continue
            print('Sorry! Not able to find a close enough match.')
            yesno = input('Would you like to try with a different spelling? (Y/N) ')
            play = check_play(yesno)
            continue

        rhymes = pick_rhyme(rhyme_list)
        choose_print_limerick(name, rhymes)
        play = get_feedback()

    print('Thanks for trying the PLG, ' + name + '!')


def display_welcome():
    print('This is the Personalized Limerick Generator (PLG). Enter your name to read a limerick unique to you!')


def get_name():
    """
    params: none

    Function asks user to input name, checks if name consists only of letters,
    capitalizes it and returns name.

    returns: str
    """
    name = input('Enter your name: ')
    while not name.isalpha():
        print('Please only use letters!')
        name = input('Enter your name: ')
    name = name.capitalize()
    return name


def last_syll(name):
    """
    params: str

    Function takes name from main, and returns full name if under 3 letters.
    If longer than 3 letters, function checks characters in reverse sequence
    for a vowel. After finding first vowel, returns vowel and
    next letter, corrects sequence, and returns last syllable
    for identifying rhyming words.

    returns: str
    """
    vow = ['a', 'e', 'i', 'o', 'u']
    max_length = len(name)
    last_syll = ''
    if max_length < 3:
        last_syll = name
    else:
        for i in reversed(range(0, max_length)):
            if name[i] not in vow:
                last_syll += name[i]
            else:
                last_syll += name[i]
                last_syll += name[i - 1]
                break
        last_syll_corrected = last_syll[::-1]
        last_syll = last_syll_corrected
    return last_syll


def get_alternate_syllable(to_rhyme):
    """
    params: str

    In case no good matches found with the original syllable,
    this function finds an alternate syllable that only returns the first vowel
    from the reverse order and the letters following it, i.e. not the vowel
    and the letter before it in the name.

    returns: str
    """

    vow = ['a', 'e', 'i', 'o', 'u']
    max = len(to_rhyme)
    alt_syll = ''

    for i in reversed(range(0, max)):
        if to_rhyme[i] not in vow:
            alt_syll += to_rhyme[i]
        else:
            alt_syll += to_rhyme[i]
            break
    alt_syll_corrected = alt_syll[::-1]
    alt_syll = alt_syll_corrected
    return alt_syll


def get_rhyming_words(to_rhyme):
    """
    params: str

    This function uses Datamuse to check for rhyming words
    with the last syllable of the user's name.
    It checks against the original last syllable,
    calls get_alternate_syllable if that yields no matches,
    and returns empty list if neither yields matches.

    returns: list
    """
    api = datamuse.Datamuse()

    # Does first check for exact rhymes for last syllable
    rhyme_matches = api.words(rel_rhy=to_rhyme, md='p''s')
    match_list = get_list(rhyme_matches)

    # Does second check for exact rhymes for alternate syllable
    if match_list == []:
        alt_syll = get_alternate_syllable(to_rhyme)
        rhyme_matches = api.words(rel_rhy=alt_syll, md='p''s')
        match_list = get_list(rhyme_matches)

    # Does third check for common English words
    url = "http://www.desiquintans.com/downloads/nounlist/nounlist.txt"
    file = urllib.request.urlopen(url)

    text_list = []
    for line in file:
        decoded_line = line.decode("utf-8")
        decoded_line = decoded_line.strip()
        text_list.append(decoded_line)

    matched_list = []

    for rhyme in match_list:
        for word in text_list:
            if rhyme == word:
                matched_list.append(rhyme)

    if matched_list == []:
        return match_list
    else:
        return matched_list


def get_list(rhyme_matches):
    # Helper function to get_rhyming_words to get list of rhyming words
    match_list = []
    for result in rhyme_matches:
        try:
            if result['score'] > 90:
                if 'n' in result['tags']:
                    if result['numSyllables'] < 3:
                        if len(result['word']) > 3:
                            match_list.append(result['word'])
        except:
            pass
    return match_list




def pick_rhyme(rhyme_list):
    """
    params: list

    Function picks rhyming word from list

    returns: str
    """
    max = (len(rhyme_list))-1
    rhyme_choice = random.randint(0, max)
    rhymes = rhyme_list[rhyme_choice]
    return rhymes


def choose_print_limerick(name, rhymes):
    """
    params: str

    This function takes the user's name from main and rhymes from get_rhyming_words
    to randomly choose one of 5 pre-defined limericks, plug in the variables,
    and prints out the limerick

    returns: none
    """
    limerick_choice = random.randint(1, 10)
    print()

    if limerick_choice == 1:
        A1 = 'I met a martian called ' + name
        A2 = 'Who had a strange addiction to ' + rhymes
        A3 = 'When I asked, "Why on Earth?"'
        A4 = name + ' cried out with mirth'
        A5 = '"Why else but for the ' + rhymes + '?"'

        print(A1, A2, A3, A4, A5, sep='\n')

    if limerick_choice == 2:
        if rhymes[0] in ['a', 'e', 'i', 'o', 'u']:
            article = 'an'
        else:
            article = 'a'

        B1 = 'This is the curious story of ' + name
        B2 = 'Whose secret passion was to be ' + article + ' ' + rhymes
        B3 = 'Each day and night'
        B4 = name + ' sighed and sighed—'
        B5 = '"If only I could have been ' + article + ' ' + rhymes + '!"'

        print(B1, B2, B3, B4, B5, sep='\n')

    if limerick_choice == 3:
        C1 = 'There once lived a unicorn ' + name
        C2 = 'Who had a pet ' + rhymes.capitalize()
        C3 = name + ' loved it so much'
        C4 = "They'd let no one else touch"
        C5 = "Their sweet little pet, " + rhymes.capitalize()

        print(C1, C2, C3, C4, C5, sep='\n')

    if limerick_choice == 4:
        D1 = 'A crotchety coder named ' + name
        D2 = 'Loved nothing more than ' + rhymes
        D3 = 'Nothing could be worse–-'
        D4 = 'It made ' + name + ' curse and curse'
        D5 = '–-Than when ' + name + ' ran out of ' + rhymes

        print(D1, D2, D3, D4, D5, sep='\n')

    if limerick_choice == 5:
        E1 = 'If you ever meet ' + name
        E2 = 'Do ask them about ' + rhymes
        E3 = name + ' denies this, of course—'
        E4 = "But I'd bet a horse!—"
        E5 = 'That ' + name + ' still has my ' + rhymes + '!'

        print(E1, E2, E3, E4, E5, sep='\n')

    if limerick_choice == 6:
        F1 = 'Let me tell you about ' + name
        F2 = 'And ' + name + "'s" + ' collection of ' + rhymes + 's'
        F3 = "You'd scarcely believe"
        F4 = "That " + name + " can live"
        F5 = 'While their house is overrun with ' + rhymes + 's'
    
        print(F1, F2, F3, F4, F5, sep = '\n')

    if limerick_choice == 7:
        G1 = 'This old farmer called ' + name
        G2 = 'Loved to exclaim, "' + rhymes.capitalize() + '!"'
        G3 = "Early each morn"
        G4 = name + "'d look upon their corn"
        G5 = 'And announce with delight, "' + rhymes.capitalize() + '!"'

        print(G1, G2, G3, G4, G5, sep='\n')

    if limerick_choice == 8:
        H1 = 'Old ' + name + ' as a young child'
        H2 = 'Was more than a good bit wild'
        H3 = "The elders'd cry, 'Oh " + name + "!"
        H4 = "If only you were more like " + rhymes.capitalize() + "!'"
        H5 = 'But ' + name + ' had already taken flight'

        print(H1, H2, H3, H4, H5, sep='\n')

    if limerick_choice == 9:
        I1 = name + ' was an irrepressible cat'
        I2 = "Who'd steal anything it could get at"
        I3 = 'The neighbors often saw ' + name
        I4 = 'Crouched with a bowl of ' + rhymes
        I5 = 'And think, "Oh, ' + "THAT'" + 'S' + ' what became of that!"'

        print(I1, I2, I3, I4, I5, sep = '\n')

    if limerick_choice == 10:
        J1 = "If you've ever come across " + name
        J2 = "You'd better hide your " + rhymes
        J3 = 'As rumor would have it'
        J4 = name + ' has a bad habit'
        J5 = 'Of quickly parting fools from their ' + rhymes

        print(J1, J2, J3, J4, J5, sep = '\n')


def get_feedback():
    """
    params: none

    Function asks user for feedback on the limerick
    and calls another function to check
    whether to continue the program

    returns: boolean
    """
    print()

    valid = True
    while valid:
        try:
            score = int(input('On a scale of 1 to 5, how would you rate your limerick? '))
            if score > 5 or score < 1:
                print('Please use a scale of 1 to 5!')
                score = int(input('On a scale of 1 to 5, how would you rate your limerick? '))
        except:
            print('Please use a scale of 1 to 5!')
            continue
        valid = False

    if score >= 3:
        yesno = input('Glad you liked it! Give it another spin? (Y/N) ')
        play = check_play(yesno)
        return play

    else:
        yesno = input("That's too bad! Do you want to give it another spin? (Y/N) ")
        play = check_play(yesno)
        return play


def check_play(yesno):
    # Helper function to check if user wants to continue the program; returns Boolean
    if yesno.isalpha():
        yesno = yesno.capitalize()
    else:
        yesno = input('Please enter Y/N only! ')
        yesno = yesno.capitalize()

    while yesno != 'Y' and yesno != 'N':
        yesno = input('Please enter Y/N only! ')
        yesno = yesno.capitalize()
    if yesno == 'Y':
        return True


if __name__ == '__main__':
    main()