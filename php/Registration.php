<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Registration</title>
</head>
<body>
    <h2>Student Registration</h2>
    <form action="" method="get" >
        <label for="name">Name: </label>
        <input type="text" name="name" id="name" ><br>

        <label for="age">Age: </label>
        <input type="number" name="age" id="age"><br>

        <label for="email">Email: </label>
        <input type="email" name="email" id="email"><br>

        <button type="submit">Register</button>
        <?php
            echo "<h2>Welcome " . $_GET["name"] . "</h2>";
            
        ?>
    </form>
</body>
</html>