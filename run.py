"""Start the website:  python run.py   ->  http://127.0.0.1:5000"""
from webapp.app import create_app

if __name__ == "__main__":
    print("\n  Alphabet AI Studio is running ->  http://127.0.0.1:5000\n")
    create_app().run(host="127.0.0.1", port=5000, debug=False)
