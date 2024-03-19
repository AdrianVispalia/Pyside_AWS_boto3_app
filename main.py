import sys
from PySide2.QtWidgets import QApplication
from View.main_window import MainWindow
from View.general.error_window import ErrorWindow
from Controller.utils import check_aws_configuration
from Controller.utils import get_session


if __name__ == '__main__':
    app = QApplication(sys.argv)

    try:
        check_aws_configuration()
        session = get_session()
        main_window = MainWindow(session)
        main_window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print("Error: " + str(e))
        error_window = ErrorWindow(str(e))
        error_window.show()
        sys.exit(error_window.exec_())

