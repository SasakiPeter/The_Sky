def registerPlayers():
    players = []
    while True:
        playerName = input("プレーヤー登録をします。名前を入力してください。完了した場合は“OK”と入力してください")
        if playerName == "OK":
            break
        else:
            players.append(playerName)
            continue
    return players


def selectLevel():
    H, W = 0, 0
    while True:
        level = input("難易度を選択してください。(かんたん　or ふつう　or むずかしい)")
        if level == "かんたん":
            H, W = 2, 2
            break
        elif level == "ふつう":
            H, W = 4, 4
            break
        elif level == "むずかしい":
            H, W = 6, 6
            break
        else:
            continue
    return H, W
