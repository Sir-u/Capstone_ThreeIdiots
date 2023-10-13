﻿#pragma once

#include <QtWidgets/QMainWindow>
#include "ui_RecommendationApp.h"
#include <QApplication>
#include <QWidget>
#include <QPushButton>
#include <QStackedWidget>
#include <QLabel>
#include <QVBoxLayout>
#include <QStringList>
#include <QRandomGenerator>

class RecommendationApp : public QWidget
{
    Q_OBJECT

public:
    RecommendationApp(QWidget* parent = nullptr)
        : QWidget(parent), prevPageIndex(0)
    {
        initUI();
    }

private:
    void initUI()
    {
        // 전체 앱 스타일 설정
        setStyleSheet(
            "font-size: 18px;"
            "color: black;"
            "background-color: #f0f0f0;");

        stackedWidget = new QStackedWidget(this);

        // 추천 페이지
        recommendPage = new QWidget();
        recommendButton = new QPushButton("추천해줘", this);
        recommendButton->setStyleSheet(
            "background-color: #3498db;"
            "color: white;"
            "padding: 10px;"
            "border: none;"
            "border-radius: 5px;");
        connect(recommendButton, &QPushButton::clicked, this, &RecommendationApp::showOptionPage);
        QVBoxLayout* recommendLayout = new QVBoxLayout(recommendPage);
        recommendLayout->addWidget(recommendButton, 0, Qt::AlignCenter); // 중앙 정렬

        // 옵션 선택 페이지
        optionPage = new QWidget();
        optionLabel = new QLabel("텍스트를 선택하세요:", this);
        QHBoxLayout* optionButtonLayout = new QHBoxLayout();
        for (auto button : optionButtons)
        {
            button->setStyleSheet(
                "background-color: #3498db;"
                "color: white;"
                "padding: 10px;"
                "border: none;"
                "border-radius: 5px;");
            connect(button, &QPushButton::clicked, this, &RecommendationApp::showResultPage);
            optionButtonLayout->addWidget(button);
        }
        recommendAgainButton = new QPushButton("재추천", this);
        recommendAgainButton->setStyleSheet(
            "background-color: #2ecc71;"
            "color: white;"
            "padding: 10px;"
            "border: none;"
            "border-radius: 5px;");
        connect(recommendAgainButton, &QPushButton::clicked, this, &RecommendationApp::recommendAgain);
        QVBoxLayout* optionLayout = new QVBoxLayout(optionPage);
        optionLayout->addWidget(optionLabel, 0, Qt::AlignCenter); // 중앙 정렬
        optionLayout->addLayout(optionButtonLayout);
        optionLayout->addWidget(recommendAgainButton, 0, Qt::AlignCenter); // 중앙 정렬

        // 결과 페이지
        resultPage = new QWidget();
        textLabel = new QLabel("", this);
        backButton = new QPushButton("돌아가기", this);
        backButton->setStyleSheet(
            "background-color: #e74c3c;"
            "color: white;"
            "padding: 10px;"
            "border: none;"
            "border-radius: 5px;");
        connect(backButton, &QPushButton::clicked, this, &RecommendationApp::showRecommendations);
        QVBoxLayout* resultLayout = new QVBoxLayout(resultPage);
        resultLayout->addWidget(textLabel, 0, Qt::AlignCenter); // 중앙 정렬
        resultLayout->addWidget(backButton, 0, Qt::AlignCenter); // 중앙 정렬

        // 페이지를 stacked widget에 추가
        stackedWidget->addWidget(recommendPage);
        stackedWidget->addWidget(optionPage);
        stackedWidget->addWidget(resultPage);

        QVBoxLayout* layout = new QVBoxLayout(this);
        layout->addWidget(stackedWidget);

        setWindowTitle("추천 앱");
        setGeometry(100, 100, 400, 200);
    }

private slots:
    void showOptionPage()
    {
        // 옵션 선택 페이지로 전환
        stackedWidget->setCurrentIndex(1);
        prevPageIndex = 0; // 현재 페이지가 옵션 선택 페이지이므로 이전 페이지는 추천 페이지(인덱스 0)
    }

    void showResultPage()
    {
        // 결과 페이지로 전환 또는 돌아가기 버튼을 누를 때 옵션 선택 페이지로 전환
        auto* senderButton = qobject_cast<QPushButton*>(sender());
        if (senderButton == backButton)
        {
            stackedWidget->setCurrentIndex(0); // 돌아가기 버튼 클릭 시 첫 번째 페이지로
        }
        else
        {
            QString selectedOption = senderButton->text();
            textLabel->setText("선택한 텍스트: " + selectedOption);
            stackedWidget->setCurrentIndex(2);
        }
    }

    void showRecommendations()
    {
        // 추천 페이지로 전환
        stackedWidget->setCurrentIndex(0);
    }

    void recommendAgain()
    {
        // 재추천을 위한 기능
        QStringList options = { "옵션 1", "옵션 2", "옵션 3" };
        unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
        std::default_random_engine rng(seed);

        // options 벡터를 무작위로 섞음
        std::shuffle(options.begin(), options.end(), rng);
        for (int i = 0; i < options.size(); ++i)
        {
            optionButtons[i]->setText(options[i]);
        }
        stackedWidget->setCurrentIndex(1); // 옵션 선택 페이지로 이동
    }

private:
    QStackedWidget* stackedWidget;
    QWidget* recommendPage;
    QPushButton* recommendButton;
    QWidget* optionPage;
    QLabel* optionLabel;
    QList<QPushButton*> optionButtons{ new QPushButton("옵션 1", this), new QPushButton("옵션 2", this), new QPushButton("옵션 3", this) };
    QPushButton* recommendAgainButton;
    QWidget* resultPage;
    QLabel* textLabel;
    QPushButton* backButton;
    int prevPageIndex;
};