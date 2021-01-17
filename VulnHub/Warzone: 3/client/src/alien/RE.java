/*    */ package alien;
/*    */ 
/*    */ import java.io.Serializable;
/*    */ 
/*    */ 
/*    */ 
/*    */ 
/*    */ public class RE
/*    */   implements Serializable
/*    */ {
/*    */   private Token token;
/*    */   private String option;
/*    */   private String cmd;
/*    */   private String value;
/*    */   
/*    */   public RE() {}
/*    */   
/*    */   public RE(Token token, String option, String cmd, String value) {
/* 19 */     this.token = token;
/* 20 */     this.option = option;
/* 21 */     this.cmd = cmd;
/* 22 */     this.value = value;
/*    */   }
/*    */ 
/*    */   
/*    */   public Token getToken() {
/* 27 */     return this.token;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setToken(Token token) {
/* 32 */     this.token = token;
/*    */   }
/*    */ 
/*    */   
/*    */   public String getOption() {
/* 37 */     return this.option;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setOption(String option) {
/* 42 */     this.option = option;
/*    */   }
/*    */ 
/*    */   
/*    */   public String getCmd() {
/* 47 */     return this.cmd;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setCmd(String cmd) {
/* 52 */     this.cmd = cmd;
/*    */   }
/*    */ 
/*    */   
/*    */   public String getValue() {
/* 57 */     return this.value;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setValue(String value) {
/* 62 */     this.value = value;
/*    */   }
/*    */ 
/*    */ 
/*    */   
/*    */   public String toString() {
/* 68 */     return "RE [ " + this.token + ", option=" + this.option + ", cmd=" + this.cmd + ", value=" + this.value + "]";
/*    */   }
/*    */ }


/* Location:              /root/repos/CTF-writeups/VulnHub/Warzone: 3/ftp/alienclient.jar!/alien/RE.class
 * Java compiler version: 11 (55.0)
 * JD-Core Version:       1.1.3
 */