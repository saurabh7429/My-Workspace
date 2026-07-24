let gameNum = 10;

let userNum = prompt("Guess any number");
do {
    userNum = prompt("try again :");
} while ( gameNum != userNum );
alert("correct number");