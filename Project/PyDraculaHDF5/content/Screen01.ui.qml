import QtQuick
import QtQuick.Controls
import PyDraculaHDF5

Rectangle {
    width: Constants.width
    height: Constants.height

    color: Constants.backgroundColor

    Text {
        text: qsTr("Hello PyDraculaHDF5")
        anchors.centerIn: parent
        font.family: Constants.font.family
    }
}
