/*    */ import java.io.UnsupportedEncodingException;
/*    */ import java.security.InvalidKeyException;
/*    */ import java.security.NoSuchAlgorithmException;
/*    */ import java.util.Scanner;
/*    */ import javax.crypto.BadPaddingException;
/*    */ import javax.crypto.IllegalBlockSizeException;
/*    */ import javax.crypto.NoSuchPaddingException;
/*    */ 
/*    */ 
/*    */ 
/*    */ 
/*    */ 
/*    */ 
/*    */ public class Main
/*    */ {
/*    */   public static void main(String[] args) throws InvalidKeyException, NoSuchPaddingException, NoSuchAlgorithmException, BadPaddingException, IllegalBlockSizeException, UnsupportedEncodingException {
/*    */     try {
/* 18 */       Scanner in = new Scanner(System.in);
/* 19 */       System.out.println("[Warzone 3] Root's Password Manager");
/* 22 */       Cryptor cryptor = new Cryptor();
/* 23 */       Resources res = new Resources();
/* 25 */       String sys = cryptor.decrypt(cryptor.decrypt(res.gotSecret(), removeSalt(res.getSecret())), removeSalt(res.getCipher()));
/* 27 */       String plaintext = cryptor.decrypt(cryptor.decrypt(res.gotSecret(), removeSalt(res.getSecret())), removeSalt(res.getCipher()));
/* 28 */       System.out.println("[+] Success, the password is : " + plaintext);
/*    */     
/* 34 */     } catch (NullPointerException n) {
/* 35 */       System.out.println("[!] Terminated");
/* 36 */       System.exit(0);
/*    */     } 
/*    */   }
/*    */ 
/*    */ 
/*    */ 
/*    */   
/* 43 */   public static String removeSalt(String salted) { return salted.replace("al13n", ""); }
/*    */ }


/* Location:              /root/repos/CTF-writeups/VulnHub/Warzone: 3/post/secpasskeeper.jar!/Main.class
 * Java compiler version: 14 (58.0)
 * JD-Core Version:       1.0.7
 */
