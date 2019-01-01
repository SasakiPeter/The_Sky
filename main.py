from memory import Memory
from register import registerPlayers, selectLevel


def main():
    players = registerPlayers()
    height, width = selectLevel()
    memory = Memory(height, width, players)
    memory.run()


if __name__ == '__main__':
    main()
