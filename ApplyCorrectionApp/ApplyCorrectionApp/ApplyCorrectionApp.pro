TEMPLATE = app
CONFIG += console c++11
CONFIG -= app_bundle
CONFIG -= qt

CONFIG += link_pkgconfig
PKGCONFIG += opencv4
PKGCONFIG += nlohmann_json





SOURCES += \
        OrthoRectify.cpp \
        main.cpp

HEADERS += \
    InputParser.h \
    OrthoRectify.h
