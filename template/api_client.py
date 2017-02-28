import requests

class Api:

    def __init__(self):
        self.url = 'http://127.0.0.1:8000/movies/api/v1.0/{0}'

    def all_movies(self):
        """
        Retrieves all the movies in the API.
        :return:
        :rtype:
        """
        return requests.get(self.url.format('get_movies'))

    def find_movie(self, title):
        """
        Retrieves a movie from the API based on the title field.
        :param title:
        :type title:
        :return:
        :rtype:
        """

        return requests.post(self.url.format('get_movie'), json={'title': title})

if __name__ == '__main__':
    api = Api()

    print(api.find_movie('Avatar').text)
