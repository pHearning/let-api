from API.app import app

if __name__ == "__main__":
    """
    A simpler way to start the API app.
    """
    app.run(debug=True, port=8000)
