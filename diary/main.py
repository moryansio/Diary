from database import connect_db
from gui import DiaryGUI

if __name__ == "__main__":
    conn = connect_db()
    app = DiaryGUI(conn)
    app.mainloop()






