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
    -------------------------------------------------
    PRIMARY KEY (user_id)
);

CREATE TABLE login (
    user_id             INTEGER         NOT NULL,
    username            TEXT            NOT NULL,
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
    event_id            INTEGER,
    club_id             INTEGER,
    event_name          TEXT,
    event_description   TEXT,
    venue               TEXT,
    date_and_time       DATETIME,
    created             DATETIME        DEFAULT CURRENT_TIMESTAMP,
    updated             DATETIME        DEFAULT CURRENT_TIMESTAMP,
    -----------------------------------------------
    PRIMARY KEY (event_id),
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
