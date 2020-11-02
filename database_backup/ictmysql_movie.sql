-- MySQL dump 10.13  Distrib 8.0.21, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: ictmysql
-- ------------------------------------------------------
-- Server version	8.0.21

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `movie`
--

DROP TABLE IF EXISTS `movie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movie` (
  `movie_id` int NOT NULL AUTO_INCREMENT,
  `ratings` decimal(3,2) DEFAULT NULL,
  `genre` varchar(100) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `director_id` int DEFAULT NULL,
  `run_time` int DEFAULT NULL,
  `poster_path` varchar(250) DEFAULT NULL,
  `plot` varchar(2500) DEFAULT NULL,
  `title` varchar(150) DEFAULT NULL,
  `overview` varchar(2500) DEFAULT NULL,
  `original_language` varchar(25) DEFAULT NULL,
  `writers` varchar(1000) DEFAULT NULL,
  `casts` varchar(1000) DEFAULT NULL,
  `release_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`movie_id`),
  UNIQUE KEY `UC_Movie` (`title`,`poster_path`,`release_date`),
  KEY `director_id` (`director_id`),
  CONSTRAINT `movie_ibfk_1` FOREIGN KEY (`director_id`) REFERENCES `director` (`director_id`),
  CONSTRAINT `movie_chk_1` CHECK (((`ratings` > 0) and (`ratings` <= 5)))
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movie`
--

LOCK TABLES `movie` WRITE;
/*!40000 ALTER TABLE `movie` DISABLE KEYS */;
INSERT INTO `movie` VALUES (1,4.00,NULL,NULL,NULL,93,'https://m.media-amazon.com/images/M/MV5BYjE2MjIwMmYtM2ZiMy00MzdmLTkyNTYtNmFiNjM5MDJhMGVmXkEyXkFqcGdeQXVyODk4OTc3MTY@._V1_SX300.jpg','A reformed hunter living in isolation on a wildlife sanctuary becomes involved in a deadly game of cat and mouse when he and the local Sheriff set out to track a vicious killer who may have kidnapped his daughter years ago.','The Silencing',NULL,NULL,NULL,NULL,'2020-07-18 00:00:00'),(2,4.00,NULL,NULL,NULL,99,'https://m.media-amazon.com/images/M/MV5BZjEwNjYyMTMtODc5Yi00NTg5LTkwMzAtZTkyOTcyNTFkMGIyXkEyXkFqcGdeQXVyMDA4NzMyOA@@._V1_SX300.jpg','Wanting to lead an honest life, a notorious bank robber turns himself in, only to be double-crossed by two ruthless FBI agents.','Honest Thief',NULL,NULL,NULL,NULL,'2020-10-16 00:00:00'),(3,4.00,NULL,NULL,NULL,137,'https://m.media-amazon.com/images/M/MV5BNWQyMzA3NDItMDRhZi00MWUxLTgyYmYtM2I1NTI3ZTE2NjY5XkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_SX300.jpg','On the trail of a missing girl, an ex-cop comes across a secretive group attempting to summon a terrifying supernatural entity.','The Empty Man',NULL,NULL,NULL,NULL,'2020-10-23 00:00:00'),(4,4.00,NULL,NULL,NULL,94,'https://m.media-amazon.com/images/M/MV5BNTlkZDQ1ODEtY2ZiMS00OGNhLWJlZDctYzY0NTFmNmQ2NDAzXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_SX300.jpg','Upset that he has to share the room he loves with his grandfather, Peter decides to declare war in an attempt to get it back.','The War with Grandpa',NULL,NULL,NULL,NULL,'2020-10-09 00:00:00'),(5,4.00,NULL,NULL,NULL,135,'https://m.media-amazon.com/images/M/MV5BM2MzZDA1NDMtYTk5Mi00M2M3LTk0MDctOGI0ODI0ZGFjNzQ4XkEyXkFqcGdeQXVyMTAwMDE3MjM1._V1_SX300.jpg','After 12 years, the Chinese women\'s volleyball team again reached the Olympic final. The ups and downs of the Chinese women\'s volleyball team for more than three decades have slowly spread away.','Leap',NULL,NULL,NULL,NULL,'2020-09-25 00:00:00'),(6,4.00,NULL,NULL,NULL,108,'https://m.media-amazon.com/images/M/MV5BODNjY2ZlZDMtYzMwZS00NTRlLWIzM2ItYTY3YmE1Njc1ODM4XkEyXkFqcGdeQXVyNDM1Nzc0MTI@._V1_SX300.jpg','Covert security company Vanguard is the last hope of survival for an accountant after he is targeted by the world\'s deadliest mercenary organization.','Vanguard',NULL,NULL,NULL,NULL,'2020-09-30 00:00:00'),(7,4.00,NULL,NULL,NULL,92,'https://m.media-amazon.com/images/M/MV5BNTRhNjQxYmYtNDkzNS00MDhlLWE2ODQtNmJiNzQzNTJjZDVmXkEyXkFqcGdeQXVyNzEzNjU1NDg@._V1_SX300.jpg','After apparent death, Siena is able to see signs that people will die. However, her friends did not believe in her abilities. Then, the sign appeared on her and those closest to her.','Aku Tahu Kapan Kamu Mati',NULL,NULL,NULL,NULL,'2020-03-05 00:00:00'),(8,4.00,NULL,NULL,NULL,150,'https://m.media-amazon.com/images/M/MV5BYzg0NGM2NjAtNmIxOC00MDJmLTg5ZmYtYzM0MTE4NWE2NzlhXkEyXkFqcGdeQXVyMTA4NjE0NjEy._V1_SX300.jpg','Armed with only one word, Tenet, and fighting for the survival of the entire world, a Protagonist journeys through a twilight world of international espionage on a mission that will unfold in something beyond real time.','Tenet',NULL,NULL,NULL,NULL,'2020-09-03 00:00:00'),(9,4.00,NULL,NULL,NULL,108,'https://m.media-amazon.com/images/M/MV5BZTgyOWUyYTctMjQxNy00MDQ5LWFlMDQtODY2ZGEzYjIyYzRmXkEyXkFqcGdeQXVyMjg0MTI5NzQ@._V1_SX300.jpg','Hearing-impaired teenager Chang Cheng transfers to a school for children with special needs. However, the world of the hearing-impaired doesn\'t seem quiet at all. When Chang witnesses the \"...','The Silent Forest',NULL,NULL,NULL,NULL,'2020-06-25 00:00:00'),(10,4.00,NULL,NULL,NULL,101,'https://m.media-amazon.com/images/M/MV5BMTRkYmJlY2ItNmFlZi00OWVhLTg1ZTctOGE0MjM5ZGMwMmY4XkEyXkFqcGdeQXVyNjY1MTg4Mzc@._V1_SX300.jpg','After swapping bodies with a deranged serial killer, a young girl in high school discovers she has less than 24 hours before the change becomes permanent.','Freaky',NULL,NULL,NULL,NULL,'2020-11-13 00:00:00'),(11,4.00,NULL,NULL,NULL,119,'https://m.media-amazon.com/images/M/MV5BOTk2Yzg5MmEtNDhhYy00OGZlLWJiYTctN2M3Yjc0NTc3NjUwXkEyXkFqcGdeQXVyOTI1MTg4MzA@._V1_SX300.jpg','N/A','My Missing Valentine',NULL,NULL,NULL,NULL,'2020-09-18 00:00:00'),(12,4.00,NULL,NULL,NULL,151,'https://m.media-amazon.com/images/M/MV5BZGVhZDBlZjgtMGNmNi00OTIyLWI1NzQtMzE5ZWQ0NzFmMjg0XkEyXkFqcGdeQXVyMTA2OTQ3MTUy._V1_SX300.jpg','Fast forward to the 1980s as Wonder Woman\'s next big screen adventure finds her facing two all-new foes: Max Lord and The Cheetah.','Wonder Woman 1984',NULL,NULL,NULL,NULL,'2020-12-25 00:00:00'),(13,4.00,NULL,NULL,NULL,113,'https://m.media-amazon.com/images/M/MV5BOTgzMzE4MGItZDgxYS00ZGEwLWE3YTctZWY3ZDAyMTk0ZGU4XkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_SX300.jpg','A young woman, traumatized by a tragic event in her past, seeks out vengeance against those who cross her path.','Promising Young Woman',NULL,NULL,NULL,NULL,'2020-12-25 00:00:00'),(14,4.00,NULL,NULL,NULL,93,'https://m.media-amazon.com/images/M/MV5BNTQwOThjZTEtNDNhZS00YmYzLWFkNWMtNWRjN2RmOWI5ZmU1XkEyXkFqcGdeQXVyODk4OTc3MTY@._V1_SX300.jpg','Thomas and Bea are now married and living with Peter and his rabbit family. Bored of life in the garden, Peter goes to the big city, where he meets shady characters and ends up creating chaos for the whole family.','Peter Rabbit 2: The Runaway',NULL,NULL,NULL,NULL,'2021-01-15 00:00:00');
/*!40000 ALTER TABLE `movie` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-11-02 22:41:27
