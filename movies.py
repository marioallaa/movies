
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy import Table, Column, Integer, String, MetaData, Date, Boolean, ARRAY, Text

class Movies:

    def __init__(self):
        self.databasePath = 'sqlite:///data/movies.db'
        self.databaseEcho = False
        self.meta = MetaData()
        self.engine = create_engine(self.databasePath, 
            echo=self.databaseEcho, 
            connect_args={"check_same_thread": False})
        self.con = self.engine.connect()
        self.movie = self._movieTable()
        self.meta.create_all(self.engine)
    

    def _movieTable(self):
        return Table(
            'movies', self.meta,
            Column('id', Integer, primary_key=True),
            Column('title', String),
            Column('popularity', Integer),
            Column('imgPath', String),
            Column('isAdult', Boolean),
            Column('language', String),
            Column('genres', String),
            Column('description', Text),
            Column('bday', Date),
            Column('votes', Integer),
            Column('averageVote', Integer),
        )

    def saveMovie(
        self, 
        movieId, 
        movieTitle,
        description,
        popularity,
        posterPath,
        isAdult, 
        language,
        genre,
        bday,
        votes,
        averageVote):
        ins = self.movie.insert().values(
            id = movieId, 
            title = movieTitle,
            popularity = popularity,
            imgPath = posterPath,
            isAdult = isAdult,
            language = language,
            genres = genre,
            description = description,
            bday = bday,
            votes = votes,
            averageVote = averageVote,
            )
        return self.con.execute(ins)

    def exists(self, movieID):
        con = self.engine.connect()
        s = self.movie.select().where(self.movie.c.id == movieID)
        res = self.con.execute(s)
        con.close()
        for r in res:
            if r:
                return True
        return False

    def getMovieById(self, movieID):
        s = self.movie.select().where(self.movie.c.id == movieID)
        res = self.con.execute(s)
        f = []
        for r in res:
            f.append(r)
        return f

    def getMovieId(self, number):
        s = self.ids.select().where(self.ids.c.id == number)
        res = self.con.execute(s)
        for r in res:
            return r['movieId']
            

    def getAllMovies(self):
        s = self.movie.select()
        res = m.con.execute(text("select * from movies;"))
        f = []
        i=0
        for r in res.fetchall():
            i+=1
            f.append([i, r['id'], r['popularity'], r['genres']])
        return f

    def getList(self, search='', popularity=-1, genres='', isAdult=False): 
        query = f' where popularity>{popularity}'
        if genres != '':
            for g in genres.split(' '):
                query = query + " and genres like '%{}%'".format(g)
        if isAdult:
            query = query + f' and isAdult=True '
        if search!='':
            for s in search.split(' '):
                query = query + " and (description like '%{}%' or title like '%{}%')".format(s, s)

        res = self.con.execute(text(f"select * from movies {query};"))
        f = []
        for r in res.fetchall():
            f.append(dict(r))
        return f

if __name__ == "__main__":
    m = Movies()
    [print(e) for e in  m.getList()]
   
