
<link rel="stylesheet" href="halloween.css" title="halloween-css" media="all" type="text/css">
<html>
<body>
<div class="outer">
<div class="middle">
<div class="inner">
<table class="input">
<tr>
<?php
    date_default_timezone_set('America/Los_Angeles');
    // The global $_POST variable allow to access the data send with the POST method
    // To access the data send with the GET method, you can use $_GET
    $name = htmlspecialchars($_POST['name']);
    $email  = htmlspecialchars($_POST['email']);
    
    include('connectioninfo.php');
    $dbh = mysql_connect($hostname, $username, $password)
        or die(mysql_error());
    $selected = mysql_select_db($database,$dbh) 
        or die(mysql_error());
    // Check to see if they have already registered
    $query  = "SELECT COUNT(*) FROM goodvsevil WHERE email='".$email."'";
    $result = mysql_query($query);
    $fetch  = mysql_fetch_row($result);
    if($fetch[0] == 0)
    {
        $query = "INSERT INTO goodvsevil (name, email) VALUES ('".$name."','".$email."')";
        mysql_query($query) or die(mysql_error());
        echo  "<td>Thank you ".$name." for joining in on the adventure!</td>";
    }
    else
    {
        echo  "<td>Thank you ".$name." but you have already registered.</td>";
    }
    mysql_close($dbh);
    
?>
<tr>
    <td><br><br>You will be receiving an email 24 hrs before the party with your role for the night.</td>
</tr>
</table>
</div>
</div>
</div>

</body>
</html>