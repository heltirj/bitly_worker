import requests
import os
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv

API_URL = "https://api-ssl.bitly.com"

def shorten_link(long_url, token):
    url = f"{API_URL}/v4/shorten"
    data = {"long_url": long_url}
    response = requests.post(url,
                             headers=get_headers(token),
                             json=data)
    response.raise_for_status()
    return response.json()["link"]


def cut_bitlink(bitlink):
    parsed_bitlink = urlparse(bitlink)
    cutted_bitlink = f"{parsed_bitlink.netloc}{parsed_bitlink.path}"
    return cutted_bitlink


def count_clicks(bitlink, token):
    url = f"{API_URL}/v4/bitlinks/{cut_bitlink(bitlink)}/clicks/summary"
    response = requests.get(url, headers=get_headers(token))
    response.raise_for_status()
    return response.json()["total_clicks"]


def is_bitlink(link, token):
    url = f"{API_URL}/v4/bitlinks/{cut_bitlink(link)}"
    response = requests.get(url, headers=get_headers(token))
    return response.ok


def get_headers(token):
    return {"Authorization": f"Bearer {token}"}


def main():
    load_dotenv()
    bitly_token = os.getenv("BITLY_TOKEN")
    parser = argparse.ArgumentParser(
        description="Script for creating bitly " \
                    "links and counting statistics")
    parser.add_argument("link", help="Shorten or full link to web source")
    args = parser.parse_args()
    link = args.link.strip()
    try:
        if is_bitlink(link, bitly_token):
            print(f"Count of clicks to {link}: "
                  f"{count_clicks(link, bitly_token)}")
        else:
            print(f"Shorten link: {shorten_link(link, bitly_token)}")
    except requests.exceptions.HTTPError as err:
        print(err)


if __name__ == "__main__":
    main()