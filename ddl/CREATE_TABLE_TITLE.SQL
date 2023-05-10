CREATE TABLE IF NOT EXISTS `title` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titledivcode` char(1) NOT NULL,
  `titledivname` varchar(8) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `titledivcode` (`titledivcode`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;