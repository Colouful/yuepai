-- 91约拍Pro MVP核心业务迁移
-- 适用：MySQL 8.0+
-- 执行前请备份数据库；本脚本使用 CREATE TABLE IF NOT EXISTS，可重复执行。

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

CREATE TABLE IF NOT EXISTS yp_demand (
  demand_id bigint NOT NULL AUTO_INCREMENT COMMENT '需求ID',
  owner_user_id bigint NOT NULL COMMENT '发布用户ID',
  title varchar(80) NOT NULL COMMENT '需求标题',
  description text NOT NULL COMMENT '需求描述',
  demand_type varchar(32) NOT NULL COMMENT '约拍类型',
  city_code varchar(20) NOT NULL COMMENT '城市编码',
  location_name varchar(160) DEFAULT NULL COMMENT '地点名称',
  shoot_at datetime NOT NULL COMMENT '拍摄开始时间',
  duration_minutes int NOT NULL DEFAULT 120 COMMENT '预计时长',
  roles_json text NOT NULL COMMENT '招募角色JSON',
  reference_assets_json text DEFAULT NULL COMMENT '参考图JSON',
  budget_type varchar(20) NOT NULL COMMENT '预算类型',
  budget_min decimal(12,2) DEFAULT NULL COMMENT '最低预算',
  budget_max decimal(12,2) DEFAULT NULL COMMENT '最高预算',
  applicant_limit int NOT NULL DEFAULT 20 COMMENT '报名人数上限',
  application_deadline datetime NOT NULL COMMENT '报名截止时间',
  audit_status varchar(16) NOT NULL DEFAULT 'pending' COMMENT '审核状态',
  status varchar(16) NOT NULL DEFAULT 'draft' COMMENT '业务状态',
  version int NOT NULL DEFAULT 1 COMMENT '乐观锁版本',
  create_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  update_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (demand_id),
  KEY idx_yp_demand_city_status_time (city_code, status, shoot_at),
  KEY idx_yp_demand_owner_status (owner_user_id, status),
  CONSTRAINT fk_yp_demand_owner FOREIGN KEY (owner_user_id) REFERENCES sys_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='约拍需求表';

CREATE TABLE IF NOT EXISTS yp_application (
  application_id bigint NOT NULL AUTO_INCREMENT COMMENT '报名ID',
  demand_id bigint NOT NULL COMMENT '需求ID',
  applicant_user_id bigint NOT NULL COMMENT '报名用户ID',
  role_code varchar(32) NOT NULL COMMENT '报名身份',
  introduction varchar(500) NOT NULL COMMENT '报名说明',
  quote_amount decimal(12,2) DEFAULT NULL COMMENT '报名报价',
  portfolio_assets_json text DEFAULT NULL COMMENT '作品资料JSON',
  status varchar(20) NOT NULL DEFAULT 'pending' COMMENT '报名状态',
  reject_reason varchar(500) DEFAULT NULL COMMENT '未入选原因',
  version int NOT NULL DEFAULT 1 COMMENT '乐观锁版本',
  create_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  update_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (application_id),
  UNIQUE KEY uk_yp_application_demand_user_role (demand_id, applicant_user_id, role_code),
  KEY idx_yp_application_demand_status (demand_id, status),
  CONSTRAINT fk_yp_application_demand FOREIGN KEY (demand_id) REFERENCES yp_demand (demand_id),
  CONSTRAINT fk_yp_application_user FOREIGN KEY (applicant_user_id) REFERENCES sys_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='约拍需求报名表';

CREATE TABLE IF NOT EXISTS yp_quote (
  quote_id bigint NOT NULL AUTO_INCREMENT COMMENT '报价ID',
  demand_id bigint DEFAULT NULL COMMENT '需求ID',
  application_id bigint DEFAULT NULL COMMENT '报名ID',
  sender_user_id bigint NOT NULL COMMENT '报价方用户ID',
  receiver_user_id bigint NOT NULL COMMENT '接收方用户ID',
  amount decimal(12,2) NOT NULL COMMENT '报价总额',
  fee_breakdown_json text NOT NULL COMMENT '费用明细JSON',
  service_snapshot_json text NOT NULL COMMENT '服务内容快照JSON',
  remark varchar(1000) DEFAULT NULL COMMENT '补充说明',
  expires_at datetime NOT NULL COMMENT '报价失效时间',
  status varchar(20) NOT NULL DEFAULT 'pending' COMMENT '报价状态',
  parent_quote_id bigint DEFAULT NULL COMMENT '原报价ID',
  version int NOT NULL DEFAULT 1 COMMENT '乐观锁版本',
  create_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  update_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (quote_id),
  KEY idx_yp_quote_demand_status (demand_id, status),
  KEY idx_yp_quote_receiver_status (receiver_user_id, status),
  CONSTRAINT fk_yp_quote_demand FOREIGN KEY (demand_id) REFERENCES yp_demand (demand_id),
  CONSTRAINT fk_yp_quote_application FOREIGN KEY (application_id) REFERENCES yp_application (application_id),
  CONSTRAINT fk_yp_quote_sender FOREIGN KEY (sender_user_id) REFERENCES sys_user (user_id),
  CONSTRAINT fk_yp_quote_receiver FOREIGN KEY (receiver_user_id) REFERENCES sys_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='约拍服务报价表';

CREATE TABLE IF NOT EXISTS yp_order (
  order_id bigint NOT NULL AUTO_INCREMENT COMMENT '订单ID',
  order_no varchar(40) NOT NULL COMMENT '订单编号',
  buyer_user_id bigint NOT NULL COMMENT '买方用户ID',
  seller_user_id bigint NOT NULL COMMENT '卖方用户ID',
  demand_id bigint DEFAULT NULL COMMENT '需求ID',
  quote_id bigint DEFAULT NULL COMMENT '报价ID',
  service_snapshot_json text NOT NULL COMMENT '服务内容快照JSON',
  amount decimal(12,2) NOT NULL COMMENT '服务金额',
  platform_fee decimal(12,2) NOT NULL DEFAULT 0 COMMENT '平台服务费',
  discount_amount decimal(12,2) NOT NULL DEFAULT 0 COMMENT '优惠金额',
  payable_amount decimal(12,2) NOT NULL COMMENT '应付金额',
  paid_amount decimal(12,2) NOT NULL DEFAULT 0 COMMENT '已付金额',
  shoot_at datetime NOT NULL COMMENT '拍摄时间',
  duration_minutes int NOT NULL COMMENT '预计服务时长',
  location_snapshot_json text NOT NULL COMMENT '地点快照JSON',
  contact_snapshot_json text NOT NULL COMMENT '联系人快照JSON',
  remark varchar(1000) DEFAULT NULL COMMENT '订单备注',
  status varchar(32) NOT NULL DEFAULT 'pending_payment' COMMENT '订单状态',
  payment_status varchar(20) NOT NULL DEFAULT 'unpaid' COMMENT '支付状态',
  refund_status varchar(20) NOT NULL DEFAULT 'none' COMMENT '退款状态',
  version int NOT NULL DEFAULT 1 COMMENT '乐观锁版本',
  create_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  update_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (order_id),
  UNIQUE KEY uk_yp_order_no (order_no),
  KEY idx_yp_order_buyer_status (buyer_user_id, status),
  KEY idx_yp_order_seller_status (seller_user_id, status),
  CONSTRAINT fk_yp_order_buyer FOREIGN KEY (buyer_user_id) REFERENCES sys_user (user_id),
  CONSTRAINT fk_yp_order_seller FOREIGN KEY (seller_user_id) REFERENCES sys_user (user_id),
  CONSTRAINT fk_yp_order_demand FOREIGN KEY (demand_id) REFERENCES yp_demand (demand_id),
  CONSTRAINT fk_yp_order_quote FOREIGN KEY (quote_id) REFERENCES yp_quote (quote_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='约拍订单表';

CREATE TABLE IF NOT EXISTS yp_order_event (
  event_id bigint NOT NULL AUTO_INCREMENT COMMENT '事件ID',
  order_id bigint NOT NULL COMMENT '订单ID',
  operator_user_id bigint NOT NULL COMMENT '操作用户ID',
  from_status varchar(32) DEFAULT NULL COMMENT '原状态',
  to_status varchar(32) NOT NULL COMMENT '新状态',
  event_type varchar(32) NOT NULL COMMENT '事件类型',
  reason varchar(500) DEFAULT NULL COMMENT '操作原因',
  request_id varchar(64) NOT NULL COMMENT '请求幂等号',
  create_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (event_id),
  UNIQUE KEY uk_yp_order_event_request_id (request_id),
  KEY idx_yp_order_event_order_time (order_id, create_time),
  CONSTRAINT fk_yp_order_event_order FOREIGN KEY (order_id) REFERENCES yp_order (order_id),
  CONSTRAINT fk_yp_order_event_user FOREIGN KEY (operator_user_id) REFERENCES sys_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='约拍订单状态日志表';

SET FOREIGN_KEY_CHECKS = 1;
