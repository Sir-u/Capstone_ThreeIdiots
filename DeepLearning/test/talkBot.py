import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt
import random
import chatbot_test

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
        image_file_path = '../Capstone_ThreeIdiots/Asset/TalkHelper_Logo.png'  # 이미지 파일 경로 및 이름 설정
        self.recommend_page = QWidget()
        # 추천 버튼 생성
        self.recommend_button = QPushButton("추천해줘")

        # 버튼 스타일 설정
        self.recommend_button.setStyleSheet(
            """
            background-color: #77ddff;
            color: #800080;
            padding: 10px;
            border: none;
            border-radius: 5px;
            """
        )

        # 이미지 레이블 생성 및 이미지 설정
        image_label = QLabel()
        pixmap = QPixmap(image_file_path)
        scaled_pixmap = pixmap.scaled(300, 300)  # 이미지 크기 조절
        image_label.setPixmap(scaled_pixmap)

        # 수직 레이아웃 생성
        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(image_label, alignment=Qt.AlignCenter)  # 이미지 레이블 추가 (상단 정렬)
        vbox_layout.addWidget(self.recommend_button)  # 버튼 추가
        self.recommend_button.clicked.connect(self.updateOptionPage)  # 버튼 클릭 시 옵션 선택 페이지로 이동
        # 추천 페이지 레이아웃 설정
        recommend_layout = QVBoxLayout()
        recommend_layout.addLayout(vbox_layout)  # 수직 레이아웃을 추천 페이지 레이아웃에 추가
        self.recommend_page.setLayout(recommend_layout)

       # 옵션 선택 페이지
        self.option_page = QWidget()
        self.option_label = QLabel("텍스트를 선택하세요:")
        self.option_buttons = [QPushButton(self.option[0]), QPushButton(self.option[1]), QPushButton(self.option[2])]

        option_layout = QVBoxLayout()  # option_layout 먼저 정의
        image_file_path = '../Capstone_ThreeIdiots/Asset/TalkHelper_Icon.png'  # 이미지 파일 경로 및 이름 설정

        for i, button in enumerate(self.option_buttons):
            button.setStyleSheet(
                """
                background-color: #77ddff;
                color: #800080;
                padding: 10px;
                border: none;
                border-radius: 5px;
                """
            )
            
            # 이미지 레이블 생성 및 이미지 설정
            image_label = QLabel()
            pixmap = QPixmap(image_file_path)
            scaled_pixmap = pixmap.scaled(50, 50)  # 이미지 크기 조절
            image_label.setPixmap(scaled_pixmap)
            
            # 이미지 레이블과 버튼을 포함하는 수평 레이아웃 생성
            hbox_layout = QHBoxLayout()
            hbox_layout.addWidget(image_label)  # 이미지 레이블 추가
            hbox_layout.addWidget(button)  # 버튼 추가
            hbox_layout.addStretch()  # 이미지와 버튼을 왼쪽과 오른쪽으로 분리하기 위한 Stretch 추가

            option_layout.addLayout(hbox_layout)  # 수평 레이아웃을 수직 레이아웃에 추가
            button.clicked.connect(self.showResultPage)

        self.recommend_again_button = QPushButton("재추천")
        self.recommend_again_button.setStyleSheet(
            """
            background-color: #98ff98;
            color: #556b2f;
            padding: 10px;
            border: none;
            border-radius: 5px;
            """
        )

        self.recommend_again_button.clicked.connect(self.updateOptionPage)  # 재추천 버튼 클릭 시 재추천 기능 실행
        option_layout.addWidget(self.recommend_again_button)

        self.option_page.setLayout(option_layout)  # option_layout을 옵션 선택 페이지 레이아웃으로 설정


        # 결과 페이지
        self.result_page = QWidget()
        self.text_label = QLabel("")
        self.back_button = QPushButton("돌아가기")
        self.back_button.setStyleSheet(
            """
            background-color: #FFB6C1;
            color: #FF007F;
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

        # 도움말 페이지
        self.help_page = QWidget()
        self.help_label = QLabel("자유롭게 대화를 하다가 무슨 말을 해야할 지 고민될 때\n\n추천해줘 버튼을 눌러 추천 문장을 선택하세요.\n\n대화 내역을 통해 적절한 문장을 분석해서 추천해드립니다.")
        self.help_back_button = QPushButton("뒤로 가기")
        self.help_back_button.setStyleSheet(
            """
            background-color: #FFB6C1;
            color: #FF007F;
            padding: 10px;
            border: none;
            border-radius: 5px;
            """
        )

        self.help_button = QPushButton("도움말")
        self.help_button.setStyleSheet(
            """
            background-color: #98ff98;
            color: #556b2f;
            padding: 10px;
            border: none;
            border-radius: 5px;
            """
        )
        self.help_button.clicked.connect(self.showHelpPage)  # 도움말 버튼을 눌렀을 때 도움말 페이지로 이동
        recommend_layout.addWidget(self.help_button)  # 추천 페이지 레이아웃에 도움말 버튼 추가

        self.help_back_button.clicked.connect(self.showRecommendations)
        help_layout = QVBoxLayout()
        help_layout.addWidget(self.help_label)
        help_layout.addWidget(self.help_back_button)
        self.help_page.setLayout(help_layout)

        # 페이지를 stacked widget에 추가
        self.stacked_widget.addWidget(self.recommend_page)
        self.stacked_widget.addWidget(self.option_page)
        self.stacked_widget.addWidget(self.result_page)
        self.stacked_widget.addWidget(self.help_page)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        self.setWindowTitle("Tellper")
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

    def updateOptionPage(self):
        for i in range(len(self.option)):
            self.option[i] = chatbot_test.GenerateAnswer(messageDict[-1])
        self.showOptionPage()

    def showHelpPage(self):
        # 도움말 페이지로 전환
        self.stacked_widget.setCurrentIndex(3)
        self.prevPageIndex = self.stacked_widget.currentIndex()  # 이전 페이지 인덱스 업데이트

def runGUI():
    app = QApplication(sys.argv)
    ex = RecommendationApp()
    ex.show()
    sys.exit(app.exec_())