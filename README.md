# Passenger Monitoring

# Requirements

* OS: Ubuntu
* check whether you can run `sudo passenger-status` because we will use this command in the following setup


# Set up

* Use crontab to set make `passegenr-monitor.py` run for every minute
```
sudo crontab -u root -e
# Add this line
*/1 * * * * /home/ctld/Passenger-Monitor/passenger-monitor.py
```
* Set `/etc/snmpd.conf` so that snmpd can `cat /tmp/passenger-snmp`
```
sudo vim /etc/snmpd.conf
# Add this line at the end of file
extend passenger /bin/cat /tmp/passenger-snmp
# Restart your snmpd
sudo systemctl restart snmpd
```

* Test whether your set up is correct
```
snmpwalk -c <your community string> localhost NET-SNMP-EXTEND-MIB::nsExtendOutput2Table | grep 'passenger'
```
you should see a line showing the requests in the queue of `/var/canvas` application

* Have a glimpse on extended oid(Note that you should escape quotes to avoid interpretation by shell)
```
snmptranslate NET-SNMP-EXTEND-MIB::nsExtendOutLine.\"passenger\".1
```


# References
* https://blog.slowb.ro/monitor-passenger-applications-via-snmp/
* http://net-snmp.sourceforge.net/wiki/index.php/Tut:Extending_snmpd_using_shell_scripts
* http://net-snmp.sourceforge.net/tutorial/tutorial-5/commands/snmptranslate.html

