from random import choice

choices = ['gawi', 'bawi', 'bo']

print("test")

def show_me_the_hand():
    print("def")
    return choice(choices[:2])
