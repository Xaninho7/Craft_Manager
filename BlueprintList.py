class Blueprint:
    def __init__(self, id, name, costClick, mu):
        self.id = id
        self.name = name
        self.costClick = costClick
        self.mu = mu


class ListBP:
    def __init__(self, conn):
        self.conn = conn
        self.bplist = []
        self.getBPfromDB()

    def getBPfromDB(self):
        sql = f'SELECT * FROM Blueprint ORDER BY Name ASC;'
        cur = self.conn.cursor()
        cur.execute(sql)
        results = cur.fetchall()
        for bp in results:
            self.bplist.append(Blueprint(bp[0], bp[1], bp[2], bp[3]))

    def refresh(self):
        self.bplist.clear()
        self.getBPfromDB()
