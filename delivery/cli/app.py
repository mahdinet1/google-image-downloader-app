import os


class CliApp:
    def get_query(self):
        print("-- if you want to exit just type 0 and exit the app!")
        query = input("Please enter your query: ")
        if query == "0":
            exit(0)
        print("Crawling images from google images ... ")
        return query
