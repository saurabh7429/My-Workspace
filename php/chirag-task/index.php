<?php 
    session_start();

    if(!isset($_SESSION["emp"])) {
        $_SESSION["emp"] = [
            [
                "id" => 1,
                "name" => "saurabh",
                "age" => 20
            ]
        ];
    }
    $emp = &$_SESSION["emp"];
    if (isset($_GET["name"]) && isset($_GET["name"]) !== "" && $_GET["age"] !== "") {
            $lastid = end($emp)["id"];
            $emp[] = [
                "id" => $lastid + 1,
                "name" => $_GET["name"],
                "age" => $_GET["age"]
            ];
            echo "<pre>";
            print_r($emp);
            echo "<pre/>";
    }
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HOME PAGE</title>
</head>
<body>
    <h3>Insert yout data</h3>

    <form action="" method="get">
        Name :<input type="text" name="name" id="naem" >
        Age : <input type="number" name="age" id="age" >
        <button type="submit">Insert</button>
        <a href="view.php">VIEW</a>
    </form>

</body>
</html>