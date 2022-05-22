/*
 Navicat Premium Data Transfer

 Source Server         : mysql_database
 Source Server Type    : MySQL
 Source Server Version : 80024
 Source Host           : localhost:3306
 Source Schema         : blog

 Target Server Type    : MySQL
 Target Server Version : 80024
 File Encoding         : 65001

 Date: 30/05/2021 17:37:25
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for credit
-- ----------------------------
DROP TABLE IF EXISTS `credit`;
CREATE TABLE `credit`  (
  `creditid` int(0) NOT NULL AUTO_INCREMENT COMMENT '积分表唯一编号',
  `userid` int(0) NULL DEFAULT NULL COMMENT '关联用户表信息',
  `category` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '积分变化对应的类别，如：\r\n阅读文章：消耗文章设定积分\r\n评论文章：加2分\r\n正常登录：加1分\r\n用户注册：加50积分\r\n在线充值：1元换10分\r\n用户投稿：加200积分\r\n',
  `target` int(0) NULL DEFAULT NULL COMMENT '积分消耗对应的目标，如果是阅读和评论文章，则对应为文章ID，如果在正常登录或注册，则显示0。',
  `credit` int(0) NULL DEFAULT NULL COMMENT '整数，可正可负',
  `createtime` datetime(0) NULL DEFAULT NULL,
  `updatetime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`creditid`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
