import sqlite3

class vehManagement:
      def __init__(self):
          try:
               self.con = sqlite3.connect('monitoring_system')
          except sqlite3.Error as error:
              print("Sqlite database connection failure.")
      def addEntry(self,veh_number,arrivalTime,status):
        #try:
          c = self.con.cursor()
          c.execute("INSERT INTO vehicle_logging('veh_number','veh_login_time','status') VALUES('"+veh_number+"','"+arrivalTime+"','"+status+"')")
          self.con.commit()
          return c.rowcount
        #except sqlite3.Error as error:
          print("Failed to insert data into sqlite table", error)
        #finally:
          self.con.close()

      def select_all_tasks(self,tableName):

          cur = self.con.cursor()
          cur.execute("SELECT * FROM "+tableName)

          rows = cur.fetchall()

          for row in rows:
              print(row)