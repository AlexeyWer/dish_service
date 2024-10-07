import argparse

from srv.web.app import Server

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--loglevel",
        dest="loglevel",
        action="store",
        default=None,
        help="Set logging level (10/20/30/40/50)"
    )
    args = parser.parse_args()
    Server(args).start_server()