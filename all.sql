create table user (
    `id` int not null auto_increment,
    `username` varchar(50) not null default '' comment '用户名',
    `realname` varchar(50) NOT NULL DEFAULT '',
    `password` char(32) NOT NULL,
    `mobile` varchar(20) NOT NULL DEFAULT '',
    `email` varchar(50) NOT NULL DEFAULT '',
    `status` tinyint(4) NOT NULL DEFAULT '1',
    `login_time` timestamp NULL DEFAULT NULL,
    `login_ip` varchar(50) DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `username` (`username`)
) engine=innodb default charset utf8;
