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
def get_xml_string_in_cache():
      
    xml_string = None 
    # Note: os.stat( * ) [8] == mtime(modified time)
    if os.path.isfile ( CACHEFILE ) and ( time.time() - os.stat ( CACHEFILE )[8]) < CACHETIME:
            # use cached data
            f = open ( CACHEFILE, 'r' )
            xml_string = f.read()
            f.close()
    else:
            xml_string = sudo_passenger_status()
            # write file
            f = open ( CACHEFILE+'.TMP.'+ repr(os.getpid()), 'w' )
            print(os.getpid())
            
            f.write ( xml_string )
            f.close()
            os.rename ( CACHEFILE+'.TMP.'+repr(os.getpid()), CACHEFILE ) # mv CACHE_FILE.TMP.pid CACHE_FILE.TMP

    assert(xml_string is not None)

    return xml_string



def main():
    xml_string = get_xml_string_in_cache()
    root = ET.fromstring(xml_string)
    # Canvas requests in queue
    canvas_get_wait_list_size = 0

    if DEBUG:
        import xml.dom.minidom
        dom = xml.dom.minidom.parseString(xml_string)
        print(dom.toprettyxml())

    for child in root:
        # [*] If there exist application group being processsed
        if child.tag == "supergroups":
            for supergroup in child:
                # Find the first subelement
                if CANVAS_ABS_PATH in supergroup.find("name").text:
                   canvas_group = supergroup.find("group")
                   assert(CANVAS_ABS_PATH in canvas_group.find("name").text)
                   canvas_get_wait_list_size = int(canvas_group.find("get_wait_list_size").text)
    print(canvas_get_wait_list_size)

if __name__ == "__main__":
    main()
