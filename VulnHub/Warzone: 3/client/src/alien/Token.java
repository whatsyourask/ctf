/*    */ package alien;
/*    */ 
/*    */ import java.io.Serializable;
/*    */ 
/*    */ public class Token
/*    */   implements Serializable
/*    */ {
/*    */   private String value;
/*    */   private String role;
/*    */   
/*    */   public Token(String value, String role) {
/* 12 */     this.value = value;
/* 13 */     this.role = role;
/*    */   }
/*    */   
/*    */   public String getValue() {
/* 17 */     return this.value;
/*    */   }
/*    */   
/*    */   public void setValue(String value) {
/* 21 */     this.value = value;
/*    */   }
/*    */   
/*    */   public String getRole() {
/* 25 */     return this.role;
/*    */   }
/*    */   
/*    */   public void setRole(String role) {
/* 29 */     this.role = role;
/*    */   }
/*    */ 
/*    */   
/*    */   public String toString() {
/* 34 */     return "Token [value=" + this.value + ", role=" + this.role + "]";
/*    */   }
/*    */ }


/* Location:              /root/repos/CTF-writeups/VulnHub/Warzone: 3/ftp/alienclient.jar!/alien/Token.class
 * Java compiler version: 11 (55.0)
 * JD-Core Version:       1.1.3
 */