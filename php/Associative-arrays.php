<?php 
    $users = [
        "name" => "Saurabh",
        "age" => 25,
        "email" => "msaurya1600x@gmail.com",
        "city" => "Surat"
    ];

    echo "User Information<br>";
    echo "<br>Name: " . $users["name"];
    echo "<br>Age: " . $users["age"];
    echo "<br>Email: " . $users["email"];
    echo "<br>City: " . $users["city"];

    // printing by using foreach loop -

    foreach( $users as $key => $value ) {
        echo "<br>" . $key . " : " . $value ;
    }
?>