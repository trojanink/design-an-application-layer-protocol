# design-an-application-layer-protocol
Ιmplement a server application that will simultaneously manage multiple clients and facilitate the exchange of files between them. You will also need to implement a client application that will connect to the server and be able to perform some functions:

1. Download the list of available files and from which clients.
2. Upload a list of files offered by the client so that they can be advertised through the server to other clients.
3. Request a specific file from a client.


In the last stage where a client requests a file from another client, the server only participates in the exchange of information so that the 2 clients can connect to each other and transfer the file to a separate connection from that of the server. 
