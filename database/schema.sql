CREATE DATABASE IF NOT EXISTS rfq_marketplace
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE rfq_marketplace;

-- Tables are normally created automatically by Flask-SQLAlchemy.
-- This file is provided for reference/manual database creation.

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('buyer', 'supplier') NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS rfqs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    buyer_id INT NOT NULL,
    product_name VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    quantity INT NOT NULL,
    delivery_location VARCHAR(200) NOT NULL,
    deadline DATE NOT NULL,
    status ENUM('open', 'closed') DEFAULT 'open',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (buyer_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS quotations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rfq_id INT NOT NULL,
    supplier_id INT NOT NULL,
    quoted_price DECIMAL(12,2) NOT NULL,
    delivery_time VARCHAR(100) NOT NULL,
    message TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_supplier_rfq (rfq_id, supplier_id),
    FOREIGN KEY (rfq_id) REFERENCES rfqs(id) ON DELETE CASCADE,
    FOREIGN KEY (supplier_id) REFERENCES users(id) ON DELETE CASCADE
);
