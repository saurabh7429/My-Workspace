<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home page</title>
</head>
<body>
    <h3>Home page</h3>

    <form action="" method="get">

        <label for="name">Name :</label>
        <input type="text" name="name" required>

        <button type="submit">Submit</button>
    </form>
    <?php 
        require_once "array-db.php";
        
        echo "<pre>";
        print_r($emp);
        echo "</pre>";
        if (isset($_GET["name"])) {
            $lastid = end( $emp["id"]);
            $emp["id"][] = $lastid + 1;
            $emp["name"][] = $_GET["name"];
        }

       
        
    ?>
    <table border="2">
        <tr>
            <th>id</th>
            <th>name</th>
        </tr>
        <?php 
            for ( $i=0; $i < count($emp["id"]); $i++){
                echo "<tr>";
                echo "<td>" . $emp["id"][$i] . "</td>";
                echo "<td>" . $emp["name"][$i] . "</td>";
                echo "</tr>";
            }
        ?>
            
        
    </table>
</body>
</html>