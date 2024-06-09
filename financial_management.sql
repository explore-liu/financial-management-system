/*
 Navicat Premium Data Transfer

 Source Server         : mysql
 Source Server Type    : MySQL
 Source Server Version : 80026
 Source Host           : localhost:3306
 Source Schema         : financial_management

 Target Server Type    : MySQL
 Target Server Version : 80026
 File Encoding         : 65001

 Date: 09/06/2024 20:43:08
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for permission
-- ----------------------------
DROP TABLE IF EXISTS `permission`;
CREATE TABLE `permission`  (
  `p_no` int NOT NULL AUTO_INCREMENT,
  `p_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`p_no`) USING BTREE,
  INDEX `p_name`(`p_name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of permission
-- ----------------------------
INSERT INTO `permission` VALUES (2, '更改薪资等级');
INSERT INTO `permission` VALUES (3, '更改身份');
INSERT INTO `permission` VALUES (1, '查看');

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role`  (
  `r_no` int NOT NULL AUTO_INCREMENT,
  `r_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`r_no`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of role
-- ----------------------------
INSERT INTO `role` VALUES (1, 'employee');
INSERT INTO `role` VALUES (2, 'financial_staff');
INSERT INTO `role` VALUES (3, 'admin');

-- ----------------------------
-- Table structure for role_permission
-- ----------------------------
DROP TABLE IF EXISTS `role_permission`;
CREATE TABLE `role_permission`  (
  `r_no` int NOT NULL,
  `p_no` int NOT NULL,
  PRIMARY KEY (`r_no`, `p_no`) USING BTREE,
  INDEX `foreign_rp_p_no`(`p_no` ASC) USING BTREE,
  CONSTRAINT `foreign_rp_p_no` FOREIGN KEY (`p_no`) REFERENCES `permission` (`p_no`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `foreign_rp_r_no` FOREIGN KEY (`r_no`) REFERENCES `role` (`r_no`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of role_permission
-- ----------------------------
INSERT INTO `role_permission` VALUES (1, 1);
INSERT INTO `role_permission` VALUES (2, 1);
INSERT INTO `role_permission` VALUES (3, 1);
INSERT INTO `role_permission` VALUES (2, 2);
INSERT INTO `role_permission` VALUES (3, 3);

-- ----------------------------
-- Table structure for scale
-- ----------------------------
DROP TABLE IF EXISTS `scale`;
CREATE TABLE `scale`  (
  `scale_no` int NOT NULL AUTO_INCREMENT,
  `scale_salary` decimal(10, 2) NOT NULL,
  PRIMARY KEY (`scale_no`) USING BTREE,
  CONSTRAINT `check_scale_salary` CHECK (`scale_salary` >= 0)
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of scale
-- ----------------------------
INSERT INTO `scale` VALUES (1, 100000.00);
INSERT INTO `scale` VALUES (2, 80000.00);
INSERT INTO `scale` VALUES (3, 70000.00);
INSERT INTO `scale` VALUES (4, 60000.00);
INSERT INTO `scale` VALUES (5, 40000.00);
INSERT INTO `scale` VALUES (6, 25000.00);
INSERT INTO `scale` VALUES (7, 20000.00);
INSERT INTO `scale` VALUES (8, 10000.00);
INSERT INTO `scale` VALUES (9, 8000.00);
INSERT INTO `scale` VALUES (10, 5000.00);

-- ----------------------------
-- Table structure for staff
-- ----------------------------
DROP TABLE IF EXISTS `staff`;
CREATE TABLE `staff`  (
  `s_no` char(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `s_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `s_sex` enum('男','女') CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `s_entryYear` year NOT NULL,
  PRIMARY KEY (`s_no`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of staff
-- ----------------------------
INSERT INTO `staff` VALUES ('2014000019', '吕廿一', '男', 2014);
INSERT INTO `staff` VALUES ('2016000015', '朱十七', '男', 2016);
INSERT INTO `staff` VALUES ('2017000034', '潘卅六', '女', 2017);
INSERT INTO `staff` VALUES ('2018000031', '熊卅三', '男', 2018);
INSERT INTO `staff` VALUES ('2018000032', '金卅四', '女', 2018);
INSERT INTO `staff` VALUES ('2019000009', '陈十一', '男', 2019);
INSERT INTO `staff` VALUES ('2019000010', '卫十二', '女', 2019);
INSERT INTO `staff` VALUES ('2020000028', '邹三十', '女', 2020);
INSERT INTO `staff` VALUES ('2021000005', '孙七', '男', 2021);
INSERT INTO `staff` VALUES ('2022000004', '赵六', '女', 2022);
INSERT INTO `staff` VALUES ('2022000024', '罗廿六', '女', 2022);
INSERT INTO `staff` VALUES ('2023000001', '张三', '男', 2023);
INSERT INTO `staff` VALUES ('2023000002', '李四', '女', 2023);
INSERT INTO `staff` VALUES ('2023000021', '陆廿三', '男', 2023);
INSERT INTO `staff` VALUES ('2023000022', '肖廿四', '女', 2023);

-- ----------------------------
-- Table structure for staff_scale
-- ----------------------------
DROP TABLE IF EXISTS `staff_scale`;
CREATE TABLE `staff_scale`  (
  `s_no` char(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `scale_no` int NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`s_no`, `scale_no`) USING BTREE,
  INDEX `foreign_ss_scale_no`(`scale_no` ASC) USING BTREE,
  CONSTRAINT `foreign_ss_s_no` FOREIGN KEY (`s_no`) REFERENCES `staff` (`s_no`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `foreign_ss_scale_no` FOREIGN KEY (`scale_no`) REFERENCES `scale` (`scale_no`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of staff_scale
-- ----------------------------
INSERT INTO `staff_scale` VALUES ('2014000019', 1, '2021-07-01');
INSERT INTO `staff_scale` VALUES ('2014000019', 2, '2019-03-24');
INSERT INTO `staff_scale` VALUES ('2014000019', 3, '2017-12-15');
INSERT INTO `staff_scale` VALUES ('2014000019', 4, '2015-09-01');
INSERT INTO `staff_scale` VALUES ('2014000019', 5, '2014-04-17');
INSERT INTO `staff_scale` VALUES ('2016000015', 3, '2022-06-07');
INSERT INTO `staff_scale` VALUES ('2016000015', 4, '2021-04-30');
INSERT INTO `staff_scale` VALUES ('2016000015', 5, '2019-10-15');
INSERT INTO `staff_scale` VALUES ('2016000015', 6, '2018-02-08');
INSERT INTO `staff_scale` VALUES ('2016000015', 7, '2016-11-11');
INSERT INTO `staff_scale` VALUES ('2017000034', 3, '2023-09-09');
INSERT INTO `staff_scale` VALUES ('2017000034', 4, '2022-01-08');
INSERT INTO `staff_scale` VALUES ('2017000034', 5, '2020-05-01');
INSERT INTO `staff_scale` VALUES ('2017000034', 7, '2018-10-10');
INSERT INTO `staff_scale` VALUES ('2017000034', 8, '2017-03-14');
INSERT INTO `staff_scale` VALUES ('2018000031', 4, '2023-12-08');
INSERT INTO `staff_scale` VALUES ('2018000031', 5, '2022-02-22');
INSERT INTO `staff_scale` VALUES ('2018000031', 6, '2021-10-03');
INSERT INTO `staff_scale` VALUES ('2018000031', 7, '2020-03-10');
INSERT INTO `staff_scale` VALUES ('2018000031', 8, '2018-02-25');
INSERT INTO `staff_scale` VALUES ('2018000032', 5, '2023-04-12');
INSERT INTO `staff_scale` VALUES ('2018000032', 6, '2021-11-28');
INSERT INTO `staff_scale` VALUES ('2018000032', 7, '2020-07-18');
INSERT INTO `staff_scale` VALUES ('2018000032', 8, '2018-12-06');
INSERT INTO `staff_scale` VALUES ('2019000009', 6, '2022-08-01');
INSERT INTO `staff_scale` VALUES ('2019000009', 8, '2020-12-08');
INSERT INTO `staff_scale` VALUES ('2019000009', 9, '2019-10-15');
INSERT INTO `staff_scale` VALUES ('2019000010', 6, '2022-10-01');
INSERT INTO `staff_scale` VALUES ('2019000010', 7, '2021-07-23');
INSERT INTO `staff_scale` VALUES ('2019000010', 8, '2020-05-05');
INSERT INTO `staff_scale` VALUES ('2019000010', 9, '2019-11-30');
INSERT INTO `staff_scale` VALUES ('2020000028', 6, '2023-01-05');
INSERT INTO `staff_scale` VALUES ('2020000028', 7, '2021-10-07');
INSERT INTO `staff_scale` VALUES ('2020000028', 8, '2020-04-05');
INSERT INTO `staff_scale` VALUES ('2021000005', 6, '2023-06-23');
INSERT INTO `staff_scale` VALUES ('2021000005', 8, '2021-12-14');
INSERT INTO `staff_scale` VALUES ('2021000005', 9, '2021-02-03');
INSERT INTO `staff_scale` VALUES ('2022000024', 8, '2023-12-10');
INSERT INTO `staff_scale` VALUES ('2022000024', 9, '2023-02-02');
INSERT INTO `staff_scale` VALUES ('2022000024', 10, '2022-04-19');
INSERT INTO `staff_scale` VALUES ('2023000001', 9, '2023-10-17');
INSERT INTO `staff_scale` VALUES ('2023000001', 10, '2023-03-12');
INSERT INTO `staff_scale` VALUES ('2023000002', 9, '2023-05-28');
INSERT INTO `staff_scale` VALUES ('2023000021', 10, '2023-07-15');
INSERT INTO `staff_scale` VALUES ('2023000022', 10, '2023-08-26');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `u_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `u_password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `u_email` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `u_phoneNumber` char(11) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `s_no` char(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `r_no` int NOT NULL DEFAULT 1,
  PRIMARY KEY (`u_name`) USING BTREE,
  UNIQUE INDEX `s_no`(`s_no` ASC) USING BTREE,
  INDEX `foreign_user_r_no`(`r_no` ASC) USING BTREE,
  CONSTRAINT `foreign_user_r_no` FOREIGN KEY (`r_no`) REFERENCES `role` (`r_no`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `foreign_user_s_no` FOREIGN KEY (`s_no`) REFERENCES `staff` (`s_no`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('abc', '123456', NULL, NULL, '2023000001', 1);
INSERT INTO `user` VALUES ('admin', '123456', NULL, NULL, '2014000019', 3);
INSERT INTO `user` VALUES ('financial', '123456', NULL, NULL, '2017000034', 2);

-- ----------------------------
-- View structure for staff_latest_scale_view
-- ----------------------------
DROP VIEW IF EXISTS `staff_latest_scale_view`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `staff_latest_scale_view` AS with `rankeddates` as (select `staff_scale`.`s_no` AS `s_no`,`staff_scale`.`scale_no` AS `scale_no`,`staff_scale`.`date` AS `date`,row_number() OVER (PARTITION BY `staff_scale`.`s_no` ORDER BY `staff_scale`.`date` desc )  AS `rn` from `staff_scale`) select `temp`.`s_no` AS `s_no`,`staff`.`s_name` AS `s_name`,`staff`.`s_sex` AS `s_sex`,`staff`.`s_entryYear` AS `s_entryYear`,`scale`.`scale_no` AS `scale_no`,`scale`.`scale_salary` AS `scale_salary` from ((`scale` join (select `rankeddates`.`s_no` AS `s_no`,`rankeddates`.`scale_no` AS `scale_no`,`rankeddates`.`date` AS `date` from `rankeddates` where (`rankeddates`.`rn` = 1)) `temp` on((`scale`.`scale_no` = `temp`.`scale_no`))) join `staff` on((`temp`.`s_no` = `staff`.`s_no`)));

-- ----------------------------
-- View structure for user_info_admin_view
-- ----------------------------
DROP VIEW IF EXISTS `user_info_admin_view`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `user_info_admin_view` AS select `user`.`u_name` AS `u_name`,`user`.`s_no` AS `s_no`,`user`.`r_no` AS `r_no` from `user`;

SET FOREIGN_KEY_CHECKS = 1;
