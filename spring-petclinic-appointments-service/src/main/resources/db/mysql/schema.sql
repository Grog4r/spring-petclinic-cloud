CREATE DATABASE IF NOT EXISTS petclinic;

CREATE USER IF NOT EXISTS 'pc'@'localhost' IDENTIFIED BY 'pc';
GRANT ALL PRIVILEGES ON petclinic.* TO 'pc'@'localhost';

USE petclinic;

CREATE TABLE IF NOT EXISTS appointments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  appointment_date DATETIME NOT NULL,
  description TEXT,
  owner_id INT NOT NULL,
  pet_id INT NOT NULL
);
