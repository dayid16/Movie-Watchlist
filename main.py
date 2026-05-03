from logic import *

def main() -> None:
    '''
    Initialize the app.
    Creates a main window.
    Begins the main loopx
    '''
    app = QApplication(sys.argv)
    window = Logic()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()