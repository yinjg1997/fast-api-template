-- ym_user definition
CREATE TABLE `ym_user` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `union_id` varchar(64) NOT NULL DEFAULT '' COMMENT '微信开放平台下的用户唯一标识',
  `open_id` varchar(64) NOT NULL DEFAULT '' COMMENT '微信openid',
  `nick_name` varchar(32) NOT NULL DEFAULT '' COMMENT '昵称',
  `password` varchar(64) NOT NULL DEFAULT '' COMMENT '密码',
  `avatar` varchar(255) NOT NULL DEFAULT '' COMMENT '头像',
  `phone` varchar(11) NOT NULL DEFAULT '' COMMENT '手机号',
  `email` varchar(50) NOT NULL DEFAULT '' COMMENT '电子邮箱',
  `last_login` varchar(20) NOT NULL DEFAULT '' COMMENT '上次登录时间',
  `status` tinyint NOT NULL DEFAULT '1' COMMENT '状态；-1:黑名单 1:正常',
  `delete_at` varchar(20) NOT NULL DEFAULT '' COMMENT '删除时间',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_phone` (`phone`) USING BTREE,
  KEY `idx_nick_name` (`nick_name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户表';


CREATE TABLE `ym_user_info` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `uid` bigint unsigned NOT NULL DEFAULT '0' COMMENT '用户id',
  `sex` tinyint NOT NULL DEFAULT '-1' COMMENT '性别；-1:未知 1:男 2:女 ',
  `province` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '省市',
  `city` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '城市',
  `county` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '区域',
  `address` varchar(255) NOT NULL DEFAULT '' COMMENT '详细地址',
  `delete_at` varchar(20) NOT NULL DEFAULT '' COMMENT '删除时间',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_uid` (`uid`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户信息表';

-- auto-generated definition
create table modelscope_wan_task_info
(
    id           int auto_increment comment '自增主键'
        primary key,
    hf_token     varchar(255) null comment 'api token',
    task_type    varchar(255) not null comment '任务类型 i2v | t2v',
    prompt       text         null comment '提示词',
    video_size   varchar(255) null comment 't2v 视频尺寸 [''1280*720'', ''960*960'', ''720*1280'', ''1088*832'', ''832*1088'']',
    image        varchar(255) null comment 'i2v 图片 URL',
    model_type   varchar(255) not null comment '[''wanx2.1-t2v-plus'', ''wanx2.1-t2v-turbo''] [''wanx2.1-i2v-plus'', ''wanx2.1-i2v-turbo'']',
    seed         float        not null comment '随机种子',
    task_status  varchar(255) null comment '任务状态 pending | progressing | completed',
    cost_time    float        null comment '处理时间',
    video_url    varchar(255) null comment '生成的视频 URL',
    is_pushed    varchar(10)  null comment '是否推送 0 | 1',
    inst_time    datetime     null comment '记录创建时间',
    inst_user_no varchar(50)  null comment '记录创建用户',
    updt_time    datetime     null comment '记录更新时间',
    updt_user_no varchar(50)  null comment '记录更新用户'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci comment 'modelscope wan 任务信息表';

INSERT INTO spider_db_local.modelscope_wan_task_info (id, hf_token, task_type, prompt, video_size, image, model_type, seed, task_status, cost_time, video_url, is_pushed, inst_time, inst_user_no, updt_time, updt_user_no) VALUES (1, '7087a490-63e7-48a5-923d-68645fddc0fc', 't2v', '    主题：卡通鸡（红色鸡冠和肉垂，简约线条）
    场景：浅米色背景（简单而突出角色）
    动作：鸡啄食虫子（虫子用弯曲线条表示运动）
    镜头语言：中景镜头，聚焦在鸡与虫子的互动
    氛围：轻松、幽默
    风格：手绘简约风格', '720*1280', null, 'wanx2.1-t2v-plus', -1, 'pending', null, null, null, null, null, null, null);


