import sys
MY_IP = "0.0.0.0"

DNS_TABLE = {
    'www.malicious.onion':"0.0.0.1",'www.regular_website.com':"0.0.0.2",'toronto_news.com':"0.0.0.3"
}

def requestWithoutTor(dst):

    return

def requestUsingTor(dst):

    return
if __name__ == "__main__":

    args = sys.argv

    #first argument is client.py, second is mode and third is serverlocation

    if len(args) != 3:

        exit(0)


    MODE = args[1]

    if not MODE in ['tor','regular']:

        exit(0)

    DESTINATION = args[2]

    if DESTINATION not in ['www.malicious.onion','www.regular_website.com','toronto_news.com']:

        exit(0)

    if MODE == 'regular':

        requestWithoutTor(DESTINATION)
        exit(0)

    if MODE == 'tor':
        requestUsingTor(DESTINATION)
        
    





