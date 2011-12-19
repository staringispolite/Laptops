CREATE DATABASE IF NOT EXISTS laptop DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;

CREATE 
  USER 'laptop'@'localhost' 
  IDENTIFIED BY 'o^n%!e*54m212N}';

GRANT
  ALL ON laptop.*
  TO 'laptop'@'localhost';
