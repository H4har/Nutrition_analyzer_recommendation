-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 22, 2024 at 04:49 PM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `python_nutricion_analyzer_recommendation`
--

-- --------------------------------------------------------

--
-- Table structure for table `self_assessment_question`
--

CREATE TABLE `self_assessment_question` (
  `id` int(100) NOT NULL,
  `question` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `report` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `self_assessment_question`
--


-- --------------------------------------------------------

--
-- Table structure for table `user_details`
--

CREATE TABLE `user_details` (
  `id` int(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `contact` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `address` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `bmi` varchar(100) NOT NULL,
  `bmi_type` varchar(100) NOT NULL,
  `height` varchar(100) NOT NULL,
  `weight` varchar(100) NOT NULL,
  `tomorrow_possible` varchar(100) NOT NULL,
  `fat` varchar(100) NOT NULL,
  `fat_count` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user_details`
--


-- --------------------------------------------------------

--
-- Table structure for table `user_self_assessment`
--

CREATE TABLE `user_self_assessment` (
  `id` int(100) NOT NULL,
  `username` varchar(100) NOT NULL,
  `qid` varchar(100) NOT NULL,
  `question` varchar(100) NOT NULL,
  `answer` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `report` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user_self_assessment`
--

