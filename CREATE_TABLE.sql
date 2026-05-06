-- MySQL/MariaDB CREATE TABLE statements for normalized schema
CREATE DATABASE IF NOT EXISTS user_db;
USE user_db;

-- Company table
CREATE TABLE IF NOT EXISTS users_company (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    catch_phrase TEXT,
    bs TEXT,
    INDEX idx_company_name (name)
);

-- Address table
CREATE TABLE IF NOT EXISTS users_address (
    id INT AUTO_INCREMENT PRIMARY KEY,
    street VARCHAR(255),
    suite VARCHAR(255),
    city VARCHAR(255) NOT NULL,
    zipcode VARCHAR(50),
    lat VARCHAR(50),
    lng VARCHAR(50),
    INDEX idx_city (city)
);

-- User table (main)
CREATE TABLE IF NOT EXISTS users_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    external_id INT NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(254) NOT NULL,
    phone VARCHAR(50),
    website VARCHAR(255),
    address_id INT NOT NULL,
    company_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (address_id) REFERENCES users_address(id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES users_company(id) ON DELETE CASCADE,
    
    INDEX idx_user_name (name),
    INDEX idx_external_id (external_id),
    INDEX idx_address_company (address_id, company_id)
);