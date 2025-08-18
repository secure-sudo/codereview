import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class SecureApp {

    public static void main(String[] args) {
        // ✅ Load credentials from environment variables or secure vaultt
        String dbUser = System.getenv("DB_USER");
        String dbPass = System.getenv("DB_PASS");
        String dbUrl  = System.getenv("DB_URL"); // e.g., jdbc:mysql://localhost:3306/testdb

        if (dbUser == null || dbPass == null || dbUrl == null) {
            System.err.println("Database credentials missing! Set DB_USER, DB_PASS, DB_URL.");
            return;
        }

        try (Connection conn = DriverManager.getConnection(dbUrl, dbUser, dbPass)) {

            // ✅ Use parameterized queries to prevent SQL injection
            String query = "SELECT username, email FROM users WHERE id = ?";
            try (PreparedStatement stmt = conn.prepareStatement(query)) {
                int userId = 1; // Example safe input (never concatenate user input!)
                stmt.setInt(1, userId);

                try (ResultSet rs = stmt.executeQuery()) {
                    while (rs.next()) {
                        System.out.println("Username: " + rs.getString("username"));
                        System.out.println("Email: " + rs.getString("email"));
                    }
                }
            }

            // ✅ Avoid any hardcoded secrets or passwords in code
            // Secrets should always be retrieved from environment variables, vaults, or encrypted storage

            // ✅ No insecure deserialization, no command execution, no debug mode

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
