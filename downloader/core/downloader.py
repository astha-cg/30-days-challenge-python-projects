import requests
import threading
import os

def download_chunk(url, start, end, filename, index):
    headers = {"Range": f"bytes={start}-{end}"}
    response = requests.get(url, headers=headers, stream=True)

    part_file = f"{filename}.part{index}"
    with open(part_file, "wb") as f:
        for chunk in response.iter_content(1024 * 1024):
            if chunk:
                f.write(chunk)

def merge_files(filename, num_threads):
    with open(filename, "wb") as final_file:
        for i in range(num_threads):
            part_file = f"{filename}.part{i}"
            with open(part_file, "rb") as pf:
                final_file.write(pf.read())
            os.remove(part_file)

def start_download(url, filename, num_threads=4):
    response = requests.head(url, allow_redirects=True)
    file_size = int(response.headers.get("Content-Length", 0))

    chunk_size = file_size // num_threads
    threads = []

    for i in range(num_threads):
        start = i * chunk_size
        end = file_size - 1 if i == num_threads - 1 else start + chunk_size - 1

        t = threading.Thread(
            target=download_chunk,
            args=(url, start, end, filename, i)
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    merge_files(filename, num_threads)