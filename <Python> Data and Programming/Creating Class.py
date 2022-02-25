# Question 1: Begin with the class below, and do the following:
#   a) Modify the what_to_watch method so that it takes an optional keyword argument that allows the user to
#       narrow down the random selection by category (e.g. select only from movies with category 'action'), but
#       defaults to the entire list of titles as it does now.
#   b) The what_to_watch method currently raises a ValueError if you use it before entering any movies. Modify
#       it using try/except so that it tells the user what they did wrong instead of raising an error.
#   c) Create a new class called InteractiveMovieDataBase that inherits MovieDataBase
#   d) Override the add_movie method in your new class so that it takes in user input to add a title, instead
#       of arguments
#   e) Add some appropriate error checking on the user input, so that they can't enter something that makes no
#       sense (e.g. title=None or year='dog')
#   f) Add a new method to InteractiveMovieDataBase named movie_rankings, which returns a list of all the titles
#       in the database currently, ordered highest ranking to lowest

from numpy import random

class MovieDataBase():
    def __init__(self):
        self.titles = []
        self.movies = {}

    def add_movie(self, title, year, category, rating):
        self.titles.append(title)
        self.movies[title] = {'year':year, 'category':category, 'rating':rating}
        print(f'{title} ({year}) added to the database.')

    def what_to_watch(self, category = None):
        try:  
            if category is not None:
                choice = random.choice(self.titles)
                movie = self.movies[choice]
                print(f"Your movie today is {choice} ({movie['year']}), which is a {movie['category']} with a rating of: {movie['rating']}")
            else:
                while True:
                    choice = random.choice(self.titles)
                    if self.movies[choice]['category'] == category:
                        movie = self.movies[choice]
                        print(f"Your movie today is {choice} ({movie['year']}), which is a {movie['category']} with a rating of: {movie['rating']}")
                        break
        except ValueError: 
            print("Movie list is empty.")


class InteractiveMovieDataBase(MovieDataBase):
    def __init__(self):
        self.title = []
        self.movies = {}
        self.category_list = []
        self.ranking = {}

    def add_movie(self):
        self.title = input("What is the title :")
        self.year = int(input("What is the year :"))
        self.category = input("What is the category :")
        self.rating = float(input("What is the rating :"))
        if type(self.title) is not str:
            print("Please input a valid string")
        elif type(self.year) is not int:
            print("Please input a valid int")
        elif type(self.category) is not str:
            print("Please input a valid string")
        elif type(self.rating) is not float:
            print("Please input a valid rating with decimal")
        else:
            self.movies[self.title] = {'year':self.year, 'category':self.category, 'rating':self.rating}
            print(f'{self.title} ({self.year}) added to the database.')
            self.category_list.append(self.movies[self.title]['category'])
            
    def movie_rankings(self):
        for i in self.movies:
            self.ranking.update({i:self.movies[i]['rating']})
        sorted_ranking = sorted(self.ranking, key=self.ranking.get, reverse=True)
        return sorted_ranking


# movienight = MovieDataBase()
# movienight.add_movie("Fast & Furious","2001","action",90)
# movienight.add_movie("Frozen","2013","family",98)
# movienight.add_movie("Harry Potter","2001","fantasy",90)
# movienight.add_movie("About Time","2013","romance",95)
# movienight.add_movie("Knock Down the House","2019","documentary",91)
# movienight.what_to_watch()


movielist = InteractiveMovieDataBase()
movielist.add_movie()
movielist.add_movie()
movielist.add_movie()


print(movielist.movie_rankings())



