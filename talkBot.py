import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QMessageBox

class RecommendationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 모던한 디자인을 위해 스타일 시트를 사용
        self.setStyleSheet("font-size: 18px; background-color: #f0f0f0;")

        # 추천 버튼 생성
        self.recommend_button = QPushButton("추천해줘")
        self.recommend_button.setStyleSheet("background-color: #3498db; color: white; padding: 10px; border: none;")
        self.recommend_button.clicked.connect(self.showRecommendations)

        # 텍스트 표시 레이블
        self.text_label = QLabel("")

        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.recommend_button)
        layout.addWidget(self.text_label)
        self.setLayout(layout)

        # 창 설정
        self.setWindowTitle("추천 앱")
        self.setGeometry(100, 100, 400, 200)

    def showRecommendations(self):
        # 추천 버튼을 클릭했을 때 텍스트 3가지를 표시하고 선택할 수 있는 대화상자 표시
        options = ["옵션 1", "옵션 2", "옵션 3"]
        choice, _ = QMessageBox.getItemChooice(self, "추천 선택", "텍스트를 선택하세요:", options=options)
        
        if choice:
            self.text_label.setText(f"선택한 텍스트: {choice}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RecommendationApp()
    ex.show()
    sys.exit(app.exec_())
