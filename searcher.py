import questionary
from youtube_search import YoutubeSearch

import nice_errors


class Searcher:
    def __init__(self):
        pass

    @staticmethod
    def search_and_ask(search_term):
        results = YoutubeSearch(search_term, max_results=10).to_dict()
        titles = []
        for result in results:
            titles.append(result["title"])
        choice = questionary.select(
            "Loaded the 10 most relevant results. Please pick the result you want to play.",
            choices=titles,
        ).ask()

        for result in results:
            if result["title"] == choice:
                link = f"https://www.youtube.com{result['url_suffix']}"
                return link, choice
        print("Please do not exit the questionary.select(). An error will be raised.")
        nice_errors.print_error("ferror", "questionary.select() exited by user.")
