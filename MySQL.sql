-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS `app_database`;

USE app_database;

-- Create the user_roles table with id starting from 1000
CREATE TABLE `user_roles` (
  `id` INT AUTO_INCREMENT NOT NULL,
  `rolename` VARCHAR(255) NOT NULL,
  `description` TEXT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci AUTO_INCREMENT=1000;

-- Create the new Users table
CREATE TABLE `users` (
  `id` INT AUTO_INCREMENT NOT NULL,
  `user_role_id` INT NOT NULL,
  `userid` VARCHAR(255) NOT NULL,
  `password` VARCHAR(64) NOT NULL,  -- Adjusted for SHA-256 hash length
--  `active` BOOLEAN NOT NULL DEFAULT FALSE,
  `created_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UserId_UNIQUE` (`userid`),
  FOREIGN KEY (`user_role_id`) REFERENCES `user_roles`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Create the user_session_table
CREATE TABLE `user_session_table` (
  `user_id` INT NOT NULL,
  `session_id` VARCHAR(36) NOT NULL,
  `session_created` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `session_updated` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `client_remote_ip` VARCHAR(45) NOT NULL,
  `is_valid` BOOLEAN DEFAULT FALSE,
  `session_closed_time` TIMESTAMP,
  PRIMARY KEY (`session_id`),
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Create the audit_table
CREATE TABLE `audit_table` (
  `client_ip` VARCHAR(45) NOT NULL,
  `time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `reason_of_failure` TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;




-- Insert dummy data into user_roles
INSERT INTO `user_roles` (`rolename`, `description`) VALUES
('Admin', 'Administrator role with full access'),
('User', 'Standard user role with limited access');
--
-- insert dummy users
INSERT INTO `users` (`user_role_id`, `userid`, `password`)
VALUES (1000, 'admin', SHA2('admin', 256));

INSERT INTO `users` (`user_role_id`, `userid`, `password`)
VALUES (1001, 'devesh', SHA2('mishra', 256));
