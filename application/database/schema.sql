CREATE TABLE users (
    user_id     INTEGER     NOT NULL PRIMARY KEY,
    username    TEXT        NOT NULL,
    password    TEXT        NOT NULL,
    approved    TEXT        DEFAULT 'Pending' CHECK (approved IN ('Pending', 'Approved', 'Rejected')),
    first_name  TEXT,
    last_name   TEXT,
    age         INTEGER,
    email       TEXT,
    phone       TEXT,
    gender      TEXT,
    FOREIGN KEY (username) REFERENCES login(username)
);



CREATE TABLE login (
    username    TEXT        NOT NULL,
    password    TEXT        NOT NULL,
    FOREIGN KEY (username) REFERENCES users(username)
);


CREATE TABLE coordinators (
    coordinator_id  INTEGER PRIMARY KEY,
    FOREIGN KEY (user_id)   REFERENCES users (user_id)
);

CREATE TABLE admin (
    user_id     INTEGER     PRIMARY KEY,
    FOREIGN KEY (user_id)   REFERENCES users (user_id)
);

Create table clubs(
  club_id Integer primary key AUTOINCREMENT,
  club_name varchar(400),
  club_description varchar(1000),
  coordinator_id integer,
  validity varchar(20) check (validity in ('Pending', 'Approved', 'Rejected')) default 'Pending',
  created datetime default CURRENT_TIMESTAMP,
  updated datetime DEFAULT CURRENT_TIMESTAMP,
  FOREIGN key (coordinator_id) REFERENCES coordinators(coordinator_id));

  Create table club_memberships(
  club_id Integer,
  user_id Integer,
  validity varchar(20) check (validity in ('Pending', 'Approved', 'Rejected')),
  created datetime default CURRENT_TIMESTAMP,
  updated datetime DEFAULT CURRENT_TIMESTAMP,
  Primary key (club_id, user_id),
  FOREIGN key (club_id) REFERENCES clubs(club_id));


 Create table events(
  event_id Integer primary key AUTOINCREMENT,
  club_id integer,
  event_name varchar(300),
  event_description varchar(1000),
  date_and_time datetime,
  venue varchar(400),
  created datetime default CURRENT_TIMESTAMP,
  updated datetime DEFAULT CURRENT_TIMESTAMP,
  FOREIGN key (club_id) REFERENCES clubs(club_id));

  Create table if event_participants(
  event_id Integer,
  user_id integer,
  validity varchar(20) check (validity in ('Pending', 'Approved', 'Rejected')),
  created datetime default CURRENT_TIMESTAMP,
  updated datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY key (event_id, user_id),
  FOREIGN key (user_id) REFERENCES users(user_id)
  FOREIGN key (event_id) REFERENCES events(event_id));



  CREATE TRIGGER check_max_clubs
  BEFORE INSERT ON club_memberships
  BEGIN
      SELECT CASE
          WHEN (SELECT COUNT(*) FROM club_memberships WHERE user_id = NEW.user_id) >= 3
          THEN
              RAISE(ABORT, 'Cannot add more than 3 clubs for a user');
      END;
  END;

