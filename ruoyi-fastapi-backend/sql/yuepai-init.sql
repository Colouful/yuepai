-- ============================
-- 约拍平台业务表初始化SQL
-- 基于 RuoYi-Vue3-FastAPI 扩展
-- ============================

-- 约拍用户扩展表
CREATE TABLE IF NOT EXISTS `yuepai_user` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `sys_user_id` bigint NOT NULL COMMENT '关联RuoYi系统用户ID',
  `uid` varchar(32) NOT NULL COMMENT '约拍用户UID',
  `phone` varchar(20) DEFAULT NULL COMMENT '手机号',
  `phone_hash` varchar(64) DEFAULT NULL COMMENT '手机号哈希',
  `wechat_openid` varchar(64) DEFAULT NULL COMMENT '微信OpenID',
  `role` varchar(20) NOT NULL DEFAULT 'user' COMMENT '角色',
  `city` varchar(50) DEFAULT NULL COMMENT '城市',
  `bio` varchar(500) DEFAULT NULL COMMENT '简介',
  `is_verified` char(1) DEFAULT '0' COMMENT '实名认证: 0否 1是',
  `is_professional` char(1) DEFAULT '0' COMMENT '专业认证',
  `credit_score` int DEFAULT 100 COMMENT '信用分',
  `balance` decimal(10,2) DEFAULT 0 COMMENT '账户余额',
  `point_balance` int DEFAULT 0 COMMENT '积分余额',
  `follower_count` int DEFAULT 0 COMMENT '粉丝数',
  `yuepai_count` int DEFAULT 0 COMMENT '约拍次数',
  `status` char(1) DEFAULT '0' COMMENT '状态: 0正常 1禁用',
  `del_flag` char(1) DEFAULT '0' COMMENT '删除标志',
  `create_by` varchar(64) DEFAULT '',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `update_by` varchar(64) DEFAULT '',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `remark` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_uid` (`uid`),
  UNIQUE KEY `uk_phone_hash` (`phone_hash`),
  UNIQUE KEY `uk_wechat_openid` (`wechat_openid`),
  KEY `idx_role` (`role`),
  KEY `idx_city` (`city`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='约拍用户扩展表';

-- 约拍需求表
CREATE TABLE IF NOT EXISTS `yuepai_demand` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `demand_no` varchar(32) NOT NULL COMMENT '需求编号',
  `user_id` bigint NOT NULL COMMENT '发布者ID',
  `type` varchar(20) NOT NULL COMMENT '类型',
  `title` varchar(100) NOT NULL COMMENT '标题',
  `description` varchar(2000) NOT NULL COMMENT '描述',
  `shooting_type` varchar(30) NOT NULL COMMENT '拍摄类型',
  `shooting_date` datetime NOT NULL COMMENT '拍摄日期',
  `city` varchar(50) NOT NULL COMMENT '城市',
  `budget_min` decimal(10,2) DEFAULT 0 COMMENT '预算下限',
  `budget_max` decimal(10,2) DEFAULT 0 COMMENT '预算上限',
  `is_mutual` char(1) DEFAULT '0' COMMENT '是否互勉',
  `reference_images` json DEFAULT NULL COMMENT '参考图片',
  `status` char(1) DEFAULT '0' COMMENT '状态: 0关闭 1开放 2进行中 3已完成',
  `view_count` int DEFAULT 0 COMMENT '浏览数',
  `apply_count` int DEFAULT 0 COMMENT '申请数',
  `audit_status` char(1) DEFAULT '0' COMMENT '审核: 0待审 1通过 2拒绝',
  `del_flag` char(1) DEFAULT '0',
  `create_by` varchar(64) DEFAULT '',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `update_by` varchar(64) DEFAULT '',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_demand_no` (`demand_no`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_city_type` (`city`, `type`),
  KEY `idx_audit` (`audit_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='约拍需求表';

-- 约拍订单表
CREATE TABLE IF NOT EXISTS `yuepai_order` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `order_no` varchar(32) NOT NULL COMMENT '订单编号',
  `demand_id` bigint NOT NULL COMMENT '需求ID',
  `publisher_id` bigint NOT NULL COMMENT '需求方ID',
  `photographer_id` bigint NOT NULL COMMENT '摄影师ID',
  `total_amount` decimal(10,2) NOT NULL COMMENT '总金额',
  `deposit_amount` decimal(10,2) NOT NULL COMMENT '定金',
  `final_amount` decimal(10,2) DEFAULT NULL COMMENT '尾款',
  `platform_fee` decimal(10,2) DEFAULT 0 COMMENT '平台佣金',
  `photographer_income` decimal(10,2) DEFAULT 0 COMMENT '摄影师收入',
  `shooting_date` datetime NOT NULL COMMENT '拍摄日期',
  `status` char(1) DEFAULT '0' COMMENT '状态',
  `del_flag` char(1) DEFAULT '0',
  `create_by` varchar(64) DEFAULT '',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `update_by` varchar(64) DEFAULT '',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_order_no` (`order_no`),
  KEY `idx_publisher` (`publisher_id`),
  KEY `idx_photographer` (`photographer_id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='约拍订单表';

-- 支付记录表
CREATE TABLE IF NOT EXISTS `yuepai_payment` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `payment_no` varchar(64) NOT NULL COMMENT '支付流水号',
  `order_id` bigint NOT NULL COMMENT '订单ID',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `type` int NOT NULL COMMENT '类型: 1定金 2尾款 3充值 4会员',
  `amount` decimal(10,2) NOT NULL COMMENT '金额',
  `channel` varchar(20) NOT NULL COMMENT '支付渠道',
  `status` int DEFAULT 0 COMMENT '状态: 0待支付 1成功 2失败 3已退款',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_payment_no` (`payment_no`),
  KEY `idx_order` (`order_id`),
  KEY `idx_user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='支付记录表';

-- 作品动态表
CREATE TABLE IF NOT EXISTS `yuepai_post` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `user_id` bigint NOT NULL COMMENT '作者ID',
  `type` varchar(20) DEFAULT 'work' COMMENT '类型',
  `title` varchar(100) DEFAULT NULL COMMENT '标题',
  `content` varchar(2000) DEFAULT NULL COMMENT '内容',
  `images` json NOT NULL COMMENT '图片列表',
  `like_count` int DEFAULT 0,
  `comment_count` int DEFAULT 0,
  `view_count` int DEFAULT 0,
  `audit_status` char(1) DEFAULT '0' COMMENT '审核: 0待审 1通过 2拒绝',
  `status` char(1) DEFAULT '0' COMMENT '状态: 0正常 1下架',
  `del_flag` char(1) DEFAULT '0',
  `create_by` varchar(64) DEFAULT '',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `update_by` varchar(64) DEFAULT '',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user` (`user_id`),
  KEY `idx_audit` (`audit_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='作品动态表';

-- 积分记录表
CREATE TABLE IF NOT EXISTS `yuepai_point_record` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `type` varchar(30) NOT NULL COMMENT '类型',
  `amount` int NOT NULL COMMENT '积分数量',
  `balance` int NOT NULL COMMENT '变动后余额',
  `description` varchar(200) DEFAULT NULL COMMENT '描述',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user` (`user_id`),
  KEY `idx_type` (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='积分记录表';

-- 会员表
CREATE TABLE IF NOT EXISTS `yuepai_member` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `level` int DEFAULT 0 COMMENT '等级: 0普通 1银卡 2金卡 3钻石',
  `started_at` datetime DEFAULT NULL COMMENT '开始时间',
  `expired_at` datetime DEFAULT NULL COMMENT '过期时间',
  `total_paid` decimal(10,2) DEFAULT 0 COMMENT '累计付费',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='会员表';

-- ============================
-- 菜单数据（插入RuoYi菜单表）
-- ============================
-- 一级菜单：约拍管理
INSERT INTO sys_menu(menu_name, parent_id, order_num, path, component, menu_type, visible, status, perms, icon, create_by, create_time)
VALUES ('约拍管理', 0, 10, 'yuepai', NULL, 'M', '0', '0', NULL, 'camera', 'admin', NOW());

SET @yp_id = LAST_INSERT_ID();

INSERT INTO sys_menu(menu_name, parent_id, order_num, path, component, menu_type, visible, status, perms, icon, create_by, create_time)
VALUES
('用户管理', @yp_id, 1, 'user', 'yuepai/user/index', 'C', '0', '0', 'yuepai:user:list', 'user', 'admin', NOW()),
('需求管理', @yp_id, 2, 'demand', 'yuepai/demand/index', 'C', '0', '0', 'yuepai:demand:list', 'form', 'admin', NOW()),
('订单管理', @yp_id, 3, 'order', 'yuepai/order/index', 'C', '0', '0', 'yuepai:order:list', 'shopping', 'admin', NOW()),
('内容审核', @yp_id, 4, 'content', 'yuepai/content/index', 'C', '0', '0', 'yuepai:content:list', 'documentation', 'admin', NOW()),
('财务统计', @yp_id, 5, 'finance', 'yuepai/finance/index', 'C', '0', '0', 'yuepai:finance:list', 'money', 'admin', NOW()),
('数据统计', @yp_id, 6, 'stats', 'yuepai/stats/index', 'C', '0', '0', 'yuepai:stats:list', 'chart', 'admin', NOW());
