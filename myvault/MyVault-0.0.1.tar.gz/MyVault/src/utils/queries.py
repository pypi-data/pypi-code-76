CREATE_SQLITE_DB = """
CREATE TABLE IF NOT EXISTS local_vault (
    folder          TEXT NOT NULL,
    name            TEXT NOT NULL,
    secret          TEXT NOT NULL,
    created_at      TEXT NOT NULL,
    last_updated_at TEXT NOT NULL,
    UNIQUE(folder, name)
);
"""

INSERT_SECRET = """
INSERT INTO local_vault VALUES (?, ?, ?, ?, ?);
"""

UPDATE_SECRET = """
UPDATE local_vault 
SET secret=?,
    last_updated_at=?
WHERE folder=?
  AND name=?;
"""

SELECT_ALL = """
SELECT folder, name, secret FROM local_vault
ORDER BY FOLDER, NAME;
"""

SELECT_FOLDER_NAME = """
SELECT folder, name FROM local_vault
ORDER BY FOLDER, NAME;
"""

SELECT_SECRET = """
SELECT secret FROM local_vault
WHERE folder=?
  AND name=?;
"""

DELETE_SECRET = """
DELETE FROM local_vault
WHERE folder=?
  AND name=?;
"""
