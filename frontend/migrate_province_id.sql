-- 1. exam_papers 表
ALTER TABLE exam_papers ADD COLUMN province_id INT;
UPDATE exam_papers ep
JOIN provinces p ON ep.province = p.name
SET ep.province_id = p.id;
ALTER TABLE exam_papers ADD CONSTRAINT fk_exam_papers_province FOREIGN KEY (province_id) REFERENCES provinces(id);

-- 2. exam_points 表（如有）
ALTER TABLE exam_points ADD COLUMN province_id INT;
UPDATE exam_points ep
JOIN provinces p ON ep.province = p.name
SET ep.province_id = p.id;
ALTER TABLE exam_points ADD CONSTRAINT fk_exam_points_province FOREIGN KEY (province_id) REFERENCES provinces(id);

-- 3. 可选：删除原有 province 字段（建议迁移完成后再删）
-- ALTER TABLE exam_papers DROP COLUMN province;
-- ALTER TABLE exam_points DROP COLUMN province; 