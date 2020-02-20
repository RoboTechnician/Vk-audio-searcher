import vkaudio

config = {}
for prop in open('config.cfg', 'r').readlines():
    pair = prop.split('=')
    if len(pair) == 2:
        config[pair[0].strip()] = pair[1].strip()

myList = vkaudio.AudioList(config['remixsid'], config['owner_id'])
myList.search_audio(config['search'])
myList.save(config['json_result_file'])
if config['download'].lower() == 'true':
    count = int(config['download_count'])
    l = len(myList.list)
    for i in range(count if l >= count else l):
        myList.list[i].save_file(config['download_directory'])
