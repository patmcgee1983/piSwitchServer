<?php


// Constants used for now
$result = new stdClass();

require("connectionDetails.php");

$con = getConnection();


function makeError($message)
{
  $result = new stdClass();
  $result->status = "fail";
  $result->message = $message;
  echo json_encode($result);
  die();
}

if (!isset($_POST["name"]) || !isset($_POST["gpio"]) || !isset($_POST["startTime"]) || !isset($_POST["endTime"]))
{
  makeError("NULL value(s) passed into function!");
}

$name = $_POST["name"];
$gpio = $_POST["gpio"];
$startTime = $_POST["startTime"];
$endTime = $_POST["endTime"];

$sql = "INSERT INTO Zone (Name,StartTime,EndTime,Gpio) VALUES ($name,$startTime,$endTime,$gpio);";

if (!mysqli_query($con,$sql) {
	makeError("Error inserting into Database");
}
$result->status = "success";

echo json_encode($result);
?>
