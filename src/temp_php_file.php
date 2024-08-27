<?php
//This php is for the user regististration part 
session_start();
// Change this to your connection info.
$DATABASE_HOST = 'localhost';
$DATABASE_EMAIL = '';
$DATABASE_USER = 'root';
$DATABASE_PASS = '';


$DATABASE_NAME = 'wolverinework';
$errors = array(); 


// Try and connect using the info above.
$con = mysqli_connect($DATABASE_HOST, $DATABASE_USER, $DATABASE_PASS, $DATABASE_NAME);

if (mysqli_connect_errno()) {
	exit('Failed to connect to MySQL: ' . mysqli_connect_error());
}



// REGISTER USER
if (isset($_POST['reg-user'])) {
	// receive all input values from the registration form
    $firstname = mysqli_real_escape_string($con, $_POST['firstname']);
	$lastname = mysqli_real_escape_string($con, $_POST['lastname']);
	$username = mysqli_real_escape_string($con, $_POST['username']);
	$email = mysqli_real_escape_string($con, $_POST['email']);
	$password = mysqli_real_escape_string($con, $_POST['password']);
	
	// form validation: ensure that the form is correctly filled ...
	// by adding (array_push()) corresponding error unto $errors array
    if (empty($firstname)) { array_push($errors, "First name is required"); }
    if (empty($lastname)) { array_push($errors, "Last name is required"); }
	if (empty($username)) { array_push($errors, "Username is required"); }
	if (empty($email)) { array_push($errors, "Email is required"); }
	if (empty($password)) { array_push($errors, "Password is required"); }
	
	$emailInput = $_POST['email'];

	// first check the database to make sure 
	// a user does not already exist with the same username and/or email
	$user_check_query = "SELECT email FROM account WHERE email='$emailInput'";
	$result = mysqli_query($con, $user_check_query);
	$user = mysqli_fetch_assoc($result);
	
	
    if ($user) { // if user exists
		if ($user['email'] === $emailInput) {
		  array_push($errors, "email already exists");
		}
        echo'Already have an account!'; //this works
    }

    // Make sure we have input
    // Remove extra white space if we do
    $email = isset($_POST['email']) ? trim($_POST['email']) : null;

    // List of allowed domains
    $allowed = [
        'umich.edu',
    ];

    // Make sure the email address is valid
    if (filter_var($email, FILTER_VALIDATE_EMAIL)){

        // Separate string by @ characters (there should be only one)
        $parts = explode('@', $email);

        // Remove and return the last part, which should be the domain
        $domain = array_pop($parts);

        // Check if the domain is in our list
        if ( ! in_array($domain, $allowed))
        {
            // Not allowed
            echo 'Did not input a correct University of Michigan email, try again!';
        }
        else {
            // Finally, register user if there are no errors in the form
            if (count($errors) == 0) {
                $passwordEncrypt = md5($password);//encrypt the password before saving in the database

                $query = "INSERT INTO account (first_name, last_name, username, email, password) 
                                VALUES('$firstname', '$lastname','$username', '$email', '$passwordEncrypt')";
                mysqli_query($con, $query);
                session_regenerate_id();
                $_SESSION['loggedin'] = TRUE;
                $_SESSION['name'] = $_POST['username'];
                //$_SESSION['username'] = $username;
                $_SESSION['success'] = "You are now logged in and registered!";
            
                //CHANGE TO HOME FILE
                header('Location: ../homepage/homepage.php');
                //echo 'homepage';
                exit;
            }
        }  
    }


}
?>
