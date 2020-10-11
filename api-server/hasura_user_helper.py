from sgqlc.endpoint.http import HTTPEndpoint

url = 'http://server.com/graphql'
headers = {'Authorization': 'bearer TOKEN'}

variables = {'varName': 'value'}

endpoint = HTTPEndpoint(url, headers, timeout=1)

def get_user(uuid) -> bool:
    """
    Get the user info from Hasura
    """
    query = """
    query user (uuid = $uuid) {
        uuid
    }
    """
    if endpoint(query, variables):
        return True

    return False


def create_user(user) -> bool:
    """
    Creates new user in Hasura
    """

    query = """
    mutate user (uuid = $uuid) {
        uuid
    }
    """
    if endpoint(query, variables):
        return True

    return False
