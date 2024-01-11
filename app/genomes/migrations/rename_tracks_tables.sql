-- Ensure you remove genomes/__pycache__/
-- see https://stackoverflow.com/questions/8408046/how-to-change-the-name-of-a-django-app

UPDATE django_content_type SET app_label='genomes' WHERE app_label='tracks';
ALTER TABLE tracks_genome RENAME TO genomes_genome;
ALTER TABLE tracks_lab RENAME TO genomes_lab;
ALTER TABLE tracks_track RENAME TO genomes_track;
UPDATE django_migrations SET app='genomes' WHERE app='tracks';
