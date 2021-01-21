/*    */ import java.io.UnsupportedEncodingException;
/*    */ import java.security.InvalidKeyException;
/*    */ import java.security.Key;
/*    */ import java.security.NoSuchAlgorithmException;
/*    */ import java.util.Base64;
/*    */ import javax.crypto.BadPaddingException;
/*    */ import javax.crypto.Cipher;
/*    */ import javax.crypto.IllegalBlockSizeException;
/*    */ import javax.crypto.NoSuchPaddingException;
/*    */ import javax.crypto.spec.SecretKeySpec;
/*    */ 
/*    */ 
/*    */ 
/*    */ 
/*    */ 
/*    */ 
/*    */ 
/*    */ 
/*    */ 
/*    */ public class Cryptor
/*    */ {
/*    */   private String secret;
/*    */   
/* 24 */   public String getSecret() { return this.secret; }
/*    */ 
/*    */ 
/*    */   
/* 28 */   public void setSecret(String secret) { this.secret = secret; }
/*    */ 
/*    */ 
/*    */   
/*    */   public String encrypt(String key, String text) throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidKeyException, BadPaddingException, IllegalBlockSizeException, UnsupportedEncodingException {
/* 33 */     Key aesKey = new SecretKeySpec(key.getBytes(), "AES");
/* 34 */     Cipher cipher = Cipher.getInstance("AES");
/* 35 */     cipher.init(1, aesKey);
/* 36 */     byte[] encrypted = cipher.doFinal(text.getBytes());
/*    */     
/* 38 */     return Base64.getEncoder().encodeToString(encrypted);
/*    */   }
/*    */ 
/*    */   
/*    */   public String decrypt(String key, String text) throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidKeyException, BadPaddingException, IllegalBlockSizeException, UnsupportedEncodingException {
/*    */     try {
/* 44 */       Key aesKey = new SecretKeySpec(key.getBytes(), "AES");
/* 45 */       Cipher cipher = Cipher.getInstance("AES");
/* 46 */       cipher.init(2, aesKey);
/* 47 */       return new String(cipher.doFinal(Base64.getDecoder().decode(text)));
/*    */ 
/*    */     
/*    */     }
/* 51 */     catch (InvalidKeyException i) {
/*    */       
/* 53 */       System.out.println("[x] Invalid key length {16 required}");
/*    */       
/* 55 */       return null;
/*    */     } 
/*    */   }
/*    */ }


/* Location:              /root/repos/CTF-writeups/VulnHub/Warzone: 3/post/secpasskeeper.jar!/Cryptor.class
 * Java compiler version: 14 (58.0)
 * JD-Core Version:       1.0.7
 */