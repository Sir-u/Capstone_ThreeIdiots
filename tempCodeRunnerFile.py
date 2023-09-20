
        # 텍스트 표시 레이블
        self.text_label = QLabel("")

        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.recommend_button)
        layout.addWidget(self.text_label)
        self.setLayout(layout)
