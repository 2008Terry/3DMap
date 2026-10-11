from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication, QMessageBox

from campus_data import load_buildings


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    app = QApplication(sys.argv)
    app.setApplicationName("Michigan Campus Map")

    try:
        buildings, extent = load_buildings(repo_root)
    except (OSError, ValueError, KeyError, TypeError) as error:
        QMessageBox.critical(None, "Campus data could not be loaded", str(error))
        return 1

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("campusBuildings", [building.to_qml() for building in buildings])
    engine.rootContext().setContextProperty("campusExtent", {
        "centerX": extent.center_x,
        "centerZ": extent.center_z,
        "width": extent.width,
        "depth": extent.depth,
    })
    qml_path = Path(__file__).with_name("Main.qml")
    engine.load(QUrl.fromLocalFile(str(qml_path)))
    if not engine.rootObjects():
        QMessageBox.critical(None, "Campus map could not start", f"Could not load {qml_path}")
        return 1
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
