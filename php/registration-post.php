<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registration form</title>
</head>
<body>
    <h2>Student Registration</h2>

    <form action="" method="POST">
        <label for="name" >Name: </label>
        <input type="text" name="name" id="name"><br>

        <label for="age">Age: </label>
        <input type="number" name="age" id="age"><br>

        <label for="email">E-mail: </label>
        <input type="email" name="email" id="email"><br>
        
        <button type="submit">Register</button>
    </form>

    <?php 
        if(isset($_POST["name"])) {
            echo "<h2>Welcome " . $_POST["name"] . "</h2>";
            echo "<p>Age: " . $_POST["age"] . "</p>";
            echo "<p>Email: " . $_POST["email"] . "</p>";
        }
    ?>
</body>
</html>