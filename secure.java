import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.Scanner;

public class SecureApp {

    public static void main(String[] args) {
        // Use environment variables for credentials instead of hardcoding
        String dbUser = System.getenv("DB_USER");
        String dbPass = System.getenv("DB_PASS");
        String dbUrl  = System.getenv("DB_URL"); // e.g., jdbc:mysql://localhost:3306/testdb

        if (dbUser == null || dbPass == null || dbUrl == null) {
            System.err.println("Database credentials not set in environment variables!");
            return;
        }

        try (Connection conn = DriverManager.getConnection(dbUrl, dbUser, dbPass)) {

            Scanner scanner = new Scanner(System.in);
            System.out.print("Enter user ID to fetch: ");
            int userId = scanner.nextInt();

            // Use PreparedStatement to prevent SQL Injection
            String query = "SELECT username, email FROM users WHERE id = ?";
            try (PreparedStatement stmt = conn.prepareStatement(query)) {
                stmt.setInt(1, userId);

                try (ResultSet rs = stmt.executeQuery()) {
                    if (rs.next()) {
                        System.out.println("Username: " + rs.getString("username"));
                        System.out.println("Email: " + rs.getString("email"));
                    } else {
                        System.out.println("User not found.");
                    }
                }
            }

            // Secure handling of secrets: no weak Base64 encoding
            // Instead, store sensitive info in environment variables or a secure vault
            String secret = System.getenv("SECRET_KEY");
            if (secret != null) {
                System.out.println("Secret length: " + secret.length());
            }

            // Avoid insecure deserialization entirely
            // Use JSON or protobuf libraries with strict schemas instead

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
