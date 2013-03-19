<?php
            if ( strpos($_GET['patientId'], '1000272' ) !== FALSE ) {
                        header ('Location: http://folk.ntnu.no/chriper/Retningslinjer/index.html?id=39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62');
                        exit;
            }
            if ( strpos($_GET['patientId'], '1000270' ) !== FALSE ) {
                        header ('Location: http://folk.ntnu.no/chriper/Retningslinjer/index.html?id=51,50,61,62,39,40,41,42,43,44,45,46,47,48,49,52,53,54,55,56,57,58,59,60');
                        exit;
            }
            if ( strpos($_GET['patientId'], '1000218' ) !== FALSE ) {
                        header ('Location: http://folk.ntnu.no/chriper/Retningslinjer/search.html');
                        exit;
            }
?>