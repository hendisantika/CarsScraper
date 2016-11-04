CREATE TABLE `jualo_cars` (
  `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `url` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `description` mediumtext,
  `price` varchar(255) DEFAULT NULL,
  `contact_person` varchar(255) DEFAULT NULL,
  `posted` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

