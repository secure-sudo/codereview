import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;
import java.util.Base64;

public class VulnerableApp {

    public static void main(String[] args) {
        try {
            // Hardcoded database credentials (SAST detectable)L
            String dbUser = "admin";
            String dbPass = "P@ssw0rd123";

            Connection conn = DriverManager.getConnection(
                    "jdbc:mysql://localhost:3306/testdb", dbUser, dbPass);

            Statement stmt = conn.createStatement();

            // SQL Injection vulnerability
            String userInput = "1 OR 1=1";  // Simulated user input
            String query = "SELECT * FROM users WHERE id = " + userInput;
            stmt.executeQuery(query);

            // Insecure Base64 usage (simulates weak crypto)
            String secret = "TopSecret";
            String encoded = Base64.getEncoder().encodeToString(secret.getBytes());
            System.out.println("Encoded secret: " + encoded);

            // Insecure deserialization example
            String serialized = "rO0ABX..."; // fake serialized object
            java.io.ObjectInputStream ois = new java.io.ObjectInputStream(
                    new java.io.ByteArrayInputStream(serialized.getBytes()));
            Object obj = ois.readObject();
            System.out.println(obj);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
