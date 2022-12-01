-- POSTGRES TRIGGER EXAMPLE
CREATE FUNCTION update_changelog() RETURNS TRIGGER AS $update_changelog$
  DECLARE
    changes TEXT DEFAULT "Made unknown changes.";
  BEGIN
    INSERT INTO changelog(projid,projname,ucomment) VALUES (NEW.id,NEW.name,changes);
  END;
$update_changelog$ LANGUAGE plpgsql;

CREATE TRIGGER updatechangelog 
  AFTER INSERT OR UPDATE OR DELETE ON projects
  FOR EACH ROW 
  EXECUTE FUNCTION update_changelog(); 
