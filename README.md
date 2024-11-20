# tor_simulation_using_web_servers

Group: 
Youngjae Heo 
Juefei Lu

Our project idea is to make a simulation of tor and in part data encapsulation and encryption between routers. 
The main language we will use is Python
Some libraries we will use are Docker to host many(5 or more) routers at once as well as the source and destination hosts, pycryptodome for encryption, and http.server library in Python since we want to simulate routers and hosts with web servers.

The encapsulation of each packet within another packet will be done manually(one packet as JSON object encapsulated by another JSON object) during the routing encryption. Also we will encode the json payload into bytes to be sent across the network.

Path selection between client and host is dynamic.

Timeline Information: 
Proposal Deadline: November 4th, 2024
Nov 11th, 2024: we create the routers, hosts, and the dynamic path with encapsulation.
Nov 18th, 2024: we finish the routing logic for the routers and encryption of the user packets.
Nov 25th, 2024: we add the multiple layers to each packet and account for mac address routing
Dec 3rd, 2024: we complete anything that hasn’t been completed and submit.

How the project relates to the field of “Computer Networks”
It touches all the layers above the data link layer of the network model, and uses everything we learned so far from basic ARP address resolution to advanced routing and incorporating the dynamic path selection feature of the TOR networks. 


Idea:

- you can dynamically create servers
- when trying to access a website because it doens't serve to your Country, make a slightly less random route with the exit node at an allowed Country
- when trying to access a .onion site just give a warnign and get back the response

