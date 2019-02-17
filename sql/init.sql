CREATE TABLE countries(
    id_country integer primary key,
    name text
);

CREATE TABLE channels(
    id_channel integer primary key,
    name text
);

CREATE TABLE campaigns (
    id_campaign integer primary key,
    name text
);

CREATE TABLE operating_systems (
    id_os integer primary key,
    name text
);

INSERT INTO countries(name) VALUES
       ('russia'),
       ('germany'),
       ('usa');

INSERT INTO operating_systems(name) VALUES
       ('windows'),
       ('linux'),
       ('mac');

INSERT INTO campaigns(name) VALUES
       ('campaign_1'),
       ('campaign_2'),
       ('campaign_3');

INSERT INTO channels(name) VALUES
       ('channel_1'),
       ('channel_2'),
       ('channel_3');


CREATE TABLE records(
       id_record INTEGER PRIMARY KEY,
       impressions INTEGER DEFAULT 0,
       clicks INTEGER DEFAULT 0,
       installs INTEGER DEFAULT 0,
       spend INTEGER DEFAULT 0,
       revenue INTEGER DEFAULT 0,
       record_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
       id_channel INTEGER NOT NULL,
       id_campaign INTEGER NOT NULL,
       id_country INTEGER NOT NULL,
       id_os INTEGER NOT NULL,
       FOREIGN KEY(id_channel) REFERENCES channels(id_channel),
       FOREIGN KEY(id_campaign) REFERENCES campaigns(id_campaign),
       FOREIGN KEY(id_country) REFERENCES countries(id_country),
       FOREIGN KEY(id_os) REFERENCES operating_systems(id_os)
);


CREATE INDEX idx_date ON records(record_date);
CREATE INDEX idx_ch ON records(id_channel);
CREATE INDEX idx_cnt ON records(id_country);
CREATE INDEX idx_os ON records(id_os);
CREATE INDEX idx_cmp ON records(id_campaign);

