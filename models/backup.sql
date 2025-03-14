-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: varsity_applicants
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `varsity_applicants`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `varsity_applicants` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `varsity_applicants`;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('d1a00375bfb7');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `documents`
--

DROP TABLE IF EXISTS `documents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `documents` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `id_document` varchar(255) DEFAULT NULL,
  `results_documents` varchar(255) DEFAULT NULL,
  `proof_of_payment` varchar(255) DEFAULT NULL,
  `id_document_parent` varchar(255) DEFAULT NULL,
  `proof_of_res` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `documents_ibfk_1` (`user_id`),
  CONSTRAINT `documents_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documents`
--

LOCK TABLES `documents` WRITE;
/*!40000 ALTER TABLE `documents` DISABLE KEYS */;
INSERT INTO `documents` VALUES (28,144,'static/MAT1501_Assessment_2.pdf','static/MAT1501_Assessment_2.pdf','static/MAT1501_Assessment_2.pdf','static/MAT1501_Assessment_2.pdf','static/MAT1501_Assessment_2.pdf'),(29,145,'static/MAT1501_Assessment_2.pdf','static/Business-Computers_365.pdf','static/PHY1507-25-Y_tutorial_letter.pdf','static/Introductory_Physics_APHY1507_1_2025_1.pdf','static/101_2025_0_b.pdf');
/*!40000 ALTER TABLE `documents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `message` text,
  `file_path` varchar(255) DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (1,'hy','static/MAT1501_Assessment_2.pdf',144,'2025-03-13 18:54:51'),(2,'Hy',NULL,145,'2025-03-13 18:54:51'),(3,'Please Submit all your documents',NULL,145,'2025-03-13 18:54:51'),(4,'','static/Introductory_Physics_APHY1507_1_2025_1.pdf',145,'2025-03-13 18:54:51'),(5,'','static/Screenshot_2025-03-12_120835.png',145,'2025-03-13 18:54:51'),(6,'Good night','static/101_2025_0_b.pdf',145,'2025-03-14 18:17:36'),(7,'Good ny buddy','static/MAT1501_Assessment_2.pdf',145,'2025-03-14 18:27:26');
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staff` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(80) NOT NULL,
  `password` varchar(120) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff`
--

LOCK TABLES `staff` WRITE;
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
INSERT INTO `staff` VALUES (1,'vutlharimathebula74@gmail.com','ca9a74caa11e55bdae025fb3dffa34201e6201b7324acb3dbcdff2543337e08b'),(2,'vukonamanganye444@gmail.com','855f1b9ef7d870552b12093b39d0f8c623886be8ecc06f3be6b95646f5b4bd3d');
/*!40000 ALTER TABLE `staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(120) DEFAULT NULL,
  `second_name` varchar(120) DEFAULT NULL,
  `surname` varchar(120) DEFAULT NULL,
  `email` varchar(120) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `applicantTitle` varchar(10) DEFAULT NULL,
  `idNumber` varchar(20) DEFAULT NULL,
  `postalCode` varchar(20) DEFAULT NULL,
  `province` varchar(50) DEFAULT NULL,
  `homeLanguage` varchar(50) DEFAULT NULL,
  `matricYear` varchar(20) DEFAULT NULL,
  `upgrading` varchar(20) DEFAULT NULL,
  `nsfasBursary` varchar(20) DEFAULT NULL,
  `bday` date DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `school` varchar(255) DEFAULT NULL,
  `nextName` varchar(120) DEFAULT NULL,
  `nextsName` varchar(120) DEFAULT NULL,
  `nextsurName` varchar(50) DEFAULT NULL,
  `nesTitle` varchar(10) DEFAULT NULL,
  `nextIdNumber` varchar(20) DEFAULT NULL,
  `nextPhone` varchar(20) DEFAULT NULL,
  `nextGender` varchar(10) DEFAULT NULL,
  `nextEmail` varchar(120) DEFAULT NULL,
  `nextBday` date DEFAULT NULL,
  `nextAddress` varchar(255) DEFAULT NULL,
  `nextPostalCode` varchar(20) DEFAULT NULL,
  `whatsapp_number` varchar(20) DEFAULT NULL,
  `username` varchar(80) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `selected_institutions` text,
  `institutions` varchar(255) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=146 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (144,'Vutlhari','Coder','Mathebula','vutlharimathebu@gmail.com','0795186497','Male','Mr','0507165568084','0930','Gauteng','Xitsonga','2025','YES','YES','2005-07-16','VONGANI, VONGANI','Akani High School','John','Smith','Mooke','Mr','8805015568081','0714586555','Male','bsd@gmail.com','1988-05-01','Giyani main road','0826','0633979570','Coding@gmail.com','scrypt:32768:8:1$Anq2PsrQbqqkwM1V$46086d574b86cba84364173ed011af2f55fa7f94580c582b2e871a20f760dd041c752fd466263e43eb022e8fc714a59c55d91d4cbbe96de59ada803516adc537','University of Limpopo,Tshwane University of Technology,Stellenbosch University,Boland TVET College',NULL,'2025-03-13 09:34:40','2025-03-13 09:34:40'),(145,'Vutlhari','Coder','Mathebula','vutlhari74@gmail.com','0795186497','Male','Mr','0507165568084','0930','Gauteng','English','2025','YES','YES','2000-02-08','VONGANI, VONGANI','Akani High School','King','vutlhari','mathebula','Mr','0507165568084','0712258845','Male','vutlhari@gmail.com','2000-12-07','123 Avenue Street','0930','0633979570','Password1@gmail.com','scrypt:32768:8:1$mZYgdxbU6sqLlu3Q$f430d208a674b98ae7e29993fb4b57b12ed0d692fce96fece0d1209a23655a7ce12b838536ab89e1751086a615323ddd1fd50e3b2565bf5136a8a1ab666ef482','University of Limpopo,Tshwane University of Technology,University of Cape Town,Stellenbosch University',NULL,'2025-03-13 16:52:53','2025-03-13 16:52:53');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-14 23:39:55
