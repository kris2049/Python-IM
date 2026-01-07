from client.client import MyClient

if __name__ == "__main__":
    client_num = 5
    clients = []
    for i in range(client_num):
        c = MyClient("127.0.0.1",9000,f"client_{i}")
        clients.append(c)
    
    for c in clients:

        c.start()
       