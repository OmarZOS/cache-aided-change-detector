import helma.xmlrpc.WebServer;
import lthash.Blake2bDigest;
import lthash.LtHash32;
import lthash.Digest;

import java.util.HashMap;
import java.util.Hashtable;

public class Hasher 
{  
   // // It was meant to be done this way, but you know.. life isn't fair most of the time..
   // // lthash implmentation doesn't offer a direct way to substract checksum and I wouldn't bother myself checking inside..
   // HashMap checks   umIndex = new HashMap<Integer,byte[]>();
   // byte[] checksum = ltHash.getChecksum();
   
   HashMap userIndex = new HashMap<String,byte[]>();
   HashMap userIndex_raw = new HashMap<String,String>();

   LtHash32 ltHash = new LtHash32();

   byte[] userChecksum;

   private final Digest digest = new Blake2bDigest();
   
   static long beforeUsedMem=0;
   static long previous=0;
   static long afterUsedMem=0;
   static boolean similar=false;

   Runtime rt = Runtime.getRuntime();

   public void set_current_memory_usage_as_default(){
      beforeUsedMem = Runtime.getRuntime().totalMemory()-Runtime.getRuntime().freeMemory();
   }

   public float get_memory_difference(){
      afterUsedMem=rt.totalMemory() -rt.freeMemory();// totalMemory -Runtime.getRuntime().freeMemory()
      // System.out.print("Memory used: ");
      // System.out.println(afterUsedMem-beforeUsedMem);
      previous=afterUsedMem-beforeUsedMem;
      return (float)(previous);
      // if(afterUsedMem-beforeUsedMem>0){
      //    return (float)(previous);
      // }
      // return (float)(previous);
   }


   public byte[] get_hash(byte[] input) {
      byte[] hash = this.digest.hash(input);
      return hash;
   }


   // This public method will be exposed to XML-RPC client
   public Hashtable sumAndDifference(int x, int y) {

      Hashtable result = new Hashtable();
      result.put("sum", new Integer(x + y));
      result.put("difference", new Integer(x - y));
      return result;
   }

   public int get_index_size(){
      return userIndex.size();
   }

   public boolean add_node_hash(String nodeId,String hashableAttributes) {

      // System.out.println("Adding a node");

      if (userIndex.containsKey(nodeId)){
         // byte[] checksum 
         ltHash.applyHashToChecksum((a,b)->a-b,(byte[]) userIndex.get(nodeId));

         byte[] new_node = get_hash((nodeId+","+hashableAttributes).getBytes());

         ltHash.applyHashToChecksum((a,b)->a+b,new_node);
         
         similar = ltHash.checksumEquals(userChecksum);
         
         // System.out.println(","+hashableAttributes);
         // System.out.println(","+userIndex.get(nodeId));
         // System.out.println(similar);
         if(similar){
            // System.out.println("Unchanged node");
            // propagateUpdate(nodeId,hashableAttributes);
            return true;
         }
         else{
            System.out.println("Node changed, updating..");
            propagateUpdate(nodeId,hashableAttributes);
            return false;
         }
      }
      else{
         System.out.println("Node not found, adding a new one..");
         propagateUpdate(nodeId,hashableAttributes);
         return false;
      }
   }

   public boolean add_node_raw(String nodeId,String hashableAttributes) {

      // System.out.println("Adding a node");

      if (userIndex_raw.containsKey(nodeId)){
         // byte[] checksum 
         // ltHash.applyHashToChecksum((a,b)->a-b,(byte[]) userIndex_raw.get(nodeId));

         // byte[] new_node = get_hash((nodeId+","+hashableAttributes).getBytes());

         // ltHash.applyHashToChecksum((a,b)->a+b,new_node);
         
         similar = userIndex_raw.get(nodeId).equals(hashableAttributes);
         
         // System.out.println(","+hashableAttributes);
         // System.out.println(","+userIndex.get(nodeId));
         // System.out.println(similar);
         if(similar){
            // System.out.println("Unchanged node");
            propagateUpdate_raw(nodeId,hashableAttributes);
            return true;
         }
         else{
            System.out.println("Node changed, updating..");
            propagateUpdate_raw(nodeId,hashableAttributes);
            return false;
         }
      }
      else{
         System.out.println("Node not found, adding a new one..");
         propagateUpdate_raw(nodeId,hashableAttributes);
         return false;
      }
      
   }

   protected void propagateUpdate(String nodeId,String newhashableAttributes) {
      
      if(! userIndex.containsKey(nodeId)){
         ltHash.add((nodeId+","+newhashableAttributes).getBytes());  
      }
      userChecksum = ltHash.getChecksum();
      userIndex.put(nodeId,get_hash((nodeId +","+newhashableAttributes).getBytes()));
   }
   protected void propagateUpdate_raw(String nodeId,String newhashableAttributes) {
      
      userIndex_raw.put(nodeId,newhashableAttributes);  
   }

   public boolean add_edge_hash(String edgeType) {
      System.out.println("How much do you wanna risk?");
      
      return true;
   }

   public void print() {
      System.out.println("Print Systems");
   }

   public static void main( String[] args ) {
      try {
         int port = Integer.parseInt(System.getenv("HASH_SERVER_PORT"));
         WebServer server = new WebServer(port);
         // Our handler is a regular java object
         Hasher hasher = new Hasher();
         hasher.set_current_memory_usage_as_default();
         server.addHandler("handler", hasher);
      } catch (Exception exception) {
         System.out.println("JavaServer " + exception.toString());
      }
   }
}