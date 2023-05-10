CREATE TABLE IF NOT EXISTS `prefecture` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `prefecturecode` char(2) NOT NULL,
  `prefecturename` varchar(8) NOT NULL,
  `blockname` varchar(8) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `prefecturecode` (`prefecturecode`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;