-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generato il: Gen 10, 2014 alle 12:55
-- Versione del server: 5.5.33
-- Versione PHP: 5.5.7-1~dotdeb.1

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `easyAround`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `client`
--

CREATE TABLE IF NOT EXISTS `client` (
  `ID` int(10) NOT NULL AUTO_INCREMENT,
  `dynamic` enum('1','2','3') NOT NULL,
  `quiet` tinyint(1) NOT NULL,
  `category` enum('young', 'adult', 'middleAged', 'edlerly'),
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Struttura della tabella `constraint`
--

CREATE TABLE IF NOT EXISTS `constraint` (
  `location_ID` int(10) NOT NULL,
  `client_ID` int(10) NOT NULL,
  `type` enum('include','avoid') NOT NULL,
  PRIMARY KEY (`location_ID`,`client_ID`),
  KEY `client_ID` (`client_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struttura della tabella `day`
--

CREATE TABLE IF NOT EXISTS `day` (
  `itinerary_ID` int(10) NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`itinerary_ID`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struttura della tabella `itinerary`
--

CREATE TABLE IF NOT EXISTS `itinerary` (
  `ID` int(10) NOT NULL AUTO_INCREMENT,
  `client_ID` int(10) NOT NULL,
  `withKids` tinyint(1) NOT NULL,
  `needsFreeTime` tinyint(1) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `client_ID` (`client_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Struttura della tabella `location`
--

CREATE TABLE IF NOT EXISTS `location` (
  `ID` int(10) NOT NULL AUTO_INCREMENT,
  `lat` decimal(10,8) NOT NULL,
  `lng` decimal(11,8) NOT NULL,
  `name` varchar(200) NOT NULL,
  `description` text NOT NULL,
  `rating` enum('1','2','3','4','5') NOT NULL,
  `intensive` tinyint(1) NOT NULL,
  `forKids` tinyint(1) DEFAULT NULL,
  `excludedCategory` enum('young', 'adult', 'middleAged', 'edlerly'),
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Struttura della tabella `preference`
--

CREATE TABLE IF NOT EXISTS `preference` (
  `client_ID` int(10) NOT NULL,
  `itinerary_ID` int(10) NOT NULL,
  `type` enum('shopping','culture','gastronomy','nightlife') NOT NULL,
  `range` enum('1','2','3','4','5') NOT NULL,
  PRIMARY KEY (`itinerary_ID`,`client_ID`,`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struttura della tabella `timeslot`
--

CREATE TABLE IF NOT EXISTS `timeslot` (
  `day_itinerary_ID` int(10) NOT NULL,
  `day_date` date NOT NULL,
  `type` enum('morning','afternoon','evening','meal') NOT NULL,
  `location_ID` int(10) NOT NULL,
  PRIMARY KEY (`day_itinerary_ID`,`day_date`,`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `constraint`
--
ALTER TABLE `constraint`
  ADD CONSTRAINT `constraint_ibfk_1` FOREIGN KEY (`location_ID`) REFERENCES `location` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `constraint_ibfk_2` FOREIGN KEY (`client_ID`) REFERENCES `client` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `constraint_ibfk_3` FOREIGN KEY (`itinerary_ID`) REFERENCES `itinerary` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `day`
--
ALTER TABLE `day`
  ADD CONSTRAINT `day_ibfk_1` FOREIGN KEY (`itinerary_ID`) REFERENCES `itinerary` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `itinerary`
--
ALTER TABLE `itinerary`
  ADD CONSTRAINT `itinerary_ibfk_1` FOREIGN KEY (`client_ID`) REFERENCES `client` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limiti per la tabella `timeslot`
--
ALTER TABLE `timeslot`
  ADD CONSTRAINT `timeslot_ibfk_1` FOREIGN KEY (`day_itinerary_ID`) REFERENCES `day` (`itinerary_ID`) ON DELETE CASCADE ON UPDATE CASCADE;
  ADD CONSTRAINT `timeslot_ibfk_2` FOREIGN KEY (`location_ID`) REFERENCES `location` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;


ALTER TABLE `preference`
  ADD CONSTRAINT `preference_ibfk_1` FOREIGN KEY (`client_ID`) REFERENCES `client` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `preference_ibfk_2` FOREIGN KEY (`itinerary_ID`) REFERENCES `itinerary` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
