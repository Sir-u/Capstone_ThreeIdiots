import sys
from PyQt5.QtWidgets import *
import random
#import testfile

messageDict = []

class RecommendationApp(QWidget):
    option = ["옵션 1", "옵션 2", "옵션 3"]

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 전체 앱 스타일 설정
        self.setStyleSheet(
            """
            font-size: 18px;
            color: black;
            background-color: #f0f0f0;
            """
        )

        self.stacked_widget = QStackedWidget()

        # 추천 페이지
        self.recommend_page = QWidget()
        self.recommend_button = QPushButton("추천해줘")
        self.recommend_button.setStyleSheet(
            """
            background-color: #3498db;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
            """
        )
        self.recommend_button.clicked.connect(self.updateOptionPage)  # 버튼 클릭 시 옵션 선택 페이지로 이동
        recommend_layout = QVBoxLayout()
        recommend_layout.addWidget(self.recommend_button)
        self.recommend_page.setLayout(recommend_layout)

        # 옵션 선택 페이지
        self.option_page = QWidget()
        self.option_label = QLabel("텍스트를 선택하세요:")
        self.option_buttons = [QPushButton(self.option[0]), QPushButton(self.option[1]), QPushButton(self.option[2])]
        for button in self.option_buttons:
            button.setStyleSheet(
                """
                background-color: #3498db;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                """
            )
            button.clicked.connect(self.showResultPage)  # 옵션 버튼 클릭 시 결과 페이지로 이동
        self.recommend_again_button = QPushButton("재추천")
        self.recommend_again_button.setStyleSheet(
            """
            background-color: #2ecc71;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
            """
        )
        self.recommend_again_button.clicked.connect(self.updateOptionPage)  # 재추천 버튼 클릭 시 재추천 기능 실행
        option_layout = QVBoxLayout()
        option_layout.addWidget(self.option_label)
        for button in self.option_buttons:
            option_layout.addWidget(button)
        option_layout.addWidget(self.recommend_again_button)
        self.option_page.setLayout(option_layout)

        # 결과 페이지
        self.result_page = QWidget()
        self.text_label = QLabel("")
        self.back_button = QPushButton("돌아가기")
        self.back_button.setStyleSheet(
            """
            background-color: #e74c3c;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
            """
        )
        self.back_button.clicked.connect(self.showRecommendations)  # 돌아가기 버튼 클릭 시 추천 페이지로 이동
        result_layout = QVBoxLayout()
        result_layout.addWidget(self.text_label)
        result_layout.addWidget(self.back_button)
        self.result_page.setLayout(result_layout)

        # 페이지를 stacked widget에 추가
        self.stacked_widget.addWidget(self.recommend_page)
        self.stacked_widget.addWidget(self.option_page)
        self.stacked_widget.addWidget(self.result_page)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        self.setWindowTitle("추천 앱")
        self.setGeometry(100, 100, 400, 200)

        # 이전 페이지 인덱스를 추적하는 변수
        self.prevPageIndex = 0

    def showOptionPage(self):
        # 옵션 선택 페이지로 전환
        self.stacked_widget.setCurrentIndex(1)
        self.prevPageIndex = 0  # 현재 페이지가 옵션 선택 페이지이므로 이전 페이지는 추천 페이지(인덱스 0)

    def showResultPage(self):
        # 결과 페이지로 전환 또는 돌아가기 버튼을 누를 때 옵션 선택 페이지로 전환
        sender = self.sender()
        if sender == self.back_button:
            self.stacked_widget.setCurrentIndex(0)  # 돌아가기 버튼 클릭 시 첫 번째 페이지로
        else:
            selected_option = sender.text()
            self.text_label.setText(f"선택한 텍스트: {selected_option}")
            self.stacked_widget.setCurrentIndex(2)

    def showRecommendations(self):
        # 추천 페이지로 전환
        self.stacked_widget.setCurrentIndex(0)

    #def recommendAgain(self):
        

    def updateOptionPage(self):
        for i in range(len(self.option)):
            self.option[i] = "DummyText"
            self.option_buttons[i].setText(self.option[i])
        self.showOptionPage()

def runGUI():
    app = QApplication(sys.argv)
    ex = RecommendationApp()
    ex.show()
    sys.exit(app.exec_())