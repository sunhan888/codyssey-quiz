"""퀴즈 한 문제를 표현하는 Quiz 클래스"""


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