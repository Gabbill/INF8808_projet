'''
    Contains the server to run our application.
'''


def create_app():
    '''
        Gets the underlying Flask server from our Dash app.

        Returns:
            The server to be run
    '''
    # the import is intentionally inside to work with the server failsafe
    from app import app  # pylint: disable=import-outside-toplevel
    return app.server


if __name__ == "__main__":
    create_app().run(port="8050", debug=True, host="0.0.0.0")
