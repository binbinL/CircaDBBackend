from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `homovalue` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `omics` VARCHAR(32) NOT NULL  COMMENT '组学',
    `tissue` VARCHAR(32) NOT NULL  COMMENT '取样组织',
    `condition` VARCHAR(32) NOT NULL  COMMENT '条件',
    `pvalue` DOUBLE NOT NULL  COMMENT 'pvalue',
    `R2` DOUBLE NOT NULL  COMMENT 'R2',
    `amp` DOUBLE NOT NULL  COMMENT 'amp',
    `phase` DOUBLE NOT NULL  COMMENT 'phase',
    `peakTime` DOUBLE NOT NULL  COMMENT 'peakTime',
    `offset` DOUBLE NOT NULL  COMMENT 'offset',
    `GSE_id` INT NOT NULL,
    `gene_id` INT NOT NULL,
    CONSTRAINT `fk_homovalu_gsetable_24db36be` FOREIGN KEY (`GSE_id`) REFERENCES `gsetable` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_homovalu_gene_84b0b8f6` FOREIGN KEY (`gene_id`) REFERENCES `gene` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
        CREATE TABLE IF NOT EXISTS `musvalue` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `omics` VARCHAR(32) NOT NULL  COMMENT '组学',
    `tissue` VARCHAR(32) NOT NULL  COMMENT '取样组织',
    `condition` VARCHAR(32) NOT NULL  COMMENT '条件',
    `pvalue` DOUBLE NOT NULL  COMMENT 'pvalue',
    `R2` DOUBLE NOT NULL  COMMENT 'R2',
    `amp` DOUBLE NOT NULL  COMMENT 'amp',
    `phase` DOUBLE NOT NULL  COMMENT 'phase',
    `peakTime` DOUBLE NOT NULL  COMMENT 'peakTime',
    `offset` DOUBLE NOT NULL  COMMENT 'offset',
    `GEOAccession_id` INT NOT NULL,
    `gene_id` INT NOT NULL,
    CONSTRAINT `fk_musvalue_gsetable_a00e305a` FOREIGN KEY (`GEOAccession_id`) REFERENCES `gsetable` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_musvalue_gene_112ee118` FOREIGN KEY (`gene_id`) REFERENCES `gene` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
        DROP TABLE IF EXISTS `jtkvalue`;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `homovalue`;
        DROP TABLE IF EXISTS `musvalue`;"""
