def main():
    a = input ("File name: ")
    mime = media_type (a)
    print(mime, end = "")

def media_type (a):

    dict = {
    "gif": "image/gif",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "pdf": "application/pdf",
    "txt": "text/plain",
    "zip": "application/zip",
    }

    a = a.strip(" ").lower()
    suffixes = tuple(dict.keys())

    for suffix in suffixes:
        if a.endswith (suffix):
            return dict[suffix]

    return "application/octet-stream"

if __name__ == "__main__":
    main()
