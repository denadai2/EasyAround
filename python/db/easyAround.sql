CREATE TABLE client (
  "ID" INTEGER NOT NULL,
  "strengths" SMALLINT NOT NULL, /*1,2,3*/
  "quiet" BOOLEAN NOT NULL,
  "name" varchar(200) NOT NULL,
  PRIMARY KEY ("ID")
);

CREATE TABLE IF NOT EXISTS "constraint" (
  "location_ID" int(10) NOT NULL,
  "client_ID" int(10) NOT NULL,
  "type" varchar NOT NULL, /*enum('include','avoid')*/
  PRIMARY KEY ("location_ID","client_ID"),
  FOREIGN KEY(location_ID)
      REFERENCES location(ID)
      ON DELETE CASCADE,
  FOREIGN KEY(client_ID)
      REFERENCES client(ID)
      ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "day" (
  "itinerary_ID" int(10) NOT NULL,
  "date" date NOT NULL,
  PRIMARY KEY ("itinerary_ID","date"),
  FOREIGN KEY(itinerary_ID)
      REFERENCES itinerary(ID)
      ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "itinerary" (
  "ID" int(10) NOT NULL,
  "client_ID" int(10) NOT NULL,
  "withKids" tinyint(1) NOT NULL,
  PRIMARY KEY ("ID"),
  FOREIGN KEY(client_ID)
      REFERENCES client(ID)
      ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "location" (
  "ID" int(10) NOT NULL,
  "lat" decimal(10,8) NOT NULL,
  "lng" decimal(11,8) NOT NULL,
  "name" varchar(200) NOT NULL,
  "description" text NOT NULL,
  "rating" SMALLINT NOT NULL, /*enum('1','2','3','4','5')*/
  "intensive" tinyint(1) NOT NULL,
  "forKids" tinyint(1) DEFAULT NULL,
  PRIMARY KEY ("ID")
);

CREATE TABLE IF NOT EXISTS "preference" (
  "client_ID" int(10) NOT NULL,
  "itinerary_ID" int(10) NOT NULL,
  "type" varchar NOT NULL, /*enum('shopping','culture','gastronomy','nightlife','needsForFreeTime')*/
  "range" SMALLINT NOT NULL, /*enum('1','2','3','4','5')*/
  PRIMARY KEY ("itinerary_ID","client_ID","type")
);

CREATE TABLE IF NOT EXISTS "timeslot" (
  "day_itinerary_ID" int(10) NOT NULL,
  "day_date" date NOT NULL,
  "type" varchar NOT NULL, /*enum('morning','afternoon','evening','meal')*/
  "location_ID" int(10) NOT NULL,
  PRIMARY KEY ("day_itinerary_ID","day_date","type"),
  FOREIGN KEY(day_itinerary_ID)
      REFERENCES day(itinerary_ID)
      ON DELETE CASCADE,
  FOREIGN KEY(day_date)
      REFERENCES day("date")
      ON DELETE CASCADE
);
