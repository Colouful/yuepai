-- =============================================
-- 约拍管理模块 菜单SQL
-- 使用 sys_menu 表（RuoYi 权限菜单）
-- =============================================

-- 一、一级菜单：约拍管理
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('约拍管理', 0, 10, '#', 'M', '0', '', 'peoples', 'admin', sysdate(), '', null, '约拍管理菜单');

-- 获取刚插入的一级菜单ID（用于后续子菜单）
SET @parentId = LAST_INSERT_ID();

-- =============================================
-- 二、二级菜单（8个）
-- =============================================

-- 1. 用户管理
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('用户管理', @parentId, 1, '/yuepai/user', 'C', '0', 'yuepai:user:list', 'user', 'admin', sysdate(), '', null, '约拍用户管理');

SET @menu1 = LAST_INSERT_ID();

-- 2. 订单管理
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('订单管理', @parentId, 2, '/yuepai/order', 'C', '0', 'yuepai:order:list', 'form', 'admin', sysdate(), '', null, '约拍订单管理');

SET @menu2 = LAST_INSERT_ID();

-- 3. 内容审核
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('内容审核', @parentId, 3, '/yuepai/audit', 'C', '0', 'yuepai:audit:list', 'eye-open', 'admin', sysdate(), '', null, '约拍内容审核');

SET @menu3 = LAST_INSERT_ID();

-- 4. 财务管理
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('财务管理', @parentId, 4, '/yuepai/finance', 'C', '0', 'yuepai:finance:list', 'money', 'admin', sysdate(), '', null, '约拍财务管理');

SET @menu4 = LAST_INSERT_ID();

-- 5. 积分管理
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('积分管理', @parentId, 5, '/yuepai/points', 'C', '0', 'yuepai:points:list', 'skill', 'admin', sysdate(), '', null, '约拍积分管理');

SET @menu5 = LAST_INSERT_ID();

-- 6. 会员管理
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('会员管理', @parentId, 6, '/yuepai/member', 'C', '0', 'yuepai:member:list', 'people', 'admin', sysdate(), '', null, '约拍会员管理');

SET @menu6 = LAST_INSERT_ID();

-- 7. 数据统计
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('数据统计', @parentId, 7, '/yuepai/statistics', 'C', '0', 'yuepai:statistics:list', 'chart', 'admin', sysdate(), '', null, '约拍数据统计');

SET @menu7 = LAST_INSERT_ID();

-- 8. 系统配置
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('系统配置', @parentId, 8, '/yuepai/config', 'C', '0', 'yuepai:config:list', 'edit', 'admin', sysdate(), '', null, '约拍系统配置');

SET @menu8 = LAST_INSERT_ID();

-- =============================================
-- 三、按钮级权限（F类型）
-- =============================================

-- 用户管理按钮
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('用户查询', @menu1, 1, '#', 'F', '0', 'yuepai:user:query', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('用户新增', @menu1, 2, '#', 'F', '0', 'yuepai:user:add', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('用户修改', @menu1, 3, '#', 'F', '0', 'yuepai:user:edit', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('用户删除', @menu1, 4, '#', 'F', '0', 'yuepai:user:remove', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('用户导出', @menu1, 5, '#', 'F', '0', 'yuepai:user:export', '#', 'admin', sysdate(), '', null, '');

-- 订单管理按钮
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('订单查询', @menu2, 1, '#', 'F', '0', 'yuepai:order:query', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('订单新增', @menu2, 2, '#', 'F', '0', 'yuepai:order:add', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('订单修改', @menu2, 3, '#', 'F', '0', 'yuepai:order:edit', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('订单删除', @menu2, 4, '#', 'F', '0', 'yuepai:order:remove', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('订单导出', @menu2, 5, '#', 'F', '0', 'yuepai:order:export', '#', 'admin', sysdate(), '', null, '');

-- 内容审核按钮
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('审核查询', @menu3, 1, '#', 'F', '0', 'yuepai:audit:query', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('审核通过', @menu3, 2, '#', 'F', '0', 'yuepai:audit:approve', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('审核驳回', @menu3, 3, '#', 'F', '0', 'yuepai:audit:reject', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('审核导出', @menu3, 4, '#', 'F', '0', 'yuepai:audit:export', '#', 'admin', sysdate(), '', null, '');

-- 财务管理按钮
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('财务查询', @menu4, 1, '#', 'F', '0', 'yuepai:finance:query', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('财务新增', @menu4, 2, '#', 'F', '0', 'yuepai:finance:add', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('财务修改', @menu4, 3, '#', 'F', '0', 'yuepai:finance:edit', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('财务删除', @menu4, 4, '#', 'F', '0', 'yuepai:finance:remove', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('财务导出', @menu4, 5, '#', 'F', '0', 'yuepai:finance:export', '#', 'admin', sysdate(), '', null, '');

-- 积分管理按钮
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('积分查询', @menu5, 1, '#', 'F', '0', 'yuepai:points:query', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('积分新增', @menu5, 2, '#', 'F', '0', 'yuepai:points:add', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('积分修改', @menu5, 3, '#', 'F', '0', 'yuepai:points:edit', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('积分删除', @menu5, 4, '#', 'F', '0', 'yuepai:points:remove', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('积分导出', @menu5, 5, '#', 'F', '0', 'yuepai:points:export', '#', 'admin', sysdate(), '', null, '');

-- 会员管理按钮
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('会员查询', @menu6, 1, '#', 'F', '0', 'yuepai:member:query', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('会员新增', @menu6, 2, '#', 'F', '0', 'yuepai:member:add', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('会员修改', @menu6, 3, '#', 'F', '0', 'yuepai:member:edit', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('会员删除', @menu6, 4, '#', 'F', '0', 'yuepai:member:remove', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('会员导出', @menu6, 5, '#', 'F', '0', 'yuepai:member:export', '#', 'admin', sysdate(), '', null, '');

-- 数据统计按钮
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('统计查询', @menu7, 1, '#', 'F', '0', 'yuepai:statistics:query', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('统计导出', @menu7, 2, '#', 'F', '0', 'yuepai:statistics:export', '#', 'admin', sysdate(), '', null, '');

-- 系统配置按钮
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('配置查询', @menu8, 1, '#', 'F', '0', 'yuepai:config:query', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('配置新增', @menu8, 2, '#', 'F', '0', 'yuepai:config:add', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('配置修改', @menu8, 3, '#', 'F', '0', 'yuepai:config:edit', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('配置删除', @menu8, 4, '#', 'F', '0', 'yuepai:config:remove', '#', 'admin', sysdate(), '', null, '');
INSERT INTO sys_menu (menu_name, parent_id, order_num, url, menu_type, visible, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES ('配置导出', @menu8, 5, '#', 'F', '0', 'yuepai:config:export', '#', 'admin', sysdate(), '', null, '');
