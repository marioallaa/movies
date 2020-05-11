
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData


class Genres:

    def __init__(self, ):
        self.databasePath = 'sqlite:///data/movies.db'
        self.databaseEcho = False
        self.meta = MetaData()
        self.engine = create_engine(self.databasePath, 
            echo=self.databaseEcho, 
            connect_args={"check_same_thread": False})
        self.con = self.engine.connect()
        self.genre = self._genreTable()
        self.meta.create_all(self.engine)

    def _genreTable(self):
        return Table(
            'genres', self.meta,
            Column('id', Integer, primary_key=True),
            Column('name', String),
        )

    def saveGenre(self, genreId, genreName):
        ins = self.genre.insert().values(id=genreId, name=genreName,)
        return self.con.execute(ins)

    def exists(self, genreID):
        con = self.engine.connect()
        s = self.genre.select().where(self.genre.c.id == genreID)
        res = self.con.execute(s)
        con.close()
        for r in res:
            if r:
                return True
        return False

    def getGenreName(self, genreID):
        s = self.genre.select().where(self.genre.c.id == genreID)
        res = self.con.execute(s)
        for r in res:
            return r['name']
    
    def getAllGenres(self):
        s = self.genre.select()
        res = self.con.execute(s)
        f = []
        for r in res:
            f.append(r)
        return f


if __name__ == "__main__":
    m = Genres()
    [print(e,"\n\n") for e in m.getAllGenres()]
