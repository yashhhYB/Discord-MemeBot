import requests
import time
import socket
import pytest
from ping3 import ping

def get_url_info(url):
    try:
        start_time = time.time()
        response = requests.get(url, timeout=5)
        end_time = time.time()
        
        return {
            "status_code": response.status_code,
            "response_time": end_time - start_time,
            "headers": dict(response.headers),
            "content": response.json() if response.status_code == 200 else None
        }
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def get_ping(host):
    try:
        return ping(host, timeout=5) * 1000
    except Exception as e:
        return {"ping_error": str(e)}

def test_meme_api():
    url = "https://meme-api.com/gimme"
    url_info = get_url_info(url)
    host = socket.gethostbyname("meme-api.com")
    
    assert "error" not in url_info, f"Request error: {url_info.get('error')}"
    assert url_info["status_code"] == 200, f"Invalid status code: {url_info['status_code']}"
    assert url_info["content"], "Response content is empty."
    
    ping_time = get_ping(host)
    assert isinstance(ping_time, (int, float)), "Ping failed."
    
    print("--- API Information ---")
    print(f"Status Code: {url_info['status_code']}")
    print(f"Response Time: {url_info['response_time']:.2f} ms")
    print(f"Ping: {ping_time:.2f} ms")
    print("Headers:", url_info["headers"])
    print("Response Example:", url_info["content"])

if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])
