"""코디세이 OT 퀴즈 게임"""
import json
from pathlib import Path

STATE_FILE = Path(__file__).parent / "state.json"  # 프로젝트 루트의 state.json


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
    
def read_text(prompt):
    """비어 있지 않은 문자열을 입력할 때까지 반복해서 묻는다."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("⚠️ 내용이 비어 있습니다. 다시 입력하세요.")



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

    def to_dict(self):
        """JSON으로 저장할 수 있도록 딕셔너리로 바꾼다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }


def create_default_quizzes():
    """코디세이 OT 자료로 만든 기본 퀴즈 목록을 돌려준다."""
    return [
        Quiz("코디세이 AI 올인원 제1기 입학연수과정 기간은?",
             ["10.1 ~ 10.31", "10.28 ~ 11.27", "11.1 ~ 11.30", "10.28 ~ 12.27"], 2),
        Quiz("입학연수과정 장학금 금액은?",
             ["50만원", "80만원", "100만원", "150만원"], 3),
        Quiz("장학금을 받기 위한 교육장 누적 출입 시간 기준은?",
             ["60시간 이상", "80시간 이상", "100시간 이상", "120시간 이상"], 2),
        Quiz("장학금을 받기 위한 동료평가 최소 횟수는? (평가하기·받기 각 1회 이상 필수)",
             ["3회", "4회", "5회", "6회"], 4),
        Quiz("본과정 선발 기준 중 배점이 가장 큰 항목은?",
             ["기초역량(시험)", "참여의지(OT 참석, 출입시간, 동료평가)", "협업 및 태도(Term Project)", "출석 횟수"], 2),
        Quiz("하루에 인정되는 최대 출입 시간은?",
             ["8시간", "10시간", "12시간", "24시간"], 3),
        Quiz("동료평가 규칙으로 옳은 것은?",
             ["원격으로 평가해도 된다", "평가자의 PC에서 진행한다",
              "한 명이라도 불참하면 해당 평가는 Fail이다", "'AI가 작성한 코드'라고 설명해도 된다"], 3),
        Quiz("코디세이 AI 도구 '네이토(Neito)'라는 이름의 유래는?",
             ["그리스어로 '지혜'라는 뜻", "아테나가 변신했던 조언자 '멘토'의 다른 이름",
              "코디세이 개발자의 이름", "'Network'의 줄임말"], 2),
    ]

def is_valid_quiz_data(item):
    """파일에서 읽은 퀴즈 한 개가 올바른 형식인지 검사한다."""
    return (
        isinstance(item, dict)
        and isinstance(item.get("question"), str)
        and isinstance(item.get("choices"), list)
        and len(item["choices"]) == 4
        and isinstance(item.get("answer"), int)
        and 1 <= item["answer"] <= 4
    )

class QuizGame:
    """게임 전체(메뉴, 진행)를 관리하는 클래스"""

    def __init__(self):
        self.is_running = True
        self.quizzes = []
        self.best_score = None  # 아직 푼 적 없으면 None
        self.load_state()

    def load_state(self):
        """state.json에서 퀴즈와 최고 점수를 불러온다."""
        if not STATE_FILE.exists():
            self.quizzes = create_default_quizzes()
            print("📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다.")
            return

        try:
            with open(STATE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            quizzes = []
            for item in data["quizzes"]:
                if not is_valid_quiz_data(item):
                    raise ValueError("퀴즈 형식 오류")
                quizzes.append(Quiz(item["question"], item["choices"], item["answer"]))

            best_score = data.get("best_score")
            if best_score is not None and not isinstance(best_score, int):
                raise ValueError("점수 형식 오류")

        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
            print("⚠️ 저장 파일이 손상되어 기본 퀴즈 데이터로 복구합니다.")
            self.quizzes = create_default_quizzes()
            self.best_score = None
            self.save_state()
            return

        self.quizzes = quizzes
        self.best_score = best_score
        score_text = f"{best_score}점" if best_score is not None else "기록 없음"
        print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(quizzes)}개, 최고점수 {score_text})")

    def save_state(self):
        """현재 퀴즈와 최고 점수를 state.json에 저장한다."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except OSError:
            print("⚠️ 파일 저장 중 오류가 발생했습니다.")

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

    def play_quiz(self):
        """등록된 퀴즈를 순서대로 출제하고 결과를 보여준다."""
        if not self.quizzes:
            print("\n📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        total = len(self.quizzes)
        correct_count = 0
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)\n")

        for number, quiz in enumerate(self.quizzes, start=1):
            quiz.display(number)
            user_answer = read_number("정답 입력: ", 1, len(quiz.choices))
            if quiz.is_correct(user_answer):
                print("✅ 정답입니다!\n")
                correct_count += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.\n")

        score = round(correct_count / total * 100)
        print("=" * 40)
        print(f"🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score}점)")
        print("=" * 40)

    def add_quiz(self):
        """문제, 선택지 4개, 정답 번호를 입력받아 새 퀴즈를 추가하고 저장한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        question = read_text("문제를 입력하세요: ")

        choices = []
        for number in range(1, 5):
            choices.append(read_text(f"선택지 {number}: "))

        answer = read_number("정답 번호 (1-4): ", 1, 4)

        self.quizzes.append(Quiz(question, choices, answer))
        self.save_state()
        print("\n✅ 퀴즈가 추가되었습니다!")

    def show_quiz_list(self):
        """등록된 퀴즈의 문제를 번호와 함께 보여준다."""
        if not self.quizzes:
            print("\n📭 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print("-" * 40)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print("-" * 40)

    def handle_choice(self, choice):
        if choice == 1:
            self.play_quiz()
        elif choice == 2:
            self.add_quiz()
        elif choice == 3:
            self.show_quiz_list()
        elif choice == 4:
            print("\n🚧 점수 확인 기능은 준비 중입니다.")

        elif choice == 5:
            self.save_state()
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