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
-- Table structure for table `munic`
--

DROP TABLE IF EXISTS `munic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `munic` (
  `kunta` varchar(15) NOT NULL,
  `maakunta` varchar(17) DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  PRIMARY KEY (`kunta`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `munic`
--

LOCK TABLES `munic` WRITE;
/*!40000 ALTER TABLE `munic` DISABLE KEYS */;
INSERT INTO `munic` VALUES ('Äänekoski','Keski-Suomi',62.6032,25.7301),('Ähtäri','Etelä-Pohjanmaa',62.55,24.0702),('Akaa','Pirkanmaa',61.1575,23.7312),('Alajärvi','Etelä-Pohjanmaa',62.9999,23.8168),('Alavieska','Pohjois-Pohjanmaa',64.1701,24.2991),('Alavus','Etelä-Pohjanmaa',62.5862,23.6185),('Asikkala','Päijät-Häme',61.2332,25.5529),('Askola','Uusimaa',60.5272,25.6),('Aura','Varsinais-Suomi',60.65,22.5866),('Brändö','Ahvenanmaa',42.7739,9.47613),('Eckerö','Ahvenanmaa',60.228,19.5964),('Enonkoski','Etelä-Savo',62.0904,28.916),('Enontekiö','Lappi',68.714,22.044),('Espoo','Uusimaa',60.2242,24.6604),('Eura','Satakunta',61.1304,22.1302),('Eurajoki','Satakunta',61.2018,21.7297),('Evijärvi','Etelä-Pohjanmaa',63.3671,23.4769),('Finström','Ahvenanmaa',60.2802,19.886),('Föglö','Ahvenanmaa',60.0106,20.4246),('Forssa','Kanta-Häme',60.8156,23.6298),('Geta','Ahvenanmaa',60.3749,19.848),('Haapajärvi','Pohjois-Pohjanmaa',63.7515,25.3135),('Haapavesi','Pohjois-Pohjanmaa',64.1379,25.3658),('Hailuoto','Pohjois-Pohjanmaa',65.0138,24.7292),('Halsua','Keski-Pohjanmaa',63.4619,24.169),('Hämeenkyrö','Pirkanmaa',61.6333,23.2),('Hämeenlinna','Kanta-Häme',60.9949,24.4665),('Hamina','Kymenlaakso',60.5689,27.1882),('Hammarland','Ahvenanmaa',60.2197,19.7378),('Hankasalmi','Keski-Suomi',62.3905,26.4397),('Hanko','Uusimaa',59.8228,22.9695),('Harjavalta','Satakunta',61.3122,22.1336),('Hartola','Päijät-Häme',61.5799,26.0206),('Hattula','Kanta-Häme',61.0737,24.3905),('Hausjärvi','Kanta-Häme',60.7788,24.9736),('Heinävesi','Etelä-Savo',62.4264,28.6329),('Heinola','Päijät-Häme',61.2027,26.0314),('Helsinki','Uusimaa',60.1674,24.9426),('Hirvensalmi','Etelä-Savo',61.6416,26.7765),('Hollola','Päijät-Häme',60.9883,25.5153),('Honkajoki','Satakunta',61.993,22.2637),('Huittinen','Satakunta',61.1834,22.7003),('Humppila','Kanta-Häme',60.9333,23.3667),('Hyrynsalmi','Kainuu',64.6747,28.4923),('Hyvinkää','Uusimaa',60.6336,24.8695),('Ii','Pohjois-Pohjanmaa',-23.6041,-69.0843),('Iisalmi','Pohjois-Savo',63.5568,27.1892),('Iitti','Kymenlaakso',60.9515,26.2862),('Ikaalinen','Pirkanmaa',61.7701,23.0634),('Ilmajoki','Etelä-Pohjanmaa',62.7313,22.5798),('Ilomantsi','Pohjois-Karjala',62.6731,30.9323),('Imatra','Etelä-Karjala',61.1923,28.778),('Inari','Lappi',68.9062,27.0261),('Ingå','Uusimaa',60.0466,24.0054),('Isojoki','Etelä-Pohjanmaa',62.1143,21.9588),('Isokyrö','Pohjanmaa',63,22.3167),('Jakobstad','Pohjanmaa',63.6667,22.7),('Jämijärvi','Satakunta',61.8212,22.697),('Jämsä','Keski-Suomi',61.864,25.1845),('Janakkala','Kanta-Häme',60.9064,24.6186),('Järvenpää','Uusimaa',60.4744,25.0925),('Joensuu','Pohjois-Karjala',62.6006,29.7585),('Jokioinen','Kanta-Häme',60.8033,23.4868),('Jomala','Ahvenanmaa',59.9884,19.6668),('Joroinen','Etelä-Savo',62.1782,27.8285),('Joutsa','Keski-Suomi',61.7427,26.1117),('Juuka','Pohjois-Karjala',63.2413,29.2537),('Juupajoki','Pirkanmaa',61.822,24.4287),('Juva','Etelä-Savo',61.8961,27.8597),('Jyväskylä','Keski-Suomi',62.2393,25.746),('Kaarina','Varsinais-Suomi',60.4062,22.3686),('Kaavi','Pohjois-Savo',62.9758,28.4801),('Kajaani','Kainuu',64.2241,27.7334),('Kalajoki','Pohjois-Pohjanmaa',64.26,23.9505),('Kangasala','Pirkanmaa',61.4649,24.0659),('Kangasniemi','Etelä-Savo',61.9895,26.6441),('Kankaanpää','Satakunta',61.8027,22.3965),('Kannonkoski','Keski-Suomi',62.9769,25.2637),('Kannus','Keski-Pohjanmaa',63.9008,23.917),('Karijoki','Etelä-Pohjanmaa',62.3075,21.7078),('Karkkila','Uusimaa',60.5344,24.2145),('Kärkölä','Päijät-Häme',60.8677,25.2511),('Kärsämäki','Pohjois-Pohjanmaa',63.9797,25.7588),('Karstula','Keski-Suomi',62.8779,24.8008),('Karvia','Satakunta',62.1373,22.5603),('Kaskinen','Pohjanmaa',62.3846,21.2226),('Kauhajoki','Etelä-Pohjanmaa',62.4317,22.1842),('Kauhava','Etelä-Pohjanmaa',63.0994,23.057),('Kauniainen','Uusimaa',60.2147,24.7135),('Kaustinen','Keski-Pohjanmaa',63.549,23.6965),('Keitele','Pohjois-Savo',63.1788,26.3393),('Kemi','Lappi',65.7333,24.5667),('Kemijärvi','Lappi',66.7161,27.4334),('Keminmaa','Lappi',65.803,24.5209),('Kempele','Pohjois-Pohjanmaa',64.9125,25.5108),('Kerava','Uusimaa',60.4034,25.1041),('Keuruu','Keski-Suomi',62.258,24.7084),('Kihniö','Pirkanmaa',62.2031,23.1764),('Kimitoön','Varsinais-Suomi',59.8821,22.4034),('Kinnula','Keski-Suomi',63.3668,24.9709),('Kirkkonummi','Uusimaa',60.1228,24.4407),('Kitee','Pohjois-Karjala',62.1002,30.1356),('Kittilä','Lappi',67.652,24.9095),('Kiuruvesi','Pohjois-Savo',63.6528,26.6197),('Kivijärvi','Keski-Suomi',63.1223,25.0725),('Kökar','Ahvenanmaa',59.9242,20.9019),('Kokemäki','Satakunta',61.2513,22.3492),('Kokkola','Keski-Pohjanmaa',63.8391,23.1337),('Kolari','Lappi',67.3303,23.7815),('Konnevesi','Keski-Suomi',62.6267,26.2916),('Kontiolahti','Pohjois-Karjala',62.7667,29.85),('Korsholm','Pohjanmaa',63.1248,21.6941),('Korsnäs','Pohjanmaa',62.7864,21.1878),('Koski Tl','Varsinais-Suomi',60.653,23.1406),('Kotka','Kymenlaakso',60.4674,26.9451),('Kouvola','Kymenlaakso',60.8702,26.7018),('Kristinestad','Pohjanmaa',62.2736,21.3731),('Kronoby','Pohjanmaa',63.7288,23.0215),('Kuhmo','Kainuu',64.1262,29.5195),('Kuhmoinen','Keski-Suomi',61.5667,25.1833),('Kumlinge','Ahvenanmaa',60.2599,20.7786),('Kuopio','Pohjois-Savo',62.8925,27.6782),('Kuortane','Etelä-Pohjanmaa',62.807,23.5069),('Kurikka','Etelä-Pohjanmaa',62.6171,22.3992),('Kustavi','Varsinais-Suomi',60.5458,21.3558),('Kuusamo','Pohjois-Pohjanmaa',65.9646,29.1883),('Kyyjärvi','Keski-Suomi',63.0436,24.5648),('Lahti','Päijät-Häme',60.9839,25.6562),('Laihia','Pohjanmaa',62.9761,22.0122),('Laitila','Varsinais-Suomi',60.8801,21.6926),('Lapinjärvi','Uusimaa',62.9437,28.3908),('Lapinlahti','Pohjois-Savo',60.1676,24.9137),('Lappajärvi','Etelä-Pohjanmaa',63.2193,23.6284),('Lappeenranta','Etelä-Karjala',61.0582,28.1875),('Lapua','Etelä-Pohjanmaa',62.9703,23.0069),('Larsmo','Pohjanmaa',63.8515,22.4879),('Laukaa','Keski-Suomi',62.4167,25.95),('Lemi','Etelä-Karjala',45.2282,7.29204),('Lemland','Ahvenanmaa',60.0557,20.1221),('Lempäälä','Pirkanmaa',61.3167,23.75),('Leppävirta','Pohjois-Savo',62.4894,27.7861),('Lestijärvi','Keski-Pohjanmaa',63.5245,24.6683),('Lieksa','Pohjois-Karjala',63.3178,30.0191),('Lieto','Varsinais-Suomi',60.5022,22.4555),('Liminka','Pohjois-Pohjanmaa',64.8106,25.4085),('Liperi','Pohjois-Karjala',62.5315,29.3872),('Lohja','Uusimaa',60.2526,24.0685),('Loimaa','Varsinais-Suomi',60.8472,23.0514),('Loppi','Kanta-Häme',60.7185,24.4404),('Loviisa','Uusimaa',60.4562,26.2268),('Luhanka','Keski-Suomi',61.797,25.7046),('Lumijoki','Pohjois-Pohjanmaa',64.8384,25.1868),('Lumparland','Ahvenanmaa',60.1169,20.2711),('Luumäki','Etelä-Karjala',60.951,27.5413),('Malax','Pohjanmaa',62.9332,21.5668),('Mäntsälä','Uusimaa',60.6339,25.3188),('Mänttä-Vilppula','Pirkanmaa',62.0826,24.4504),('Mäntyharju','Etelä-Savo',61.4155,26.8797),('Mariehamn','Ahvenanmaa',60.1024,19.9413),('Marttila','Varsinais-Suomi',60.5851,22.8985),('Masku','Varsinais-Suomi',60.5667,22.1),('Merijärvi','Pohjois-Pohjanmaa',64.2926,24.4373),('Merikarvia','Satakunta',61.859,21.5032),('Miehikkälä','Kymenlaakso',60.6692,27.6962),('Mikkeli','Etelä-Savo',61.6878,27.2727),('Muhos','Pohjois-Pohjanmaa',64.8063,25.9954),('Multia','Keski-Suomi',62.41,24.8001),('Muonio','Lappi',67.9593,23.6774),('Muurame','Keski-Suomi',62.129,25.6749),('Mynämäki','Varsinais-Suomi',60.6789,21.9861),('Myrskylä','Uusimaa',60.6703,25.8514),('Naantali','Varsinais-Suomi',60.4689,22.0291),('Nakkila','Satakunta',61.3665,22),('Närpes','Pohjanmaa',62.478,21.3367),('Nivala','Pohjois-Pohjanmaa',63.929,24.9613),('Nokia','Pirkanmaa',61.4766,23.5053),('Nousiainen','Varsinais-Suomi',60.5992,22.0841),('Nurmes','Pohjois-Karjala',63.5422,29.141),('Nurmijärvi','Uusimaa',60.4667,24.8),('Nykarleby','Pohjanmaa',63.5222,22.5284),('Orimattila','Päijät-Häme',60.8051,25.7334),('Oripää','Varsinais-Suomi',60.8556,22.6946),('Orivesi','Pirkanmaa',61.6776,24.3588),('Oulainen','Pohjois-Pohjanmaa',64.2668,24.8),('Oulu','Pohjois-Pohjanmaa',65.0119,25.4717),('Outokumpu','Pohjois-Karjala',62.7255,29.0187),('Padasjoki','Päijät-Häme',61.3513,25.2786),('Paimio','Varsinais-Suomi',60.457,22.6883),('Pälkäne','Pirkanmaa',61.3371,24.2649),('Paltamo','Kainuu',64.4069,27.8336),('Pargas','Varsinais-Suomi',60.3055,22.2996),('Parikkala','Etelä-Karjala',61.5501,29.5),('Parkano','Pirkanmaa',62.0102,23.0246),('Pedersöre','Pohjanmaa',63.5408,23.0452),('Pelkosenniemi','Lappi',67.1096,27.5118),('Pello','Lappi',66.7747,23.9677),('Perho','Keski-Pohjanmaa',63.2144,24.4196),('Pertunmaa','Etelä-Savo',61.5034,26.4784),('Petäjävesi','Keski-Suomi',62.2505,25.2005),('Pieksämäki','Etelä-Savo',62.3005,27.164),('Pielavesi','Pohjois-Savo',63.2333,26.75),('Pihtipudas','Keski-Suomi',63.3706,25.5755),('Pirkkala','Pirkanmaa',61.4655,23.6456),('Polvijärvi','Pohjois-Karjala',62.8545,29.3669),('Pomarkku','Satakunta',61.6935,22.0084),('Pori','Satakunta',61.4866,21.7969),('Pornainen','Uusimaa',60.4756,25.3746),('Porvoo','Uusimaa',60.3954,25.6605),('Posio','Lappi',66.1093,28.1651),('Pöytyä','Varsinais-Suomi',60.7198,22.6041),('Pudasjärvi','Pohjois-Pohjanmaa',65.3604,26.9985),('Pukkila','Uusimaa',60.6456,25.582),('Punkalaidun','Pirkanmaa',61.1158,23.0994),('Puolanka','Kainuu',64.873,27.6553),('Puumala','Etelä-Savo',61.5232,28.1769),('Pyhäjärvi','Pohjois-Pohjanmaa',63.7015,25.9398),('Pyhäjoki','Pohjois-Pohjanmaa',64.4663,24.2551),('Pyhäntä','Pohjois-Pohjanmaa',64.0963,26.3316),('Pyhäranta','Varsinais-Suomi',60.9499,21.4427),('Pyhtää','Kymenlaakso',60.4933,26.5474),('Raahe','Pohjois-Pohjanmaa',64.6797,24.4709),('Rääkkylä','Pohjois-Karjala',62.3143,29.6276),('Raasepori','Uusimaa',59.9279,23.5257),('Raisio','Varsinais-Suomi',60.4881,22.1636),('Rantasalmi','Etelä-Savo',62.0637,28.3045),('Ranua','Lappi',65.9277,26.5131),('Rauma','Satakunta',61.1289,21.5039),('Rautalampi','Pohjois-Savo',62.6207,26.8385),('Rautavaara','Pohjois-Savo',63.494,28.2985),('Rautjärvi','Etelä-Karjala',61.3648,29.209),('Reisjärvi','Pohjois-Pohjanmaa',63.6041,24.9356),('Riihimäki','Kanta-Häme',60.739,24.7728),('Ristijärvi','Kainuu',61.8132,24.6716),('Rovaniemi','Lappi',66.4976,25.7192),('Ruokolahti','Etelä-Karjala',61.2912,28.8295),('Ruovesi','Pirkanmaa',61.9856,24.0703),('Rusko','Varsinais-Suomi',64.6863,97.7453),('Saarijärvi','Keski-Suomi',62.7051,25.2583),('Säkylä','Satakunta',61.0507,22.3337),('Salla','Lappi',66.8319,28.6669),('Salo','Varsinais-Suomi',60.3847,23.1286),('Saltvik','Ahvenanmaa',60.2756,20.0612),('Sastamala','Pirkanmaa',61.45,22.8417),('Sauvo','Varsinais-Suomi',60.3432,22.6949),('Savitaipale','Etelä-Karjala',61.1983,27.6815),('Savonlinna','Etelä-Savo',61.869,28.8797),('Savukoski','Lappi',67.2923,28.1639),('Seinäjoki','Etelä-Pohjanmaa',62.7954,22.8442),('Sievi','Pohjois-Pohjanmaa',63.9083,24.516),('Siikainen','Satakunta',61.8767,21.8217),('Siikajoki','Pohjois-Pohjanmaa',64.7107,24.9813),('Siikalatva','Pohjois-Pohjanmaa',64.3119,26.079),('Siilinjärvi','Pohjois-Savo',63.0743,27.6623),('Simo','Lappi',65.6623,25.0638),('Sipoo','Uusimaa',60.3762,25.2651),('Siuntio','Uusimaa',60.1378,24.2266),('Sodankylä','Lappi',67.419,26.5902),('Soini','Etelä-Pohjanmaa',60.9833,26.25),('Somero','Varsinais-Suomi',60.6299,23.514),('Sonkajärvi','Pohjois-Savo',63.6689,27.5233),('Sotkamo','Kainuu',64.1318,28.3878),('Sottunga','Ahvenanmaa',60.0696,20.8104),('Sulkava','Etelä-Savo',61.7873,28.3713),('Sund','Ahvenanmaa',55.7866,12.7174),('Suomussalmi','Kainuu',64.8848,28.9146),('Suonenjoki','Pohjois-Savo',62.6242,27.1246),('Sysmä','Päijät-Häme',61.5074,25.6739),('Taipalsaari','Etelä-Karjala',61.1612,28.06),('Taivalkoski','Pohjois-Pohjanmaa',65.5753,28.2426),('Taivassalo','Varsinais-Suomi',60.563,21.6127),('Tammela','Kanta-Häme',60.8088,23.7598),('Tampere','Pirkanmaa',61.498,23.7603),('Tervo','Pohjois-Savo',62.9564,26.7605),('Tervola','Lappi',66.0823,24.8059),('Teuva','Etelä-Pohjanmaa',62.4869,21.742),('Tohmajärvi','Pohjois-Karjala',62.2259,30.3336),('Toholampi','Keski-Pohjanmaa',63.7726,24.2515),('Toivakka','Keski-Suomi',62.0962,26.0805),('Tornio','Lappi',65.8458,24.1464),('Turku','Varsinais-Suomi',60.4518,22.2671),('Tuusniemi','Pohjois-Savo',62.813,28.474),('Tuusula','Uusimaa',60.4017,25.0281),('Tyrnävä','Pohjois-Pohjanmaa',64.7621,25.6499),('Ulvila','Satakunta',61.4333,21.8833),('Urjala','Pirkanmaa',61.0812,23.549),('Utajärvi','Pohjois-Pohjanmaa',64.7619,26.417),('Utsjoki','Lappi',69.9076,27.0255),('Uurainen','Keski-Suomi',62.5008,25.438),('Uusikaupunki','Varsinais-Suomi',60.8017,21.4086),('Vaala','Pohjois-Pohjanmaa',64.5565,26.8467),('Vaasa','Pohjanmaa',63.0958,21.6159),('Valkeakoski','Pirkanmaa',61.2638,24.0301),('Vantaa','Uusimaa',60.3092,25.0365),('Vårdö','Ahvenanmaa',43.9599,4.29764),('Varkaus','Pohjois-Savo',62.3176,27.8681),('Vehmaa','Varsinais-Suomi',60.6844,21.6967),('Vesanto','Pohjois-Savo',62.9303,26.4089),('Vesilahti','Pirkanmaa',61.297,23.6388),('Veteli','Keski-Pohjanmaa',63.4719,23.7926),('Vieremä','Pohjois-Savo',63.75,27.0167),('Vihti','Uusimaa',-18.124,179.012),('Viitasaari','Keski-Suomi',63.0837,25.8528),('Vimpeli','Etelä-Pohjanmaa',63.1615,23.8178),('Virolahti','Kymenlaakso',60.4994,27.5838),('Virrat','Pirkanmaa',62.2402,23.7726),('Vöyri','Pohjanmaa',63.1305,22.2507),('Ylitornio','Lappi',66.3164,23.6713),('Ylivieska','Pohjois-Pohjanmaa',64.0729,24.5327),('Ylöjärvi','Pirkanmaa',61.55,23.5969),('Ypäjä','Kanta-Häme',60.8038,23.2821);
/*!40000 ALTER TABLE `munic` ENABLE KEYS */;
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