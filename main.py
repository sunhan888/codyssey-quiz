"""코디세이 OT 퀴즈 게임"""


def read_number(prompt, min_value, max_value):
    """min_value~max_value 사이의 정수를 올바르게 입력할 때까지 반복해서 묻는다."""
    while True:
        text = input(prompt).strip()  # 앞뒤 공백 제거

        if text == "":
            print(f"⚠️ 입력이 비어 있습니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
            continue

        try:
            number = int(text)
        except ValueError:
            print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
            continue

        if number < min_value or number > max_value:
            print(f"⚠️ 범위를 벗어났습니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
            continue

        return number

class Quiz:
    """퀴즈 한 문제를 표현하는 클래스"""

    def __init__(self, question, choices, answer):
        self.question = question  # 문제 (str)
        self.choices = choices    # 선택지 4개 (list)
        self.answer = answer      # 정답 번호 1~4 (int)

    def display(self, number):
        """문제 번호와 함께 문제와 선택지를 출력한다."""
        print("-" * 40)
        print(f"[문제 {number}]")
        print(self.question)
        print()
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")
        print()

    def is_correct(self, user_answer):
        """사용자가 고른 번호가 정답이면 True를 돌려준다."""
        return user_answer == self.answer

class QuizGame:
    """게임 전체(메뉴, 진행)를 관리하는 클래스"""

    def __init__(self):
        self.is_running = True

    def show_menu(self):
        print()
        print("=" * 40)
        print("       🎯 코디세이 OT 퀴즈 게임 🎯")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    def handle_choice(self, choice):
        if choice == 1:
            print("\n🚧 퀴즈 풀기 기능은 준비 중입니다.")
        elif choice == 2:
            print("\n🚧 퀴즈 추가 기능은 준비 중입니다.")
        elif choice == 3:
            print("\n🚧 퀴즈 목록 기능은 준비 중입니다.")
        elif choice == 4:
            print("\n🚧 점수 확인 기능은 준비 중입니다.")
        elif choice == 5:
            print("\n👋 게임을 종료합니다. 다음에 또 만나요!")
            self.is_running = False

    def run(self):
        while self.is_running:
            self.show_menu()
            choice = read_number("선택: ", 1, 5)
            self.handle_choice(choice)


if __name__ == "__main__":
    game = QuizGame()
    game.run()