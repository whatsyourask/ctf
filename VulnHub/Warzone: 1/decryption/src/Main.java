package decrypt;

import java.util.Scanner;
import crypto.AES;

public class Main {
  public static void main(String[] args) {
    System.out.println("Symmetric Decryption by Alienum");
    Scanner in = new Scanner(System.in);
    System.out.print("enter the encrypted password to decrypt : ");
    String password = in.nextLine();
    System.out.println("decrypted password : " + AES.decryptString(password));
    System.exit(0);
  }

}
