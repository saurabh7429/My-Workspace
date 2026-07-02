<?php 
    $users = [
        [
            "name" => "Saurabh",
            "age" => 25,
            "city" => "Surat"
        ],
        [
            "name" => "Shreya",
            "age" => 24,
            "city" => "Ahemdabad"
        ],
        [
            "name" => "Khushi",
            "age" => 24,
            "city" => "Navsari"
        ]
    ];

    echo "<h3>User's Information</h3>";

    foreach ( $users as $key1 => $user ){
        echo "Student : " . ( $key1 + 1 ) . "<br>";
        foreach ( $user as  $key2 => $value ) {
            echo $key2 . " : " . $value . "<br>";
        }
        echo "<br>";
    }

?>