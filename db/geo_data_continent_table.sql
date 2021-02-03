-- MariaDB dump 10.17  Distrib 10.4.6-MariaDB, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: geo_data
-- ------------------------------------------------------
-- Server version	8.0.18

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `continent_table`
--

DROP TABLE IF EXISTS `continent_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `continent_table` (
  `country` varchar(32) NOT NULL,
  `continent` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`country`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `continent_table`
--

LOCK TABLES `continent_table` WRITE;
/*!40000 ALTER TABLE `continent_table` DISABLE KEYS */;
INSERT INTO `continent_table` VALUES ('Afghanistan','Asia'),('Albania','Europe'),('Algeria','Africa'),('Andorra','Europe'),('Angola','Africa'),('Antigua and Barbuda','North America'),('Argentina','South America'),('Armenia','Asia'),('Australia','Oceana'),('Austria','Europe'),('Azerbaijan','Asia'),('Bahamas','North America'),('Bahrain','Asia'),('Bangladesh','Asia'),('Barbados','North America'),('Belarus','Europe'),('Belgium','Europe'),('Belize','North America'),('Benin','Africa'),('Bhutan','Asia'),('Bolivia','South America'),('Bosnia and Herzegovina','Europe'),('Botswana','Africa'),('Brazil','South America'),('Brunei','Asia'),('Bulgaria','Europe'),('Burkina Faso','Africa'),('Burma','Asia'),('Burundi','Africa'),('Cabo Verde','Africa'),('Cambodia','Asia'),('Cameroon','Africa'),('Canada','North America'),('Central African Republic','Africa'),('Chad','Africa'),('Chile','South America'),('China','Asia'),('Colombia','South America'),('Comoros','Africa'),('Congo (Brazzaville)','Africa'),('Congo (Kinshasa)','Africa'),('Costa Rica','North America'),('Cote d\'Ivoire','Africa'),('Croatia','Europe'),('Cuba','North America'),('Cyprus','Asia'),('Czechia','Europe'),('Denmark','Europe'),('Diamond Princess','Cruise'),('Djibouti','Africa'),('Dominica','North America'),('Dominican Republic','North America'),('Ecuador','South America'),('Egypt','Africa'),('El Salvador','North America'),('Equatorial Guinea','Africa'),('Eritrea','Africa'),('Estonia','Europe'),('Eswatini','Africa'),('Ethiopia','Africa'),('Fiji','Oceana'),('Finland','Europe'),('France','Europe'),('Gabon','Africa'),('Gambia','Africa'),('Georgia','Asia'),('Germany','Europe'),('Ghana','Africa'),('Greece','Europe'),('Grenada','North America'),('Guatemala','North America'),('Guinea','Africa'),('Guinea-Bissau','Africa'),('Guyana','South America'),('Haiti','North America'),('Holy See','Europe'),('Honduras','North America'),('Hungary','Europe'),('Iceland','Europe'),('India','Asia'),('Indonesia','Asia'),('Iran','Asia'),('Iraq','Asia'),('Ireland','Europe'),('Israel','Asia'),('Italy','Europe'),('Jamaica','North America'),('Japan','Asia'),('Jordan','Asia'),('Kazakhstan','Asia'),('Kenya','Africa'),('Korea, South','Asia'),('Kosovo','Europe'),('Kuwait','Asia'),('Kyrgyzstan','Asia'),('Laos','Asia'),('Latvia','Europe'),('Lebanon','Asia'),('Lesotho','Africa'),('Liberia','Africa'),('Libya','Africa'),('Liechtenstein','Europe'),('Lithuania','Europe'),('Luxembourg','Europe'),('Madagascar','Africa'),('Malawi','Africa'),('Malaysia','Asia'),('Maldives','Asia'),('Mali','Africa'),('Malta','Europe'),('Marshall Islands','Oceana'),('Mauritania','Africa'),('Mauritius','Africa'),('Mexico','North America'),('Moldova','Europe'),('Monaco','Europe'),('Mongolia','Asia'),('Montenegro','Europe'),('Morocco','Africa'),('Mozambique','Africa'),('MS Zaandam','Cruise'),('Namibia','Africa'),('Nepal','Asia'),('Netherlands','Europe'),('New Zealand','Oceana'),('Nicaragua','North America'),('Niger','Africa'),('Nigeria','Africa'),('North Macedonia','Europe'),('Norway','Europe'),('Oman','Asia'),('Pakistan','Asia'),('Panama','North America'),('Papua New Guinea','Oceana'),('Paraguay','South America'),('Peru','South America'),('Philippines','Asia'),('Poland','Europe'),('Portugal','Europe'),('Qatar','Asia'),('Romania','Europe'),('Russia','Asia'),('Rwanda','Africa'),('Saint Kitts and Nevis','North America'),('Saint Lucia','North America'),('Saint Vincent and the Grenadines','North America'),('Samoa','Oceana'),('San Marino','Europe'),('Sao Tome and Principe','Africa'),('Saudi Arabia','Asia'),('Senegal','Africa'),('Serbia','Europe'),('Seychelles','Africa'),('Sierra Leone','Africa'),('Singapore','Asia'),('Slovakia','Europe'),('Slovenia','Europe'),('Solomon Islands','Oceana'),('Somalia','Africa'),('South Africa','Africa'),('South Sudan','Africa'),('Spain','Europe'),('Sri Lanka','Asia'),('Sudan','Africa'),('Suriname','South America'),('Sweden','Europe'),('Switzerland','Europe'),('Syria','Asia'),('Taiwan*','Asia'),('Tajikistan','Asia'),('Tanzania','Africa'),('Thailand','Asia'),('Timor-Leste','Asia'),('Togo','Africa'),('Trinidad and Tobago','North America'),('Tunisia','Africa'),('Turkey','Asia'),('Uganda','Africa'),('Ukraine','Europe'),('United Arab Emirates','Asia'),('United Kingdom','Europe'),('United States of America','North America'),('Uruguay','South America'),('Uzbekistan','Asia'),('Vanuatu','Oceana'),('Venezuela','South America'),('Vietnam','Asia'),('West Bank and Gaza','Asia'),('Western Sahara','Africa'),('Yemen','Asia'),('Zambia','Africa'),('Zimbabwe','Africa');
/*!40000 ALTER TABLE `continent_table` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-12-12 16:27:18
