<?php 
    $students = [
        "Rahul",
        "Aman",
        "Saurabh",
        "Priya",
        "Rohit"
    ];

    echo "Student List: <br><br>";
    foreach( $students as $key => $student ) {
        echo ( $key + 1 ) . ". ". $student . "<br>";
    }
?>