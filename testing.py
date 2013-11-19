from rtorrent import RTorrent
import texttable
import pprint
def calc_size(n):
    unit_index = 0
    size_reduced = n
    # we don't want a result in the thousands
    while size_reduced >= 1000:
        size_reduced /= float(1024)
        unit_index += 1
    return(size_reduced, unit_index)


def format_size(bytes_):


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

def format_speed(bits):
    units = ("KB", "MB", "GB", "TB")
    # convert bits to kilobits before calculating (we dont want 0.0 b/s)
    bits /= float(1024)
    speed_reduced, unit_index = calc_size(bits)
    speed_formatted = "{0:.1f}{1}/s".format(speed_reduced,
                                        units[unit_index])
    return(speed_formatted)


table = texttable.Texttable(max_width=350)
table.set_precision(2)
table.set_deco(texttable.Texttable.HEADER)
r = RTorrent(url="http://admin:zxczxc@rtorrent.opensrc.mx")
for torrent in r.get_torrents():
    complete_per = format_percentage( torrent.completed_bytes, torrent.size_bytes)
    connected = torrent.get_peers_connected()
    total = connected + torrent.get_peers_not_connected()
    table.add_row([
        torrent.get_name(),
        "%s of %s" %(connected,total),
        "%s%%" % complete_per,
        format_size(torrent.size_bytes),
        format_ratio(torrent.ratio),
    ])
output = table.draw()
if output: print output

table.reset()

table = texttable.Texttable(max_width=80)
table.set_deco(texttable.Texttable.HEADER)

table.add_row([ 
        "DW:%s" %format_speed(r.get_down_rate()),
        "UP:%s" %format_speed(r.get_up_rate()),
        " ",
        " ",
        ])
print table.draw()
