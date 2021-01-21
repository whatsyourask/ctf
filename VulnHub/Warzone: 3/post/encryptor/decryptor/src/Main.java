package alienum;

import java.io.File;
import java.io.IOException;



public class Main
{
  static String path = "aliens.txt";


  
  public static void main(String[] args) throws IOException, ClassNotFoundException {
    String key = "w4rz0nerex0gener";
    File inputFile = new File("aliens.encrypted");
    File encryptedFile = new File("aliens.txt");
    
    try {
      Cryptor.encrypt(key, inputFile, encryptedFile);
    } catch (CryptoException ex) {
      System.out.println(ex.getMessage());
      ex.printStackTrace();
    } 
  }
}

