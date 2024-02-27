--================================================== Table Definitions ==================================================--

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
    approved            TEXT            NOT NULL CHECK (approved IN ('PENDING', 'APPROVED', 'REJECTED')) DEFAULT 'PENDING',
    created             DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated             DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -----------------------------------------------------------------------
    PRIMARY KEY (user_id)
);

CREATE TABLE login (
    user_id             INTEGER         NOT NULL,
    username            TEXT            NOT NULL,
    created             DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated             DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -----------------------------------------------------------------------
    PRIMARY KEY (username),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE clubs (
    club_id             INTEGER         NOT NULL,
    club_name           TEXT            NOT NULL,
    club_description    TEXT            NOT NULL,
    creator             INTEGER         NOT NULL,
    validity            TEXT            NOT NULL CHECK (validity IN ('PENDING', 'APPROVED', 'REJECTED')) DEFAULT 'PENDING',
    created             DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated             DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -----------------------------------------------------------------------
    PRIMARY KEY (club_id),
    FOREIGN KEY (creator) REFERENCES users(user_id)
);

CREATE TABLE club_memberships (
    club_id             INTEGER         NOT NULL,
    user_id             INTEGER         NOT NULL,
    validity            TEXT            NOT NULL CHECK (validity IN ('PENDING', 'APPROVED', 'REJECTED')) DEFAULT 'PENDING',
    created             DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated             DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -----------------------------------------------------------------------
    PRIMARY KEY (club_id, user_id),
    FOREIGN KEY (club_id) REFERENCES clubs(club_id)
);

CREATE TABLE events (
    event_id            INTEGER         NOT NULL,
    club_id             INTEGER         NOT NULL,
    event_name          TEXT            NOT NULL,
    event_description   TEXT            NOT NULL,
    venue               TEXT            NOT NULL,
    date                TEXT            NOT NULL,
    time                TEXT            NOT NULL,
    created             DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated             DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -----------------------------------------------------------------------
    PRIMARY KEY (event_id),
    FOREIGN KEY (club_id) REFERENCES clubs(club_id)
);

CREATE TABLE event_participants (
    event_id            INTEGER         NOT NULL,
    user_id             INTEGER         NOT NULL,
    validity            TEXT            NOT NULL CHECK (validity IN ('PENDING', 'APPROVED', 'REJECTED')) DEFAULT 'PENDING',
    created             DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated             DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -----------------------------------------------------------------------
    PRIMARY KEY (event_id, user_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (event_id) REFERENCES events(event_id)
);

--================================================== Timestamp Triggers =================================================--

CREATE TRIGGER update_timestamp_users
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    UPDATE users
    SET updated = CURRENT_TIMESTAMP
    WHERE user_id = OLD.user_id;
END;

CREATE TRIGGER update_timestamp_login
AFTER UPDATE ON login
FOR EACH ROW
BEGIN
    UPDATE login
    SET updated = CURRENT_TIMESTAMP
    WHERE username = OLD.username;
END;

CREATE TRIGGER update_timestamp_clubs
AFTER UPDATE ON clubs
FOR EACH ROW
BEGIN
    UPDATE clubs
    SET updated = CURRENT_TIMESTAMP
    WHERE club_id = OLD.club_id;
END;

CREATE TRIGGER update_timestamp_club_memberships
AFTER UPDATE ON club_memberships
FOR EACH ROW
BEGIN
    UPDATE club_memberships
    SET updated = CURRENT_TIMESTAMP
    WHERE club_id = OLD.club_id AND user_id = OLD.user_id;
END;

CREATE TRIGGER update_timestamp_events
AFTER UPDATE ON events
FOR EACH ROW
BEGIN
    UPDATE events
    SET updated = CURRENT_TIMESTAMP
    WHERE event_id = OLD.event_id;
END;

CREATE TRIGGER update_timestamp_event_participants
AFTER UPDATE ON event_participants
FOR EACH ROW
BEGIN
    UPDATE event_participants
    SET updated = CURRENT_TIMESTAMP
    WHERE event_id = OLD.event_id AND user_id = OLD.user_id;
END;

--========================================================= Views =======================================================--

-- 1: All user-related attributes (users & login tables)
CREATE VIEW all_user_attributes
AS
SELECT
    users.user_id,
    login.username,
    users.password,
    users.first_name,
    users.last_name,
    users.age,
    users.email,
    users.phone,
    users.gender,
    users.approved,
    users.user_type
FROM
    users
INNER JOIN login USING (user_id);

-- 2: All profile-related attributes (users table)
CREATE VIEW profile_user_attributes
AS
SELECT
    user_id,
    first_name,
    last_name,
    age,
    email,
    phone,
    gender
FROM
    users;

-- 3: All event-related attributes (events & clubs tables)
CREATE VIEW event_info
AS
SELECT
    events.event_id,
    events.event_name,
    clubs.club_name,
    events.event_description,
    events.venue,
    events.date,
    events.time,
    events.club_id
FROM
    events
INNER JOIN clubs USING (club_id)
ORDER BY
    events.event_id;

--========================================================== End ========================================================--
