#!/usr/bin/php
<?php
include_once dirname(__FILE__) . '/../php_inc/password.inc';
include_once dirname(__FILE__) . '/../php_inc/bootstrap.inc';

function my_user_check_password($password, $stored_hash) {  
  print( "Passwort = $password, stored_hash = $stored_hash\n");
  $type = substr($stored_hash, 0, 3);
  switch ($type) {
    case '$S$':
      // A normal Drupal 7 password using sha512.
      $hash = _password_crypt('sha512', $password, $stored_hash);
      print( "Normal Drupal 7 password, hash = $hash\n");
      break;
    case '$H$':
      // phpBB3 uses "$H$" for the same thing as "$P$".
    case '$P$':
      // A phpass password generated using md5.  This is an
      // imported password or from an earlier Drupal version.
      $hash = _password_crypt('md5', $password, $stored_hash);
      break;
    default:
      return FALSE;
  }
  return ($hash && $stored_hash == $hash);
}

var_dump( $argv);

/**
 * Drupal hash script - to generate a hash from a plaintext password
 *
 * Check for your PHP interpreter - on Windows you'll probably have to
 * replace line 1 with
 *   #!c:/program files/php/php.exe
 *
 * @param password1 [password2 [password3 ...]]
 *  Plain-text passwords in quotes (or with spaces backslash escaped).
 */

if (version_compare(PHP_VERSION, "5.2.0", "<")) {
  $version  = PHP_VERSION;
  echo <<<EOF

ERROR: This script requires at least PHP version 5.2.0. You invoked it with
       PHP version {$version}.
\n
EOF;
  exit;
}

$script = basename(array_shift($_SERVER['argv']));

if (in_array('--help', $_SERVER['argv']) || empty($_SERVER['argv'])) {
  echo <<<EOF

Generate Drupal password hashes from the shell.

Usage:        {$script} [OPTIONS] "<plain-text password>" "<hash">
Example:      {$script} "mynewpassword" "$$$abcdef"

All arguments are long options.

  --help      Print this page.

  --root <path>

              Set the working directory for the script to the specified path.
              To execute this script this has to be the root directory of your
              Drupal installation, e.g. /home/www/foo/drupal (assuming Drupal
              running on Unix). Use surrounding quotation marks on Windows.

  '<password1>' ['<password2>' ['<password3>' ...]]

              One or more plan-text passwords enclosed by double quotes. The
              output hash may be manually entered into the {users}.pass field to
              change a password via SQL to a known value.

To run this script without the --root argument invoke it from the root directory
of your Drupal installation as

  ./scripts/{$script}
\n
EOF;
  exit;
}

$passwords = array();

var_dump( $argv);
var_dump( $_SERVER['argv']);
// Parse invocation arguments.
while ($param = array_shift($_SERVER['argv'])) {
  print( "cmdLine = $param\n");
  switch ($param) {
    case '--root':
      // Change the working directory.
      $path = array_shift($_SERVER['argv']);
      if (is_dir($path)) {
        chdir($path);
      }
      break;
    default:
      // Add a password to the list to be processed.
      $passwords[] = $param;
      break;
  }
}

define('DRUPAL_ROOT', getcwd());

include_once dirname(__FILE__) . '/../php_inc/password.inc';
include_once dirname(__FILE__) . '/../php_inc/bootstrap.inc';

foreach( $passwords as $p) {
    print( "Eingabe = $p\n");
}
$test = my_user_check_password( $passwords[0], $passwords[1]);
print("\nErgebnis = ");
echo (int)$test;
print("\n");
exit( $test ? 1 : 0);
