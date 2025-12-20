from network.server import MyServer


if __name__ == "__main__":
    """The main entry point for the server application."""
    print("This is the main server file.")
    print("Starting server...")
    server = MyServer("0.0.0.0", 9000)
    server.start()
