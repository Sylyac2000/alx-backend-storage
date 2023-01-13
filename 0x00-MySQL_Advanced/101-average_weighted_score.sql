--  Write a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers ()
BEGIN
    ALTER TABLE users ADD total_poids_score INT NOT NULL;
    ALTER TABLE users ADD total_weight INT NOT NULL;

    UPDATE users
        SET total_poids_score = (
            SELECT SUM(corrections.score * projects.weight)
            FROM corrections
                INNER JOIN projects
                    ON corrections.project_id = projects.id
            WHERE corrections.user_id = users.id
            );

    UPDATE users
        SET total_weight = (
            SELECT SUM(projects.weight)
                FROM corrections
                    INNER JOIN projects
                        ON corrections.project_id = projects.id
                WHERE corrections.user_id = users.id
            );

    UPDATE users
        SET users.average_score = IF(users.total_weight = 0, 0, users.total_poids_score / users.total_weight);
    ALTER TABLE users
        DROP COLUMN total_poids_score;
    ALTER TABLE users
        DROP COLUMN total_weight;
END $$
DELIMITER ;
