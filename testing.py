from rtorrent import RTorrent
import texttable
import pprint

def format_size(bytes_):
    def calc_size(n):
        unit_index = 0
        size_reduced = n
        # we don't want a result in the thousands
        while size_reduced >= 1000:
            size_reduced /= float(1024)
            unit_index += 1
        return(size_reduced, unit_index)


    units = ("B", "KB", "MB", "GB", "TB")
    size_reduced, unit_index = calc_size(bytes_)
    size_formatted = "{0:.2f}{1}".format(size_reduced,
                                        units[unit_index]) 
    return(size_formatted)

def format_percentage(completed, total):
    p_float = (completed / (total * 1.00)) * 100
    p_formatted = "{0:2.1f}".format(p_float)
    return(p_formatted)

def format_ratio(ratio):
    ratio_formatted = "{0:.2f}R".format(ratio)
    return(ratio_formatted)


table = texttable.Texttable(max_width=350)
table.set_deco(texttable.Texttable.HEADER)
table.set_cols_dtype(['t','a','a','a','f'])
table.set_precision(2)
r = RTorrent(url="http://localhost")
for torrent in r.get_torrents():
    complete_per = format_percentage( torrent.completed_bytes, torrent.size_bytes)
    table.add_row([
        torrent.get_name(),
        "%s of %s" %(torrent.get_peers_connected(),len(torrent.get_peers())),
        "%s%%" % complete_per,
        format_size(torrent.size_bytes),
        format_ratio(torrent.ratio),
    ])
print table.draw()
