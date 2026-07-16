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
        <input type="text" name="name" require>

        <button type="submit">Submit</button>
    </form>
    <?php 
        include "array-db.php";
        
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
            echo "<tr>";
            for ( $i=0; $i < count($emp["id"]); $i++){
                echo "<td>" . $emp["id"][$i] . "</td>";
                echo "<td>" . $emp["name"][$i] . "</td>";
            }
            echo "/<tr>";
        ?>
            
        
    </table>
</body>
</html>