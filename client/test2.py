from network.client import MyClient

if __name__ == "__main__":
    client = MyClient("127.0.0.1",9000,"test_client")
    client.start()
