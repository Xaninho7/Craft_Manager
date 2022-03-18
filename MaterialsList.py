class Material:
    def __init__(self, id, name, value, mu):
        self.id = id
        self.name = name
        self.value = value
        self.mu = mu


class ListMaterial:
    def __init__(self, conn):
        self.conn = conn
        self.itemsList = []
        self.getMaterialFromDB()

    def getMaterialFromDB(self):
        sql = f'SELECT * FROM Material ORDER BY Name ASC;'
        cur = self.conn.cursor()
        cur.execute(sql)
        results = cur.fetchall()
        for mat in results:
            self.itemsList.append(Material(mat[0], mat[1], mat[2], mat[3]))

    def refresh(self):
        self.itemsList.clear()
        self.getMaterialFromDB()
