from pyqode.core.modes import spellchecker_mode as scm


request_data = {
    'code': """
(Correct correct.)
(Correct correct)
(Incorrect1 incorrect2.)
(Incorrect1 incorrect2.)
(Incorrect3 incorrect4)
Single parenthetical words can also be (correct) or (incorrect5)
Single quoted words can also be 'correct' or 'incorrect6'
Single quoted words can also be "correct" or "incorrect7"
Correct!
Correct?
Correct:
Correct;
__Correct__
__Incorrect13__
Incorrect8!
Incorrect9?
Incorrect10:
Incorrect11;
Single parenthetical words can also be [correct] or [incorrect12]
Words like xx should be correct
Words like can't should be correct
Words like cna't should be incorrect
8wordds that start with numbers should also be correct
"""
}

for row in scm.run_spellcheck(request_data):
    print(row)

# import re
# WORD_PATTERN = r'[\s\[\(\{](?P<word>[\w\'][\w\']([\w\']+))'

# code = "This is 'correct'"

# for group in re.finditer(WORD_PATTERN, code):
#     word = group.group('word')
#     print(word.strip('\'"'))
#     
