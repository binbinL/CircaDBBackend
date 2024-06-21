from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `gsetable` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `GSE` VARCHAR(32) NOT NULL  COMMENT 'GSE号',
    `title` VARCHAR(255) NOT NULL  COMMENT '对应文章名'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `gene` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(32) NOT NULL  COMMENT '基因名',
    `type` VARCHAR(32) NOT NULL  COMMENT '种类'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `jtkvalue` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `omics` VARCHAR(32) NOT NULL  COMMENT '组学',
    `tissue` VARCHAR(32) NOT NULL  COMMENT '取样组织',
    `condition` VARCHAR(32) NOT NULL  COMMENT '条件',
    `JTK_pvalue` DOUBLE NOT NULL  COMMENT 'JTK_value',
    `JTK_BH_Q` DOUBLE NOT NULL  COMMENT 'JTK_BH_Q',
    `JTK_period` DOUBLE NOT NULL  COMMENT 'JTK_period',
    `JTK_adjphase` DOUBLE NOT NULL  COMMENT 'JTK_adjphase',
    `JTK_amplitude` DOUBLE NOT NULL  COMMENT 'JTK_amplitude',
    `meta2d_Base` DOUBLE NOT NULL  COMMENT 'meta2d_Base',
    `meta2d_AMP` DOUBLE NOT NULL  COMMENT 'meta2d_AMP',
    `meta2d_rAMP` DOUBLE NOT NULL  COMMENT 'meta2d_rAMP',
    `GSE_id` INT NOT NULL,
    `gene_id` INT NOT NULL,
    CONSTRAINT `fk_jtkvalue_gsetable_4f8c76f4` FOREIGN KEY (`GSE_id`) REFERENCES `gsetable` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_jtkvalue_gene_4c6f9b5e` FOREIGN KEY (`gene_id`) REFERENCES `gene` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
