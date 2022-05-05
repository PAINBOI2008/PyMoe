import ujson
import requests
from pymoe.errors import serializationFailed, serverError
from pymoe.helpers import anilistWrapper

settings = {
    'header': {
        'Content-Type': 'application/json',
        'User-Agent': 'Pymoe (github.com/ccubed/PyMoe)',
        'Accept': 'application/json'
    },
    'apiurl': 'https://graphql.anilist.co'
}

def manga(term: str, page: int = 1, perPage: int = 3):
    """
        Search for a manga by term.
        Results are paginated by default. Page specifies which page we're on.
        Perpage specifies how many per page to request. 3 is just the example from the API docs.

        TODO: WRITE THIS
    """
    query_string = """\
        query( $query: String, $page: Int, $perPage: Int ){
            Page ( page: $page, perPage: $perPage ) {
                pageInfo {
                    currentPage
                    hasNextPage
                }
                media ( search: $query, type: MANGA ){
                    id
                    idMal
                    title {
                        romaji
                        english
                    }
                    coverImage {
                        extralarge
                        large
                        medium
                        color
                    }
                    status
                    description
                    startDate {
                        year
                        month
                        day
                    }
                    endDate {
                        year
                        month
                        day
                    }
                    averageScore
                    popularity
                    chapters
                    volumes
                    genres
                    hashtag
                    isAdult
                    averageScore
                    synonyms
                    siteUrl
                }
            }
        }    
    """

    json_params = {
        'query': query_string,
        'variables': {
            'query': term,
            'page': page,
            'perPage': perPage
        }
    }

    r = requests.post(
        settings['apiurl'],
        headers = settings['header'],
        json = json_params
    )

    try:
        jsd = ujson.loads(r.text)
    except ValueError:
        raise serializationFailed(r.text, r.status_code)
    else:
        if 'errors' in jsd:
            raise serverError(r.text, r.status_code)
        else:
            if jsd['data']['Page']['pageInfo']['hasNextPage']:
                return anilistWrapper(
                    jsd['data']['Page']['media'],
                    json_params,
                    settings['header'],
                    settings['apiurl']
                )
            else:
                return jsd['data']['Page']['media']