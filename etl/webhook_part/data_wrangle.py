import sqlite3

from utils import connect_db

# Construct the data for "Grand Prix" page
def get_races_data():
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        """
    SELECT ra.raceId AS _id, ra.year AS Season, ra.date AS Date, ra.name AS 'Grand Prix',
    d.forename || d.surname AS Winner, c.name AS Constructor,
    ct.name AS Circuit, ct.lat, ct.lng, ct.location AS Location
    FROM drivers AS d
    LEFT JOIN results AS r
    ON d.driverId = r.driverId
    LEFT JOIN races AS ra
    ON r.raceId = ra.raceId
    LEFT JOIN constructors AS c
    ON r.constructorId = c.constructorId
    LEFT JOIN circuits AS ct
    ON ra.circuitId = ct.circuitId
    WHERE r.position = 1
    ORDER BY ra.date
    """
    )
    result = cur.fetchall()
    conn.close()
    return [dict(x) for x in result]


# Construct the data for "Incidents" page
def get_status_data():
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        """
    SELECT ct.circuitId || ra.year || d.driverId AS _id, ra.year AS Season, ra.date AS Date, ct.name AS Circuit, 
    d.forename || ' ' || d.surname AS Driver, c.name AS Constructor, st.status AS Incident
    FROM drivers AS d
    LEFT JOIN results AS r
    ON d.driverId = r.driverId
    LEFT JOIN races AS ra
    ON r.raceId = ra.raceId
    LEFT JOIN constructors AS c
    ON r.constructorId = c.constructorId
    LEFT JOIN circuits AS ct
    ON ra.circuitId = ct.circuitId
    LEFT JOIN status as st
    ON r.statusId = st.statusId
    WHERE st.status NOT LIKE '%Lap%' AND st.status != 'Finished'
    ORDER BY ra.date
    """
    )
    result = cur.fetchall()
    conn.close()
    return result


# Construct the data for "Drivers" page
def get_drivers_performance():
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        """
    SELECT d.driverId || ra.raceId || ra.year || d.surname AS _id, d.forename || ' ' || d.surname AS Driver, ct.name AS Circuit,
    c.name AS Constructor, r.position as Position,
    d_st.points AS Points, ra.round AS Round, ra.year AS Season,
    r.grid AS Grid
    FROM drivers AS d
    LEFT JOIN results AS r
    ON d.driverId = r.driverId
    LEFT JOIN races AS ra
    ON r.raceId = ra.RaceId
    LEFT JOIN constructors AS c
    ON r.constructorId = c.constructorId
    LEFT JOIN circuits AS ct
    ON ra.circuitId = ct.circuitId
    LEFT JOIN driver_standings AS d_st
    ON d.driverId = d_st.driverId AND ra.raceId = d_st.raceId
    ORDER BY ra.year 
    """
    )
    result = cur.fetchall()
    conn.close()
    return result


# Construct the data for "Seasons" page
def get_drivers_season_data():
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        """
        WITH podiums AS (
            SELECT d.driverId, ra.year, 
			COUNT(DISTINCT r.raceId) AS Podiums
            FROM drivers AS d
            LEFT JOIN results AS r
            ON d.driverId = r.driverId
            LEFT JOIN races AS ra
            ON r.raceId = ra.raceId
            WHERE r.position IN (1, 2, 3)
            GROUP BY 1, 2
            )
        SELECT d.driverId || ra.year AS _id, d.forename || ' ' || d.surname AS Driver, 
        d.nationality AS Nationality, ra.year AS Season,
        MAX(CAST(d_st.points AS FLOAT)) AS Points,
        p.Podiums
        FROM drivers AS d
        LEFT JOIN driver_standings AS d_st
        ON d.driverId = d_st.driverId
        LEFT JOIN races AS ra
        ON d_st.raceId = ra.raceId
        LEFT JOIN podiums AS p
        ON d.driverId = p.driverId AND ra.year = p.year
        GROUP BY 1, 2, 3, 4
        ORDER BY 5 DESC
    """
    )
    result = cur.fetchall()
    conn.close()
    return result


# Construct the data for "Seasons" page
def get_constructors_season_data():
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        """
        WITH podiums AS (
            SELECT c.constructorId, ra.year, 
			COUNT(DISTINCT r.raceId) AS Podiums
            FROM constructors AS c
            LEFT JOIN results AS r
            ON c.constructorId = r.constructorId
            LEFT JOIN races AS ra
            ON r.raceId = ra.raceId
            WHERE r.position IN (1, 2, 3)
            GROUP BY 1, 2
            )
        SELECT c.constructorId || ra.year AS _id, c.name AS Constructor, 
        c.nationality AS Nationality, ra.year AS Season,
        MAX(CAST(c_st.points AS FLOAT)) AS Points,
        p.Podiums
        FROM constructors AS c
        LEFT JOIN constructor_standings AS c_st
        ON c.constructorId = c_st.constructorId
        LEFT JOIN races AS ra
        ON c_st.raceId = ra.raceId
        LEFT JOIN podiums AS p
        ON c.constructorId = p.constructorId AND ra.year = p.year
        GROUP BY 1, 2, 3, 4
        ORDER BY 5 DESC
    """
    )
    result = cur.fetchall()
    conn.close()
    return result


# Get max year
def get_seasons():
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        """
        SELECT DISTINCT year AS _id, year AS Season
        FROM races
        ORDER BY 1 DESC
    """
    )
    result = cur.fetchall()
    conn.close()
    return result


# Get drivers list
def get_drivers():
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        """
        SELECT DISTINCT driverId AS _id, driver FROM (
        SELECT driverId, forename || ' ' || surname AS driver
        FROM drivers
        ) AS sub
        ORDER BY 2
    """
    )
    result = cur.fetchall()
    conn.close()
    return result
