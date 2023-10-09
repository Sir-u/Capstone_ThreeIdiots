#include "RecommendationApp.h"
#include <QtWidgets/QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    RecommendationApp w;
    w.show();
    return a.exec();
}
