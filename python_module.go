package main

import (
    "os"
	"log"
	"net"
	"net/rpc"
	"net/rpc/jsonrpc"
)

// Define Functions here.
type Echo int

func (h *Echo) Echo(arg *string, reply *string) error {
	log.Println("received: ", *arg)
	*reply = *arg
	return nil
}

func main() {
	// Register Functions on the RPC here.
	hello := new(Echo)
	rpc.Register(hello)

	listener, errors := net.Listen("unix", os.Args[1])
	defer listener.Close()

	if errors != nil {
		log.Fatal(errors)
	}

	log.Print("Listening for RPC-JSON connections: ", listener.Addr())

	for {
		log.Print("Waiting for RPC-JSON connections...")
		conection, errors := listener.Accept()

		if errors != nil {
			log.Printf("Accept error: %s", conection)
			continue
		}

		log.Printf("Connection started: %v", conection.RemoteAddr())
		go jsonrpc.ServeConn(conection)
	}
}
