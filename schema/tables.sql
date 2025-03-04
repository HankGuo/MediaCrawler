-- ----------------------------
-- Table structure for xhs_creator
-- ----------------------------
DROP TABLE IF EXISTS `xhs_creator`;
CREATE TABLE `xhs_creator`
(
    `id`             int         NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `user_id`        varchar(64) NOT NULL COMMENT '用户ID',
    `nickname`       varchar(64)  DEFAULT NULL COMMENT '用户昵称',
    `avatar`         varchar(255) DEFAULT NULL COMMENT '用户头像地址',
    `ip_location`    varchar(255) DEFAULT NULL COMMENT '评论时的IP地址',
    `add_ts`         bigint      NOT NULL COMMENT '记录添加时间戳',
    `last_modify_ts` bigint      NOT NULL COMMENT '记录最后修改时间戳',
    `desc`           longtext COMMENT '用户描述',
    `gender`         varchar(1)   DEFAULT NULL COMMENT '性别',
    `follows`        varchar(16)  DEFAULT NULL COMMENT '关注数',
    `fans`           varchar(16)  DEFAULT NULL COMMENT '粉丝数',
    `interaction`    varchar(16)  DEFAULT NULL COMMENT '获赞和收藏数',
    `tag_list`       longtext COMMENT '标签列表',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='小红书博主';

-- ----------------------------
-- Table structure for xhs_note
-- ----------------------------
DROP TABLE IF EXISTS `xhs_creator`;
CREATE TABLE `xhs_note`
(
    `id`               int         NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `user_id`          varchar(64) NOT NULL COMMENT '用户ID',
    `nickname`         varchar(64)  DEFAULT NULL COMMENT '用户昵称',
    `avatar`           varchar(255) DEFAULT NULL COMMENT '用户头像地址',
    `ip_location`      varchar(255) DEFAULT NULL COMMENT '评论时的IP地址',
    `add_ts`           bigint      NOT NULL COMMENT '记录添加时间戳',
    `last_modify_ts`   bigint      NOT NULL COMMENT '记录最后修改时间戳',
    `note_id`          varchar(64) NOT NULL COMMENT '笔记ID',
    `type`             varchar(16)  DEFAULT NULL COMMENT '笔记类型(normal | video)',
    `title`            varchar(255) DEFAULT NULL COMMENT '笔记标题',
    `desc`             longtext COMMENT '笔记描述',
    `video_url`        longtext COMMENT '视频地址',
    `time`             bigint      NOT NULL COMMENT '笔记发布时间戳',
    `last_update_time` bigint      NOT NULL COMMENT '笔记最后更新时间戳',
    `liked_count`      varchar(16)  DEFAULT NULL COMMENT '笔记点赞数',
    `collected_count`  varchar(16)  DEFAULT NULL COMMENT '笔记收藏数',
    `comment_count`    varchar(16)  DEFAULT NULL COMMENT '笔记评论数',
    `share_count`      varchar(16)  DEFAULT NULL COMMENT '笔记分享数',
    `image_list`       longtext COMMENT '笔记封面图片列表',
    `tag_list`         longtext COMMENT '标签列表',
    `note_url`         varchar(255) DEFAULT NULL COMMENT '笔记详情页的URL',
    PRIMARY KEY (`id`),
    KEY                `idx_xhs_note_note_id_209457` (`note_id`),
    KEY                `idx_xhs_note_time_eaa910` (`time`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='小红书笔记';

-- ----------------------------
-- Table structure for xhs_note_comment
-- ----------------------------
DROP TABLE IF EXISTS `xhs_note_comment`;
CREATE TABLE `xhs_note_comment`
(
    `id`                int         NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `user_id`           varchar(64) NOT NULL COMMENT '用户ID',
    `nickname`          varchar(64)  DEFAULT NULL COMMENT '用户昵称',
    `avatar`            varchar(255) DEFAULT NULL COMMENT '用户头像地址',
    `ip_location`       varchar(255) DEFAULT NULL COMMENT '评论时的IP地址',
    `add_ts`            bigint      NOT NULL COMMENT '记录添加时间戳',
    `last_modify_ts`    bigint      NOT NULL COMMENT '记录最后修改时间戳',
    `comment_id`        varchar(64) NOT NULL COMMENT '评论ID',
    `create_time`       bigint      NOT NULL COMMENT '评论时间戳',
    `note_id`           varchar(64) NOT NULL COMMENT '笔记ID',
    `content`           longtext    NOT NULL COMMENT '评论内容',
    `sub_comment_count` int         NOT NULL COMMENT '子评论数量',
    `pictures`          varchar(512) DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY                 `idx_xhs_note_co_comment_8e8349` (`comment_id`),
    KEY                 `idx_xhs_note_co_create__204f8d` (`create_time`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='小红书笔记评论';

-- ----------------------------
-- alter table xhs_note_comment to support parent_comment_id
-- ----------------------------
ALTER TABLE `xhs_note_comment` ADD COLUMN `parent_comment_id` VARCHAR(64) DEFAULT NULL COMMENT '父评论ID';

ALTER TABLE xhs_note ADD COLUMN `source_keyword` VARCHAR(255) DEFAULT '' comment '搜索来源关键字';

ALTER TABLE `xhs_note_comment` ADD COLUMN `like_count` VARCHAR(64) DEFAULT NULL COMMENT '评论点赞数量';

ALTER TABLE xhs_note ADD COLUMN xsec_token VARCHAR(50) DEFAULT NULL comment '签名算法';