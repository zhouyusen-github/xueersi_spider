全部default null这样以后处理意外方便
#城市数据库
CREATE TABLE `citys` (
   `order_id` int UNSIGNED AUTO_INCREMENT,
   `id` varchar(32) DEFAULT NULL,
   `name` varchar(32) DEFAULT NULL,
   `area` varchar(32) DEFAULT NULL,
   `pinyin` varchar(32) DEFAULT NULL,
   `local_city` varchar(32) DEFAULT NULL,
   `snapshot_time` DATETIME DEFAULT NULL,
   PRIMARY KEY (`order_id`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8

都32反正这个数据库无所谓

#年级数据库
CREATE TABLE `grades` (
   `order_id` int UNSIGNED AUTO_INCREMENT,
   `name` varchar(32) DEFAULT NULL,
   `areaCode` varchar(32) DEFAULT NULL,
   `grd_id` varchar(32) DEFAULT NULL,
   `grd_name` varchar(32) DEFAULT NULL,
   `cla_gt_id` varchar(32) DEFAULT NULL,
   `cla_gt_name` varchar(32) DEFAULT NULL,
   `snapshot_time` DATETIME DEFAULT NULL,
   PRIMARY KEY (`order_id`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8

#课程条目数数据库
CREATE TABLE `courses_totalCount` (
   `order_id` int UNSIGNED AUTO_INCREMENT,
   `name` varchar(32) DEFAULT NULL,
   `areaCode` varchar(32) DEFAULT NULL,
   `grd_id` varchar(32) DEFAULT NULL,
   `grd_name` varchar(32) DEFAULT NULL,
   `status` varchar(32) DEFAULT NULL,
   `code` varchar(32) DEFAULT NULL,
   `msg` varchar(32) DEFAULT NULL,
   `totalCount` int DEFAULT NULL,
   `snapshot_time` DATETIME DEFAULT NULL,
   PRIMARY KEY (`order_id`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8



#课程详细数据库
CREATE TABLE `courses_test1` (
    `id` int UNSIGNED AUTO_INCREMENT,
    `cityName` varchar(32) DEFAULT NULL,
    `cityCode` varchar(32) DEFAULT NULL,
    `gradeName` varchar(32) DEFAULT NULL,
    `gradeId` varchar(32) DEFAULT NULL,


    `class_id` varchar(40) DEFAULT NULL,
    `class_name` varchar(60) DEFAULT NULL,
    `course_id` varchar(40) DEFAULT NULL,
    `class_type` int DEFAULT NULL,
    `start_date` date DEFAULT NULL,
    `end_date` date DEFAULT NULL,
    `classtimeNames` varchar(80) DEFAULT NULL,
    `reg_num` int DEFAULT NULL,
    `area_name` varchar(20) DEFAULT NULL,
    `servicecenterName` varchar(32) DEFAULT NULL,
    `teacher_emp_no` varchar(16) DEFAULT NULL,
    `teacher_id` varchar(50) DEFAULT NULL,
    `teacher_name` varchar(30) DEFAULT NULL,
    `tutor_emp_no` varchar(16) DEFAULT NULL,
    `tutor_id` varchar(50) DEFAULT NULL,
    `tutor_sys_name` varchar(30) DEFAULT NULL,

    `business_type` int DEFAULT NULL,
    `max_persons` int DEFAULT NULL,
    `surplus_persons` int DEFAULT NULL,
    `class_count` int DEFAULT NULL,

    `venue_name` varchar(40) DEFAULT NULL,
    `price` int DEFAULT NULL,
    `fee_type` int DEFAULT NULL,
    `classroom_name` varchar(32) DEFAULT NULL,
    `biz_type` int DEFAULT NULL,
    `cla_quota_num` varchar(8) DEFAULT NULL,
    `cla_quota_state` int DEFAULT NULL,
    `course_reg_num` int DEFAULT NULL,
    `class_resist_state` int DEFAULT NULL,
    `class_resist_state_num` int DEFAULT NULL,
    `district_id` varchar(30) DEFAULT NULL,
    `district_name` varchar(16) DEFAULT NULL,
    `subject_id` varchar(64) DEFAULT NULL,
    `subject_name` varchar(16) DEFAULT NULL,
    `level_name` varchar(32) DEFAULT NULL,
    `snapshot_time` DATETIME DEFAULT NULL,
    PRIMARY KEY (`id`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8