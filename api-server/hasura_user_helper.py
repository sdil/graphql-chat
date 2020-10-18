import os

from gql import AIOHTTPTransport, Client, gql

transport = AIOHTTPTransport(
    os.environ.get("GRAPHQL_SERVER"),
    headers={
        "X-Hasura-Admin-Secret": f'{os.environ.get("HASURA_GRAPHQL_ADMIN_SECRET")}'
    },
)

client = Client(transport=transport, fetch_schema_from_transport=True)


def get_user(uuid: str):
    """
    Get the user info from Hasura
    """
    query = gql(
        """
        query GetUser ($uid: String!) {
            user(where: {id: {_eq: $uid}}) {
                id
                name
            }
        }
    """
    )

    params = {"uid": uuid}
    result = client.execute(query, variable_values=params)["user"]
    
    if len(result) == 0:
        # If no user match, return False so that it creates new user
        return False
    
    return result[0]


def create_user(user):
    """
    Creates new user in Hasura
    """

    query = gql(
        """
        mutation InsertNewUser($id: String!, $name: String!) {
            insert_user_one(object: {id: $id, name: $name}) {
                id
                name
            }
        }
    """
    )

    params = {"id": user["localId"], "name": user["displayName"]}
    return client.execute(query, variable_values=params)
