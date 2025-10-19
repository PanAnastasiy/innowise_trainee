
--FOR TESTING
CREATE OR REPLACE FUNCTION TEST_2(
    P_PARAM1 DATE,
    P_PARAM2 TIMESTAMP,
    P_PARAM3 DATE
)
    RETURNS VARCHAR
    LANGUAGE SQL
AS
$$
    'TEST_2 executed with: ' || P_PARAM1 || ', ' || P_PARAM2 || ', ' || P_PARAM3
$$;


CREATE OR REPLACE TEMPORARY TABLE PROC_PARAMS (
                                                  PARAM1 DATE,
                                                  PARAM2 TIMESTAMP,
                                                  PARAM3 DATE
);

INSERT INTO PROC_PARAMS (PARAM1, PARAM2, PARAM3) VALUES
                                                     ('2025-02-06','2025-02-12 09:38:25.999982','2025-01-28'),
                                                     ('2025-02-14','2025-02-14 16:17:14.095384','2025-02-06'),
                                                     ('2025-02-20','2025-02-21 08:41:53.643244','2025-02-14');

SELECT TEST_2(PARAM1, PARAM2, PARAM3) AS MESSAGE
FROM PROC_PARAMS
ORDER BY PARAM1;
