import argparse
import os


from source.support import extract_credentials
from source.northbound.rest_calls import RestClient

DATA_DIR = os.path.join(os.path.dirname(__file__), "UNS")
FILES = os.listdir(DATA_DIR)

def main(): 
    parse = argparse.ArgumentParser()
    parse.add_argument("conn", type=str, default=None, help="REST User:Passowrd@IP:Port to send UNS through")
    parse.add_argument("UNS", type=str, choices=[param.split(".")[0] for param in FILES], default=None,
                       help="UNS group to publish")
    args = parse.parse_args()
    host, port, user, password = extract_credentials(args.conn)
    conn = RestClient(conn=f"{host}:{port}", auth=(user, password), timeout=30)

    

if __name__ == "__main__":
    main()

