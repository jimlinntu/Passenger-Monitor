<?php

// Polls Passenger statistics from script via SNMP
use LibreNMS\RRD\RrdDefinition;

$name = 'passenger';
$app_id = $app['app_id'];
if (!empty($agent_data['app'][$name])) {
    $passenger = $agent_data['app'][$name];
} else {
    $options = '-Oqv';
    // You can use `snmptranslate` to verify this oid is `NET-SNMP-EXTEND-MIB::nsExtendOutputFull."passenger"`
    $oid     = '.1.3.6.1.4.1.8072.1.3.2.3.1.2.9.112.97.115.115.101.110.103.101.114'; 
    $passenger  = snmp_get($device, $oid, $options);
}

echo ' passenger powered by Jim Lin';

list ($wait_list_size) = explode("\n", $passenger);

$rrd_name = array('app', $name, $app_id);
$rrd_def = RrdDefinition::make()->addDataset('wait_list_size', 'GAUGE', 0);

$fields = array('wait_list_size'       => $wait_list_size);

$tags = compact('name', 'app_id', 'rrd_name', 'rrd_def');
data_update($device, 'app', $tags, $fields);
update_application($app, $passenger, $fields);
