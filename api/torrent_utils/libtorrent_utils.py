import libtorrent
import time

def downloadMagnet(magnet_url):
    
    session = libtorrent.session()
    session.listen_on(6881, 6891)

    params = {"url":magnet_url, "save_path":'.'}

    h = session.add_torrent(params)

    h = getMetadataFromMagnet(session, magnet_url)

    while(not h.is_seed()):
        s = h.status()
        print(f"[*] Progress: {round(s.progress * 100, 2)}%, Peers: {s.num_peers}")
        time.sleep(1)

    print(f"[*] Download finished for: {h.name()}")
    return h.name()

def getMetadataFromMagnet(session, magnet_url):
    params = {"url":magnet_url, "save_path":'.'}

    h = session.add_torrent(params)

    print("[*] Collecting metadata...")
    
    while(not h.has_metadata()):
        time.sleep(1)
    
    return h

def getFileInfo(torrentInfo):
    attributes = [
        'path',
        'symlink_path',
        'offset',
        'size',
        'mtime',
        'filehash',
        'pad_file',
        'hidden_attribute',
        'executable_attribute',
        'symlink_attribute',
    ]
    for attr in attributes:
        print(getattr(torrentInfo, attr))

def downloadFileFromMagnet(magnet_url, file_name):

    session = libtorrent.session()
    session.listen_on(6881, 6891)

    params = {
        'url':magnet_url,
        'save_path':'.',
    }

    handle = session.add_torrent(params)

    print("[*] Collecting metadata (1).")
    while(not handle.has_metadata()):
        time.sleep(1)
    
    print("[*] Completed (1).")

    info = handle.get_torrent_info()

    priorities = []
    for file in info.files():
        if file_name == file.path:
            priorities.append(1)
        else:
            priorities.append(0)

    session = libtorrent.session()
    session.listen_on(6881, 6891)

    params = {
        'url':magnet_url,
        'save_path':'.',
        'file_priorities': priorities
    }

    handle = session.add_torrent(params)

    print("[*] Collecting metadata (2).")
    while(not handle.has_metadata()):
        time.sleep(1)
    
    while(not handle.is_seed()):
        s = handle.status()
        print(f"[*] Progress: {round(s.progress * 100, 2)}%, Peers: {s.num_peers}")
        if s.progress>=1:
            break
        time.sleep(1)
         
    print(f"[*] Download finished for: {handle.name()}")
    return file_name


if __name__ == "__main__":
    magnet_url = "magnet:?xt=urn:btih:c9e15763f722f23e98a29decdfae341b98d53056&dn=Cosmos+Laundromat&tr=udp%3A%2F%2Fexplodie.org%3A6969&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Ftracker.empire-js.us%3A1337&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=wss%3A%2F%2Ftracker.btorrent.xyz&tr=wss%3A%2F%2Ftracker.fastcast.nz&tr=wss%3A%2F%2Ftracker.openwebtorrent.com&ws=https%3A%2F%2Fwebtorrent.io%2Ftorrents%2F&xs=https%3A%2F%2Fwebtorrent.io%2Ftorrents%2Fcosmos-laundromat.torrent"
    downloadMagnet(magnet_url)
    #downloadFileFromMagnet(magnet_url, "Cosmos Laundromat/Cosmos Laundromat.mp4")
    


