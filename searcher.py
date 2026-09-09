import questionary
from youtube_search import YoutubeSearch

import nice_errors


class Searcher:
    """Searches YouTube for relevant results.

    This function searches YouTube using YoutubeSearch.
    """

    @staticmethod
    def search_and_ask(search_term) -> None:
        """Search YouTube for a search term.

        Args:
            search_term: Search term.

        Returns:
            link: YouTube URL.
            choice: YouTube video name.
        """
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
