<?php
    $marks = 82;
    $name = "Saurabh";

    if ( $marks >= 35 ) {
        if ($marks >= 75 ) {
            echo "Grade: Distinction<br>";
        } 
        echo $name . ", You Passed.";
    } else {
        echo $name . ", You Failed.";
    }
?>