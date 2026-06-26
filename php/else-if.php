<?php 
    $marks = 78;
    $name = "Saurabh";

    echo "Student: " . $name . "<br>Marks: " . $marks . "<br>";

    if ( $marks >= 90 ) {
        echo "Grade: A";
    } elseif ( $marks >= 75 ) {
        echo "Grade: B";
    } elseif ( $marks >= 60 ) {
        echo "Grade: C";
    } elseif ( $marks >= 35 ) {
        echo "Grade: D";
    } else {
        echo "Fail";
    }
?>