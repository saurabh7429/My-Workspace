<?php 
    function greet($name) {
        echo "Hello, " . $name . "<br>";
    }

    function addition( $num1, $num2 ) {
        return $num1 + $num2;
    }

    $name = "Saurabh";
    $result = addition(20, 15);
    
    greet("$name");
    echo "Addition is: " . $result;
?>