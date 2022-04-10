import requests


def get_quote():
    """ Get a random quote from the quotable.io api:
    https://github.com/lukePeavey/quotable
    """

    r = requests.get("https://api.quotable.io/random")
    
    content = r.json()
    
    return content['content']
