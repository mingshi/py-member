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

create table department (
    `id` int not null auto_increment,
    `name` varchar(50) not null default '' comment '部门名称',
    PRIMARY KEY (`id`)
) engine=innodb default charset utf8;

create table position (
    `id` int not null auto_increment,
    `name` varchar(50) not null default '' comment '职位名称',
    `did` int not null default '0' comment '所属部门id',
    PRIMARY KEY (`id`),
    KEY `did` (`did`)
) engine=innodb default charset utf8;

alter table user add is_admin tinyint(1) NOT NULL DEFAULT '0' COMMENT 'is admin';
alter table user add position int(10) NOT NULL DEFAULT '0' COMMENT '职位id';
alter table user add department int(10) NOT NULL DEFAULT '0' COMMENT '部门id';

alter table user add is_default_pass tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否初始密码1:是,0:否';

alter table user add qq varchar(20) NOT null DEFAULT '' comment '用户qq';


#2014-03-14
alter table user add `higher` int(10) NOT NULL DEFAULT '0' COMMENT '用户的上级uid';
