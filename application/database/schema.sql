CREATE TABLE users (
    user_id             INTEGER         NOT NULL,
    first_name          TEXT,
    last_name           TEXT,
    age                 INTEGER,
    email               TEXT,
    phone               TEXT,
    gender              TEXT,
    password            TEXT            NOT NULL,
    user_type           TEXT            NOT NULL CHECK (user_type IN ('STUDENT', 'COORDINATOR', 'ADMINISTRATOR')),
    approved            TEXT            CHECK (approved IN ('PENDING', 'APPROVED', 'REJECTED')) DEFAULT 'PENDING',
    created             DATETIME        DEFAULT CURRENT_TIMESTAMP,
    updated             DATETIME        DEFAULT CURRENT_TIMESTAMP,
    -------------------------------------------------
    PRIMARY KEY (user_id)
);

CREATE TABLE login (
    user_id             INTEGER         NOT NULL,
    username            TEXT            NOT NULL,
    created             DATETIME        DEFAULT CURRENT_TIMESTAMP,
    -------------------------------------------------
    PRIMARY KEY (username),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE clubs (
    club_id             INTEGER,
    club_name           TEXT,
    club_description    TEXT,
    creator             INTEGER,
    validity            TEXT            CHECK (validity IN ('PENDING', 'APPROVED', 'REJECTED')) DEFAULT 'PENDING',
    created             DATETIME        DEFAULT CURRENT_TIMESTAMP,
    updated             DATETIME        DEFAULT CURRENT_TIMESTAMP,
    --------------------------------------------------------------------
    PRIMARY KEY (club_id),
    FOREIGN KEY (creator) REFERENCES users(user_id)
);

CREATE TABLE club_memberships (
    club_id             INTEGER,
    user_id             INTEGER,
    validity            TEXT            CHECK (validity IN ('PENDING', 'APPROVED', 'REJECTED')) DEFAULT 'PENDING',
    created             DATETIME        DEFAULT CURRENT_TIMESTAMP,
    updated             DATETIME        DEFAULT CURRENT_TIMESTAMP,
    -----------------------------------------------
    PRIMARY KEY (club_id, user_id),
    FOREIGN KEY (club_id) REFERENCES clubs(club_id)
);


CREATE TABLE events (
    event_id            INTEGER PRIMARY KEY AUTOINCREMENT,
    club_id             INTEGER,
    event_name          TEXT,
    event_description   TEXT,
    venue               TEXT,
    date                TEXT,
    time                TEXT,
    created             DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated             DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (club_id) REFERENCES clubs(club_id)
);






CREATE TABLE event_participants (
    event_id            INTEGER,
    user_id             INTEGER,
    validity            TEXT            CHECK (validity IN ('PENDING', 'APPROVED', 'REJECTED')) DEFAULT 'PENDING',
    created             DATETIME        DEFAULT CURRENT_TIMESTAMP,
    updated             DATETIME        DEFAULT CURRENT_TIMESTAMP,
    --------------------------------------------------
    PRIMARY KEY (event_id, user_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    FOREIGN KEY (event_id) REFERENCES events(event_id)
);

CREATE TRIGGER update_timestamp_users
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    UPDATE users SET updated = CURRENT_TIMESTAMP WHERE user_id = OLD.user_id;
END;

CREATE TRIGGER update_timestamp_login
AFTER UPDATE ON login
FOR EACH ROW
BEGIN
    UPDATE login SET updated = CURRENT_TIMESTAMP WHERE username = OLD.username;
END;

CREATE TRIGGER update_timestamp_clubs
AFTER UPDATE ON clubs
FOR EACH ROW
BEGIN
    UPDATE clubs SET updated = CURRENT_TIMESTAMP WHERE club_id = OLD.club_id;
END;

CREATE TRIGGER update_timestamp_club_memberships
AFTER UPDATE ON club_memberships
FOR EACH ROW
BEGIN
    UPDATE club_memberships SET updated = CURRENT_TIMESTAMP WHERE club_id = OLD.club_id AND user_id = OLD.user_id;
END;

CREATE TRIGGER update_timestamp_events
AFTER UPDATE ON events
FOR EACH ROW
BEGIN
    UPDATE events SET updated = CURRENT_TIMESTAMP WHERE event_id = OLD.event_id;
END;

CREATE TRIGGER update_timestamp_event_participants
AFTER UPDATE ON event_participants
FOR EACH ROW
BEGIN
    UPDATE event_participants SET updated = CURRENT_TIMESTAMP WHERE event_id = OLD.event_id AND user_id = OLD.user_id;
END;

--
--CREATE TRIGGER check_max_clubs
--BEFORE INSERT ON club_memberships
--BEGIN
--    SELECT CASE
--        WHEN (SELECT COUNT(*) FROM club_memberships WHERE user_id = NEW.user_id) >= 3
--        THEN
--            RAISE(ABORT, 'Cannot add more than 3 clubs for a user');
--    END;
--END;
--
