// thread example
#include <iostream>       // std::cout
#include <thread>         // std::thread
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sstream>
#include <mutex>

class Database;

class Manager;

class Server {
    private:
        int id;
        void server_function();
        void initThread();
        Manager* manager;

    public:
        std::thread* thread;
        Database *database;
        Server();
        int getID();
        void join();
        void diagnostic();
        void initialise(int id, Manager* manager);
};