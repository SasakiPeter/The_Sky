import random
import copy


class Memory:
    def __init__(self, height, width, players):
        self.H, self.W, self.N = height, width, len(players)
        self.playersName = players
        self.cache = []
        self.history = []
        self.message = ""
        self.__removeFlag = False
        self.__closeFlag = False
        self.endFlag = False
        self.prepareAnswer()
        self.createPlayer()
        self.createDisplay()

    def __str__(self):
        print(self.playersName, self.cache, self.history,
              self.answer, self.display, self.players)
        return "stringですよ"

    def getDisplay(self, *query):
        if query:
            a, b = query
            if self.display[a][b] == 0:
                # カードを開く
                self.display[a][b] = self.answer[a][b]
                # 一枚目をめくる時
                if not self.cache:
                    self.cache = [a, b]
                    if self.__closeFlag:
                        self.__closeCards(self.history[-1])
                    elif self.__removeFlag:
                        self.__removeCards(self.history[-1])
                    self.message = "もう一枚選択してください"
                # 二枚目をめくる時
                else:
                    newHistory = self.cache.copy()
                    newHistory.extend([a, b])
                    self.history.append(newHistory)
                    self.__judgeCards(newHistory)
                    self.cache = []
        return copy.deepcopy(self.display)

    def getAnswer(self):
        return self.answer

    def getResults(self):
        results = []
        for index, score in enumerate(self.players):
            results.append(f"{self.playersName[index]}:{score}")
        return results

    def getMessages(self):
        messages = copy.deepcopy(self.message)
        return messages

    def getMaxIndex(self):
        return int(self.H*self.W/2)

    def getWidth(self):
        width = copy.deepcopy(self.W)
        return width

    def prepareAnswer(self):
        cards = [i for i in range(1, int(self.H*self.W/2)+1)]*2
        for index in range(len(cards)):
            rand = random.randrange(self.H*self.W)
            [cards[index], cards[rand]] = [cards[rand], cards[index]]
        # 1d to 2d
        self.answer = [cards[i: i+self.W]
                       for i in range(0, self.H * self.W, self.H)]

    def createDisplay(self):
        self.display = [[0 for i in range(self.W)] for j in range(self.H)]

    def createPlayer(self):
        # N人のプレイヤーそれぞれの得点をリスト型にする
        self.players = [0 for i in range(self.N)]
        self.player_index = 0

    def __registerHistory(self):
        # xのマスを選択しようとしたら、エラー出るようにする
        query = self.__getQuery("捲りたいカードを選択してください")
        self.__openCard(query)
        while True:
            second = self.__getQuery("もう一枚カードを選択してください")
            if query != second:
                query.extend(second)
                self.__openCard(query)
                self.__judge(query)
                self.history.append(query)
                break
            else:
                print("同じカード選択するって、あなたやる気あるの？")
            if input("答えを教えて欲しいなら、“はい”と言うといいわ") == "はい":
                self.showAnswer()
                print("ゲームは終わりよ")
                self.endFlag = True
                break

    def __getQuery(self, comment):
        while True:
            query = [int(i) for i in input(comment).rstrip().split()]
            if len(query) == 2:
                return query
            else:
                print("正確に指定してください")

    def __openCard(self, query):
        it = iter(query)
        for a, b in zip(it, it):
            self.display[a-1][b-1] = self.answer[a-1][b-1]
        self.drawDisplay()
        it = iter(query)
        for a, b in zip(it, it):
            self.display[a-1][b-1] = 0

    # cui用のコード
    def __takeCards(self, a, b, c, d):
        self.display[a-1][b-1] = -1
        self.display[c-1][d-1] = -1

    def __removeCards(self, lastHistory):
        a, b, c, d = lastHistory
        self.display[a][b] = -1
        self.display[c][d] = -1
        self.__removeFlag = False

    def __closeCards(self, lastHistory):
        a, b, c, d = lastHistory
        self.display[a][b] = 0
        self.display[c][d] = 0
        self.__closeFlag = False

    def __judgeCards(self, newHistory):
        a, b, c, d = newHistory
        if self.answer[a][b] == self.answer[c][d]:
            # print("正解")
            self.players[self.player_index % self.N] += 2
            if sum(self.players) == self.H * self.W:
                self.message = "ゲームは終了です。結果は以下になりました。"
                self.endFlag = True
            else:
                self.message = "正解です。続けてプレイできます。"
                self.__removeFlag = True
        else:
            # print("不正解")
            self.player_index += 1
            playerName = self.playersName[self.player_index % self.N]
            self.message = f"{playerName}さんの番です。プレイヤーを交代してください"
            self.__closeFlag = True

    # cui用
    def __judge(self, newHistory):
        a, b, c, d = newHistory
        if self.answer[a-1][b-1] == self.answer[c-1][d-1]:
                # print("正解")
            self.players[self.player_index % self.N] += 2
            if sum(self.players) == self.H * self.W:
                print("ゲームは終了です。結果は以下になりました。")
                self.showResult()
                self.endFlag = True
            else:
                print("正解です。続けてプレイできます。")
                self.__takeCards(a, b, c, d)
                self.__registerHistory()
        else:
            # print("不正解")
            # 不正解したら、プレイヤー交代
            self.player_index += 1
            print("プレイヤーを交代してください")
            self.__registerHistory()

    def showResult(self):
        for index, score in enumerate(self.players):
            print(f"{self.playersName[index]}:{score}")

    def showAnswer(self):
        answer = self.answer.copy()
        answer.insert(0,  [i + 1 for i in range(self.W)])
        self.__drawBoard(answer)

    def drawDisplay(self):
        display = self.display.copy()
        display.insert(0, [i + 1 for i in range(self.W)])
        self.__drawBoard(display)

    def __drawBoard(self, board):
        for index, line in enumerate(board):
            if index == 0:
                print("  ", end="")
                for dot in line:
                    print(" "+str(dot)+" ", end=" ")
                print()
            else:
                print(index, end=" ")
                for dot in line:
                    if dot == 0:
                        print("[ ]", end=" ")
                    elif dot == -1:
                        print("[x]", end=" ")
                    else:
                        print("["+str(dot)+"]", end=" ")
                print()

    def reset(self):
        if input("もう一度プレイしますか？（yes or no）") == ("yes" or "y"):
            self.history = []
            self.endFlag = False
            self.prepareAnswer()
            self.createPlayer()
            self.createDisplay()
            self.run()

    def run(self):
        # self.showAnswer()
        self.drawDisplay()
        while not self.endFlag:
            self.__registerHistory()
        self.reset()
