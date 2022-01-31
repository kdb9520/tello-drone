import pygame


def init():
    pygame.init()
    pygame.display.set_mode((400, 400))


def getKey(keyName):
    ans = False
    for event in pygame.event.get():
        pass
    key_input = pygame.key.get_pressed()
    my_key = getattr(pygame, 'K_{}'.format(keyName))
    if key_input[my_key]:
        ans = True
    pygame.display.update()
    return ans


def main():
    while True:
        if getKey("LEFT"):
            print("Left Key Pressed")
        if getKey("RIGHT"):
            print("Right Key Pressed")


if __name__ == '__main__':
    init()
    main()
