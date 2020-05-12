from movies import Movies
from genres import Genres
from dateutil import parser
from datetime import datetime, date
import requests
import random

class Api:

    def __init__(self):
        self.currMovies = 702625
        self.g = Genres()
        self.m = Movies()
        self.imgURI = 'https://image.tmdb.org/t/p/w220_and_h330_face'
        self._apiKey = 'cab215b672637a6d24409a56bcd457c2'
        self._baseUri = 'https://api.themoviedb.org/'
        pass

    def getGenres(self):
        endpoint = '3/genre/movie/list'
        genres = requests.get(url=self._baseUri+endpoint, params=dict(api_key=self._apiKey,))
        d = genres.json()
        [self._saveGenres(g) for g in d['genres']]
    
    def _saveGenres(self, genre):
        if not self.g.exists(genre['id']):
            self.g.saveGenre(genreId=genre['id'], genreName=genre['name'])


    def _getGenreWithID(self, id):
        return self.g.getGenreName(id)

    def getMovies(self):
        result = self.makeRequest()
        l = 'popularity.asc, popularity.desc, release_date.asc, release_date.desc, revenue.asc, revenue.desc, primary_release_date.asc, primary_release_date.desc, original_title.asc, original_title.desc, vote_average.asc, vote_average.desc, vote_count.asc, vote_count.desc'
        totalPages = result['total_pages']
        print(f'going to download info for {result["total_results"]} movies :)))\n\n')
        [self._saveMovies(m) for m in result['results']]
        for page in range(totalPages):  
            print(f'current page: {page} \n\n')
            for c in l.split(', '):
                result = self.makeRequest(endpoint= '3/discover/movie', page=page+1, c=c)
                [self._saveMovies(m) for m in result['results']]
        result = self.makeRequest(endpoint= '3/discover/tv')
        totalPages = result['total_pages']
        for page in range(totalPages):  
            print(f'current page: {page} \n\n')
            for c in l.split(', '):
                result = self.makeRequest(endpoint= '3/discover/tv',page=page+1, c=c)
                [self._saveMovies(m) for m in result['results']]
        
        

    def findMovie(self, search='', popularity=-1, genres='', adult=False, limit=10):
        print(search, adult, genres, popularity, limit)
        popularity = int(popularity)
        array = self.m.getList(search=search, popularity=popularity, genres=genres, isAdult=adult,)
        final = []
        if len(array) > limit:
            while len(final) < limit:
                final.append(array.pop(random.randint(0, len(array))))
        else:
            final = array
        return final



    def makeRequest(self, endpoint= '3/discover/movie', page=1, c='popularity.desc'):
        genres = requests.get(
            url=self._baseUri+endpoint, 
            params=dict(
                api_key=self._apiKey,
                include_adult=True,
                sort_by=c,
                page=page
                ))
        return genres.json()
    
    def getSavedMovies(self):
        [print(l, '\n') for l in self.m.getAllMovies() ]
        return self.m.getAllMovies()
    
    def _saveMovies(self, movie): 
        try:  
            popularity = movie['popularity']
            if movie['poster_path']:
                posterPath = self.imgURI + movie['poster_path']
            else: 
                posterPath = 'https://scontent.ftia4-1.fna.fbcdn.net/v/t1.0-9/31358061_1486482608130033_6889977130264821760_o.jpg?_nc_cat=108&_nc_sid=09cbfe&_nc_ohc=LTfoIC-71R0AX8GBsPb&_nc_ht=scontent.ftia4-1.fna&oh=38837f4d06399f89709401838678f389&oe=5EDD08ED'
            movieId = movie['id']
            isAdult = movie['adult']
            language = movie['original_language']
            genres = []
            [genres.append(self._getGenreWithID(id)) for id in movie['genre_ids']]
            title = movie['title']
            description = movie['overview']
            bday = movie['release_date']
            votes = movie['vote_count']
            bday = parser.parse(bday)
            averageVote = movie['vote_average']
            if not self.m.exists(movieId):
                self.m.saveMovie(
                    movieId=movieId,
                    movieTitle=title,
                    description=description,
                    popularity=popularity,
                    posterPath=posterPath,
                    isAdult=isAdult,
                    language=language,
                    genre=''.join(str(e+' ') for e in genres),
                    bday=bday,
                    votes=votes,
                    averageVote=averageVote
                )
                print(f'\tsaved movie with id: {movieId} \t title: {title}')
                return f'\tsaved movie with id: {movieId} \t title: {title}'
            else: 
                print(f'\talready saved movie with id: {movieId} \t title: {title}')
                return f'\talready saved movie with id: {movieId} \t title: {title}'
        except Exception:
            print('smth went wrong but we good')
            return False

if __name__ == '__main__':
	a = Api()
	a.getMovies()

        
