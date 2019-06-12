#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import subprocess # Execute command
import os
import time
CACHETIME = 30 # write file every 30 seconds
CACHEFILE = '/tmp/passenger-snmp'
CANVAS_ABS_PATH = "/var/canvas"
DEBUG=True # Turn on if you want to see whole xml file of `sudo passenger-status`


def sudo_passenger_status():
    # [*] Execute `sudo passenger-status --show=xml`
    completed_process = subprocess.run(["sudo", "passenger-status", "--show=xml"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    xml_string = completed_process.stdout.decode("utf-8")

    return xml_string

# If there is a cache file that is modified `CACHETIME ago, then just return the result in that cache file
def get_cache():
    canvas_get_wait_list_size = 0
    # Note: os.stat( * ) [8] == mtime(modified time)
    if os.path.isfile ( CACHEFILE ) and ( time.time() - os.stat ( CACHEFILE )[8]) < CACHETIME:
            # use cached data
            f = open ( CACHEFILE, 'r' )
            canvas_get_wait_list_size = int(f.read())
            f.close()
    else:
            xml_string = sudo_passenger_status()
            # write file
            f = open ( CACHEFILE+'.TMP.'+ repr(os.getpid()), 'w' )
            print(os.getpid())
            canvas_get_wait_list_size = parse_xml_string(xml_string)
            f.write ( str(canvas_get_wait_list_size) )
            f.close()
            os.rename ( CACHEFILE+'.TMP.'+repr(os.getpid()), CACHEFILE ) # mv CACHE_FILE.TMP.pid CACHE_FILE.TMP

    return canvas_get_wait_list_size

def parse_xml_string(xml_string):
    root = ET.fromstring(xml_string)

    if DEBUG:
        import xml.dom.minidom
        dom = xml.dom.minidom.parseString(xml_string)
        print(dom.toprettyxml())

    canvas_get_wait_list_size = 0
    for child in root:
        # [*] If there exist application group being processsed
        if child.tag == "supergroups":
            for supergroup in child:
                # Find the first subelement
                if CANVAS_ABS_PATH in supergroup.find("name").text:
                   canvas_group = supergroup.find("group")
                   assert(CANVAS_ABS_PATH in canvas_group.find("name").text)
                   canvas_get_wait_list_size = int(canvas_group.find("get_wait_list_size").text)

    return canvas_get_wait_list_size

def chmod_rx():
    os.chmod(CACHEFILE, 0o555) # r_xr_xr_x

def main():
    # Canvas requests in queue
    canvas_get_wait_list_size = get_cache()
    # chmod so that snmp user can read
    chmod_rx()

if __name__ == "__main__":
    main()
