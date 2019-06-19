<?php

$scale_min = 0;

require 'includes/graphs/common.inc.php';

$passenger_rrd = rrd_name($device['hostname'], array('app', 'passenger', $app['app_id']));

if (rrdtool_check_rrd_exists($passenger_rrd)) {
    $rrd_filename = $passenger_rrd;
}

$ds = 'wait_list_size';

$colour_area = 'CDEB8B';
$colour_line = '006600';

$colour_area_max = 'FFEE99';

// boolean value (1 indicates true). For more information please see 'includes/graphs/generic_simplex.inc.php'
$graph_max  = 1; 

$unit_text = 'Wait list size';

require 'includes/graphs/generic_simplex.inc.php';
